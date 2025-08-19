import requests

def scrape_remoteok():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    data = resp.json()
    jobs = []

    # First item in API response is metadata, skip it
    for job in data[1:20]:  # limit to 20
        jobs.append({
            "title": job.get("position"),
            "company": job.get("company"),
            "url": job.get("url"),
            "summary": job.get("tags", []),  # tags as summary
            "logo": job.get("company_logo"),
            "source": "remoteok"
        })

    return jobs
