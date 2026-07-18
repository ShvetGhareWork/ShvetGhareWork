"""
fetch_contributions.py
----------------------
Scrapes the unauthenticated GitHub contribution graph endpoint and saves the
data as data/contributions.json — no personal access token required.

Set USERNAME below (or override via the USERNAME env variable) to target any
public GitHub account.

Output:
    data/contributions.json
"""

import json
import os

import requests
from bs4 import BeautifulSoup

# ── Configuration ─────────────────────────────────────────────────────────────
USERNAME = os.environ.get("GH_USERNAME", "SHVETGHAREWORK")
# ──────────────────────────────────────────────────────────────────────────────


def fetch_contributions(username: str = USERNAME) -> None:
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}

    print(f"Fetching contribution graph for @{username} …")
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    days_data: list[dict] = []

    # GitHub's contribution calendar cells
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level")
        if date and level is not None:
            days_data.append({"date": date, "level": int(level)})

    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "contributions.json")
    with open(out_path, "w") as f:
        json.dump({"days": days_data}, f, indent=2)

    print(f"Saved {len(days_data)} days of contributions to {out_path}")


if __name__ == "__main__":
    fetch_contributions()
