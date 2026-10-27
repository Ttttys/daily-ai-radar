import requests
import re
from datetime import datetime

GITHUB_TRENDING_URL = "https://github.com/trending?since=daily"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_trending():
    resp = requests.get(GITHUB_TRENDING_URL, headers=HEADERS)
    resp.raise_for_status()
    return resp.text

def extract_repos(html):
    # Simple regex to capture repo names and descriptions
    pattern = r'<article class="Box-row">.*?<h2.*?<a href="/([\w.-]+/[\w.-]+)".*?</a>.*?<p.*?>(.*?)</p>' 
    matches = re.findall(pattern, html, re.S)
    repos = []
    for full_name, desc in matches[:10]:
        clean_desc = re.sub(r'<[^>]+>', '', desc).strip()
        repos.append((full_name, clean_desc))
    return repos

def generate_digest(repos):
    today = datetime.now().strftime('%Y-%m-%d')
    lines = [f"# Daily AI Radar - {today}", ""]
    lines.append("## Trending Repos")
    for name, desc in repos:
        lines.append(f"- **{name}**: {desc if desc else 'No description'}")
    lines.append("\n*Generated automatically*")
    return "\n".join(lines)

def main():
    try:
        html = fetch_trending()
        repos = extract_repos(html)
        digest = generate_digest(repos)
        with open("daily_radar.md", "w", encoding="utf-8") as f:
            f.write(digest)
        print("Digest saved to daily_radar.md")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
