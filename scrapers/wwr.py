import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings

# Silence the XML warning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def scrape_wwr():
    url = "https://weworkremotely.com/categories/remote-programming-jobs"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # Try parsing as HTML first
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    job_sections = soup.select("section.jobs li:not(.view-all)")
    if not job_sections:
        # fallback: maybe it's XML (feed)
        soup = BeautifulSoup(resp.text, "xml")
        for item in soup.find_all("item"):
            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)
            company = item.find("company") or item.find("dc:creator")
            company = company.get_text(strip=True) if company else "Unknown"

            jobs.append({
                "title": title,
                "company": company,
                "url": link,
                "summary": title,
                "logo": None,
                "source": "weworkremotely"
            })
        return jobs

    # Normal HTML scraping
    for job in job_sections:
        link = job.find("a", href=True)
        if not link:
            continue

        url = "https://weworkremotely.com" + link["href"]
        company = job.find("span", class_="company")
        title = job.find("span", class_="title")

        company = company.get_text(strip=True) if company else "Unknown"
        title = title.get_text(strip=True) if title else "No Title"

        logo_tag = job.find("div", class_="flag-logo")
        logo = logo_tag.find("img")["src"] if logo_tag and logo_tag.find("img") else None

        jobs.append({
            "title": title,
            "company": company,
            "url": url,
            "summary": f"{title} at {company}",
            "logo": logo,
            "source": "weworkremotely"
        })

    return jobs
