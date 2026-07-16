import requests
import base64

REPO = "AnsElvin/solutions-website"
BRANCH = "main"
FILE_PATH = "index.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

response = requests.get(f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}")
print(f"GET status: {response.status_code}")
if response.status_code == 200:
    sha = response.json().get("sha")
    print(f"Current SHA: {sha}")
    
    data = {
        "message": "Restore tech-style index.html",
        "content": encoded_content,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
    
    print(f"Content length: {len(content)}")
    print(f"Encoded length: {len(encoded_content)}")
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.put(
            f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}",
            json=data,
            headers=headers,
            timeout=30
        )
        print(f"PUT status: {response.status_code}")
        if response.status_code in [200, 201]:
            print("SUCCESS! File updated.")
            print(f"URL: {response.json()['content']['html_url']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
else:
    print(f"Failed to get file info: {response.text}")