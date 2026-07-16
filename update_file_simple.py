import urllib.request
import urllib.error
import json
import base64

REPO = "AnsElvin/solutions-website"
BRANCH = "main"
FILE_PATH = "index.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

try:
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode())
        sha = data.get("sha")
        print(f"Current SHA: {sha}")
    
    put_data = {
        "message": "Restore tech-style index.html",
        "content": encoded_content,
        "branch": BRANCH
    }
    if sha:
        put_data["sha"] = sha
    
    json_data = json.dumps(put_data).encode("utf-8")
    put_req = urllib.request.Request(
        url,
        data=json_data,
        method="PUT",
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(put_req, timeout=30) as response:
        result = json.loads(response.read().decode())
        print(f"Status: {response.status}")
        print(f"SUCCESS! URL: {result['content']['html_url']}")
        
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Response: {e.read().decode()[:500]}")
except Exception as e:
    print(f"Error: {e}")