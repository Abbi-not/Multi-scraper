import requests

def get_workingnomads_jobs():
    url = "https://www.workingnomads.com/jobs/feed"
    res = requests.get(url)
    jobs = []

    if res.status_code == 200:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res.text, "xml")
        for item in soup.find_all("item")[:20]:
            jobs.append({
                "title": item.title.text,
                "company": "",
                "url": item.link.text,
                "date": item.pubDate.text,
                "logo": "",
                "summary": item.description.text[:140]
            })
    return jobs
