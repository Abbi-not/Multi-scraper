import requests
from bs4 import BeautifulSoup

def scrape_jobspresso():
    url = "https://jobspresso.co/remote-work/"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []
    # Each job listing is inside <li class="job_listing"> ... </li>
    job_cards = soup.find_all("li", class_="job_listing")

    for job in job_cards:
        title_elem = job.find("h3")
        company_elem = job.find("div", class_="job_listing-company")
        link_elem = job.find("a", href=True)

        if not title_elem or not link_elem:
            continue

        jobs.append({
            "title": title_elem.get_text(strip=True),
            "company": company_elem.get_text(strip=True) if company_elem else "N/A",
            "link": link_elem["href"],
            "source": "Jobspresso"
        })

    return jobs
