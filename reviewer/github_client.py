# github_client.py
import requests

class GitHubClient:
    def __init__(self, token, repo, pr_number):
        self.token = token
        self.repo = repo  # "username/reponame"
        self.pr_number = pr_number
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def get_pr_diff(self):
        url = f"https://api.github.com/repos/{self.repo}/pulls/{self.pr_number}"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
        resp = requests.get(url, headers=headers)
        return resp.text

    def get_changed_files(self):
        url = f"https://api.github.com/repos/{self.repo}/pulls/{self.pr_number}/files"
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def post_review_comment(self, body, commit_id, path, line):
        url = f"https://api.github.com/repos/{self.repo}/pulls/{self.pr_number}/comments"
        payload = {
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "line": line
        }
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def post_general_comment(self, body):
        url = f"https://api.github.com/repos/{self.repo}/issues/{self.pr_number}/comments"
        resp = requests.post(url, headers=self.headers, json={"body": body})
        return resp.json()