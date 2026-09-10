#!/usr/bin/env python3
"""Push local Bean-There-QLD HEAD to GitHub main via the git-database REST API.

SSH/HTTPS git transport is blocked from this machine, so pushes go through
blobs -> tree -> commit -> ref. Uses the custom.github surrogate credential
(via authd), which has Contents read+write but NOT Workflows scope, so
.github/workflows/* files are never part of a push (there are none here,
and the script refuses if one ever appears).

Unlike the beanie-day twin, the local repo is fresh (no local base to diff
against), so the script reconciles against the remote tree directly: every
path in the local tree must either be new on remote or have a blob SHA
identical to the local one, otherwise it refuses to avoid clobbering.
For follow-up pushes it diffs local HEAD against HEAD~1 (the previously
pushed state) and applies only those changes onto the remote tree,
refusing on workflow paths or on paths changed remotely since the base.
"""
import base64, json, subprocess, sys, urllib.request, urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

REPO = "marcustayye93/Bean-There-QLD"
API = f"https://api.github.com/repos/{REPO}"
HOSTS = ("api.github.com",)
WORK = "/home/hatch/workspace/bean-there-qld"

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"Accept": "application/vnd.github+json"})
    add_surrogate_to_request(req, "custom.github", allowed_hosts=HOSTS)
    try:
        return read_json_response(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        if e.code == 409 and method == "GET":
            # Empty repos answer the ref lookup with 409 Conflict instead of 404.
            return None
        raise

def sh(*args):
    return subprocess.run(args, capture_output=True, text=True, check=True,
                          cwd=WORK).stdout.strip()

def ls_tree_local(rev):
    out = sh("git", "ls-tree", "-r", rev)
    m = {}
    for line in out.splitlines():
        parts = line.split()
        m[parts[3]] = parts[2]
    return m

local_head = sh("git", "rev-parse", "HEAD")
head_files = ls_tree_local(local_head)

ref = api("GET", "/git/refs/heads/main")
remote_files = {}
remote_sha = None
remote_tree = None
if ref:
    remote_sha = ref["object"]["sha"]
    print("remote main:", remote_sha)
    remote_commit = api("GET", f"/git/commits/{remote_sha}")
    remote_tree = remote_commit["tree"]["sha"]
    remote_files = {t["path"]: t["sha"] for t in
                    api("GET", f"/git/trees/{remote_tree}?recursive=1")["tree"]
                    if t["type"] == "blob"}
    print("remote files:", len(remote_files))
else:
    print("remote main does not exist yet — initial push")

if remote_sha is None:
    # ---- initial push: every local path must be new or identical on remote ----
    for p, blob in head_files.items():
        r = remote_files.get(p)
        if r is not None and r != blob:
            print(f"REFUSING: {p} differs on remote — manual merge needed")
            sys.exit(1)
    changed = sorted(head_files)
    base_files = {}
else:
    # ---- follow-up push: diff local HEAD against HEAD~1 (the pushed base) ----
    try:
        local_base = sh("git", "rev-parse", "HEAD~1")
    except subprocess.CalledProcessError:
        print("REFUSING: remote exists but local repo has a single commit — "
              "cannot determine the pushed base; push manually")
        sys.exit(1)
    print("local base:", local_base)
    base_files = ls_tree_local(local_base)
    changed = sorted(p for p in set(base_files) | set(head_files)
                     if base_files.get(p) != head_files.get(p))

print("local HEAD:", local_head, "| files:", len(head_files),
      "| changed:", len(changed))

banned = [p for p in changed if p.startswith(".github/workflows/")]
if banned:
    print("REFUSING: push would touch workflow files (no Workflows scope):", banned)
    sys.exit(1)

if remote_sha is not None:
    # Reconcile: every changed path must be untouched on remote since our base.
    for p in changed:
        if remote_files.get(p) != base_files.get(p):
            print(f"REFUSING: {p} changed on remote since local base — manual merge needed")
            sys.exit(1)

entries = []
for p in changed:
    if p in head_files:
        content = subprocess.run(["git", "show", f"{local_head}:{p}"],
                                 capture_output=True, check=True, cwd=WORK).stdout
        blob = api("POST", "/git/blobs", {"content": base64.b64encode(content).decode(),
                                          "encoding": "base64"})
        entries.append({"path": p, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        print("blob:", p)
    else:
        entries.append({"path": p, "mode": "100644", "type": "blob", "sha": None})
        print("delete:", p)
print("blobs uploaded:", len(entries))

payload = {"tree": entries}
if remote_tree:
    payload["base_tree"] = remote_tree
tree = api("POST", "/git/trees", payload)
print("tree:", tree["sha"])

msg = sh("git", "log", "-1", "--format=%B", local_head)
commit_payload = {"message": msg, "tree": tree["sha"]}
if remote_sha:
    commit_payload["parents"] = [remote_sha]
commit = api("POST", "/git/commits", commit_payload)
print("commit:", commit["sha"])

if remote_sha:
    api("PATCH", "/git/refs/heads/main", {"sha": commit["sha"]})
    print("main fast-forwarded to", commit["sha"])
else:
    api("POST", "/git/refs", {"ref": "refs/heads/main", "sha": commit["sha"]})
    print("created refs/heads/main at", commit["sha"])
