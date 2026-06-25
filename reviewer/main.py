import os
from github_client import GitHubClient
from diff_parser import parse_diff
from static_analysis import run_static_checks
from llm_reviewer import review_chunk

def main():
    print("Starting AI PR Reviewer...")

    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]
    print(f"Repo: {repo}, PR: {pr_number}")

    client = GitHubClient(token, repo, pr_number)

    print("Fetching PR diff...")
    diff_text = client.get_pr_diff()
    print(f"Diff length: {len(diff_text)} characters")
    if len(diff_text) == 0:
        print("WARNING: Diff is empty. Nothing to review.")

    print("Fetching changed files list...")
    changed_files = client.get_changed_files()
    print(f"Changed files response: {changed_files}")

    parsed_files = parse_diff(diff_text)
    print(f"Parsed {len(parsed_files)} file(s) from diff: {[f['filename'] for f in parsed_files]}")

    static_report = run_static_checks([f["filename"] for f in parsed_files])
    print(f"Static analysis report: {static_report}")

    summary_comments = []
    for file in parsed_files:
        findings = static_report.get(file["filename"], "")
        print(f"Sending {file['filename']} to LLM for review...")
        try:
            review = review_chunk(file["filename"], file["raw_chunk"], findings)
            print(f"LLM review result for {file['filename']}: {review}")
        except Exception as e:
            print(f"ERROR calling LLM for {file['filename']}: {e}")
            continue

        if review["severity"] != "none":
            summary_comments.append(
                f"**{file['filename']}** [{review['severity'].upper()}]: {review['comment']}"
            )

    if summary_comments:
        body = "## 🤖 AI Code Review\n\n" + "\n\n".join(summary_comments)
    else:
        body = "## 🤖 AI Code Review\n\nNo issues found. Looks good!"

    print("Posting comment to PR...")
    result = client.post_general_comment(body)
    print(f"Comment post result: {result}")

if __name__ == "__main__":
    main()