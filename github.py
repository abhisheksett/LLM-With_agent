import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

# Load the environment variables
github_token =  os.getenv("GITHUB_TOKEN")

# Fetch the data from the GitHub API
def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {github_token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed with status code: {response.status_code}")
        return []
    return data

# Load the issues into the Document object
def load_issues(issues):
    docs = []
    for issue in issues:
        metadata = {
            "author": issue["user"]["login"],
            "comments": issue["comments"],
            "body": issue["body"],
            "labels": issue["labels"],
            "created_at": issue["created_at"],
        }
        data = issue["title"]
        if issue["body"]:
            data += " " + issue["body"]
        doc = Document(page_content=data, metadata=metadata)
        docs.append(doc)

    return docs

# Fetch the issues from the GitHub API
def fetch_git_issues(owner, repo):
    issues = fetch_github(owner, repo, "issues")
    return load_issues(issues)