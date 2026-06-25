# diff_parser.py
import re

def parse_diff(diff_text):
    """
    Splits a unified diff into per-file chunks with added lines.
    Returns: [{"filename": ..., "added_lines": [...], "raw_chunk": ...}]
    """
    files = []
    current_file = None
    current_chunk = []

    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            if current_file:
                files.append({
                    "filename": current_file,
                    "raw_chunk": "\n".join(current_chunk)
                })
            match = re.search(r"b/(.+)$", line)
            current_file = match.group(1) if match else "unknown"
            current_chunk = []
        else:
            current_chunk.append(line)

    if current_file:
        files.append({"filename": current_file, "raw_chunk": "\n".join(current_chunk)})

    return files