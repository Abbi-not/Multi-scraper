import requests 
from bs4 import BeautifulSoup

def scrape_remotive():
    url = "https://remotive.com/api/remote-jobs"

    try:
        resp = requests.get(url, timeout=15)  # increased timeout
        resp.raise_for_status()  # raise if non-200
    except requests.exceptions.Timeout:
        print("⚠️ Remotive request timed out")
        return []
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching Remotive jobs: {e}")
        return []

    data = resp.json()
    jobs = []

    for job in data.get("jobs", []):
        # Clean up description from HTML
        raw_desc = job.get("description", "")
        summary = ""
        if raw_desc:
            soup = BeautifulSoup(raw_desc, "html.parser")
            summary = soup.get_text(" ", strip=True)[:200] + "..."

        jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "summary": summary,
            "url": job.get("url"),
            "logo": job.get("company_logo_url"),
            "source": "Remotive"
        })

    return jobs
