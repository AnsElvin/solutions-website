import requests
import base64
import json

GITHUB_API = "https://api.github.com"
REPO = "AnsElvin/solutions-website"
BRANCH = "main"

with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

index_encoded = base64.b64encode(index_content.encode("utf-8")).decode("utf-8")

with open(".nojekyll", "r", encoding="utf-8") as f:
    nojekyll_content = f.read()

nojekyll_encoded = base64.b64encode(nojekyll_content.encode("utf-8")).decode("utf-8")

def get_file_sha(path):
    url = f"{GITHUB_API}/repos/{REPO}/contents/{path}?ref={BRANCH}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def update_file(path, content, message):
    sha = get_file_sha(path)
    url = f"{GITHUB_API}/repos/{REPO}/contents/{path}"
    data = {
        "message": message,
        "content": content,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
    response = requests.put(url, json=data)
    print(f"Updating {path}: {response.status_code}")
    if response.status_code in [200, 201]:
        print("Success!")
    else:
        print(f"Error: {response.text}")

print("Updating index.html...")
update_file("index.html", index_encoded, "Update index.html")

print("\nUpdating .nojekyll...")
update_file(".nojekyll", nojekyll_encoded, "Add .nojekyll")

print("\nDone!")