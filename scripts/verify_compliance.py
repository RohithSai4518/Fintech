"""
Audit script checking all rubric requirements.
"""

import os
import subprocess
import zipfile

def main():
    print("=== FINTECH PLATFORM AUTOMATED COMPLIANCE AUDIT ===")

    root_dir = r"E:\Fintech"
    exclude_dirs = {".git", "__pycache__", ".pytest_cache", "tests", "scripts", "data"}
    valid_exts = {".py", ".js", ".html", ".css"}

    total_lines = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs and not d.startswith(".")]
        for f in filenames:
            if os.path.splitext(f)[1] in valid_exts:
                with open(os.path.join(dirpath, f), "r", encoding="utf-8", errors="ignore") as file:
                    total_lines += len(file.readlines())

    status_loc = "PASS" if total_lines >= 50000 else "FAIL"
    print(f"1. Production LOC: {total_lines:,} (Required: >= 50,000) -> {status_loc}")

    has_git = os.path.exists(os.path.join(root_dir, ".git"))
    status_git = "PASS" if has_git else "FAIL"
    print(f"2. Git Repository: .git exists -> {status_git}")

    log_out = subprocess.check_output(["git", "log", "--oneline"], cwd=root_dir, text=True)
    commits = log_out.strip().splitlines()
    pr_merges = [c for c in commits if "Merge pull request" in c]

    status_commits = "PASS" if len(commits) >= 5 else "FAIL"
    status_prs = "PASS" if len(pr_merges) >= 4 else "FAIL"
    print(f"3. Commits Count: {len(commits)} (Required: >= 5) -> {status_commits}")
    print(f"4. Pull Requests / Merges: {len(pr_merges)} (Required: >= 4) -> {status_prs}")

    indicators = ["main.py", "Dockerfile", "docker-compose.yml", "Makefile", "package.json"]
    has_indicators = all(os.path.exists(os.path.join(root_dir, i)) for i in indicators)
    status_ind = "PASS" if has_indicators else "FAIL"
    print(f"5. Executable Indicators ({len(indicators)} files) -> {status_ind}")

    manifests = ["requirements.txt", "package.json", "package-lock.json", "pyproject.toml", "poetry.lock"]
    has_manifests = all(os.path.exists(os.path.join(root_dir, m)) for m in manifests)
    status_man = "PASS" if has_manifests else "FAIL"
    print(f"6. Manifests & Lockfiles ({len(manifests)} files) -> {status_man}")

    zip_path = r"E:\Fintech\Fintech_Enterprise_Platform.zip"
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        has_git_in_zip = any(n.startswith(".git/") or n.startswith(".git\\") for n in names)
    status_zip = "PASS" if has_git_in_zip else "FAIL"
    print(f"7. ZIP Package contains .git history -> {status_zip}")

    test_res = subprocess.run(["python", "-m", "unittest", "discover", "-s", "tests"], cwd=root_dir, capture_output=True)
    status_tests = "PASS" if test_res.returncode == 0 else "FAIL"
    print(f"8. Automated Test Suite Execution -> {status_tests}")
    print("====================================================")

if __name__ == "__main__":
    main()
