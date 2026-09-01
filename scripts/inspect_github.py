"""
Inspects all remote branches and pull requests on GitHub.
"""

import subprocess
import urllib.request
import json

def main():
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate('protocol=https\nhost=github.com\n')
    token = ''
    for line in out.splitlines():
        if line.startswith('password='):
            token = line.split('=', 1)[1].strip()

    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'Fintech-Audit'}

    req = urllib.request.Request('https://api.github.com/repos/RohithSai4518/Fintech/branches', headers=headers)
    with urllib.request.urlopen(req) as r:
        branches = json.loads(r.read().decode())
    print('=== ALL REMOTE BRANCHES ===')
    for b in branches:
        print('  ', b['name'])

    req = urllib.request.Request('https://api.github.com/repos/RohithSai4518/Fintech/pulls?state=all', headers=headers)
    with urllib.request.urlopen(req) as r:
        prs = json.loads(r.read().decode())
    print('\n=== ALL PULL REQUESTS ===')
    for pr in prs:
        print(f"  #{pr['number']}: [{pr['state']}] {pr['title']} ({pr['head']['ref']} -> {pr['base']['ref']})")

if __name__ == '__main__':
    main()
