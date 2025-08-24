import requests
from bs4 import BeautifulSoup

# --- Heuristics --------------------------------------------------------------

TECH_CATEGORIES = {
    "software", "software development", "software developer",
    "devops", "sysadmin", "system", "systems",
    "data", "engineering", "it", "qa", "security",
}

TECH_KEYWORDS = [
    "developer", "engineer", "devops", "sre", "site reliability",
    "frontend", "front-end", "backend", "back-end", "full stack", "full-stack",
    "mobile", "android", "ios",
    "data", "ml", "machine learning", "ai",
    "cloud", "platform", "infra", "infrastructure",
    "security", "qa", "test", "automation",
    "python", "java", "javascript", "typescript", "node", "react", "vue",
    "go", "golang", "rust", "kotlin", "swift", "ruby", "php", "c++", "c#",
    "kubernetes", "docker", "aws", "gcp", "azure",
]

AFRICA_KEYWORDS = [
    "africa", "emea",
    "south africa", "nigeria", "kenya", "ethiopia", "ghana", "uganda",
    "tanzania", "rwanda", "morocco", "egypt", "algeria", "tunisia",
    "senegal", "cameroon", "ivory coast", "cote d'ivoire", "côte d’ivoire",
    "botswana", "namibia", "zimbabwe", "zambia", "angola", "mozambique",
    "mauritius", "madagascar", "liberia", "sierra leone", "gambia",
    "benin", "togo", "niger", "mali", "burkina faso", "chad",
    "sudan", "south sudan", "somalia", "djibouti", "eritrea",
    "lesotho", "eswatini", "swaziland", "mauritania", "seychelles",
    "cape verde", "cabo verde", "libya", "western sahara",
    "sao tome", "são tomé", "comoros", "equatorial guinea",
    "guinea", "guinea-bissau", "central african republic",
    "dr congo", "democratic republic of the congo", "congo", "gabon",
]

WORLDWIDE_TERMS = ["worldwide", "anywhere", "global"]


def _is_tech(job: dict) -> bool:
    """Decide if a job is 'tech' using category/title/tags."""
    cat = (job.get("category") or "").lower()
    if any(c in cat for c in TECH_CATEGORIES):
        return True

    title = (job.get("title") or "").lower()
    if any(k in title for k in TECH_KEYWORDS):
        return True

    tags = [str(t).lower() for t in (job.get("tags") or [])]
    if any(any(k in t for k in TECH_KEYWORDS) for t in tags):
        return True

    job_type = (job.get("job_type") or "").lower()
    if "engineer" in job_type or "developer" in job_type:
        return True

    return False


def _location_matches_africa(job: dict, include_worldwide: bool) -> bool:
    """Check candidate_required_location for Africa/EMEA or Worldwide/Anywhere/Global."""
    loc = (job.get("candidate_required_location") or "").lower()
    if not loc:
        return False

    if any(k in loc for k in AFRICA_KEYWORDS):
        return True

    # Many postings use 'EMEA' for Europe/Middle East/Africa
    if "emea" in loc:
        return True

    if include_worldwide and any(w in loc for w in WORLDWIDE_TERMS):
        return True

    return False


# --- Scraper -----------------------------------------------------------------

def scrape_remotive(include_worldwide: bool = True):
    """
    Fetch Remotive jobs and filter to 'tech' + Africa/EMEA.
    Set include_worldwide=False to exclude 'Worldwide/Anywhere/Global' roles.
    """
    url = "https://remotive.com/api/remote-jobs"

    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print("⚠️ Remotive request timed out")
        return []
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching Remotive jobs: {e}")
        return []

    payload = resp.json()
    raw_jobs = payload.get("jobs", [])
    results = []

    tech_count = 0
    loc_count = 0

    for job in raw_jobs:
        if not _is_tech(job):
            continue
        tech_count += 1

        if not _location_matches_africa(job, include_worldwide=include_worldwide):
            continue
        loc_count += 1

        # Clean description to a short summary
        raw_desc = job.get("description", "")
        summary = ""
        if raw_desc:
            soup = BeautifulSoup(raw_desc, "html.parser")
            summary = soup.get_text(" ", strip=True)[:200] + "..."

        results.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "summary": summary,
            "url": job.get("url"),
            "logo": job.get("company_logo_url"),
            "source": "remotive",  # keep lowercase to match your filters
        })

    print(
        f"✅ Remotive: {len(results)} Africa/EMEA (incl_worldwide={include_worldwide}) "
        f"out of {len(raw_jobs)} total; tech-matched={tech_count}, loc-matched={loc_count}"
    )
    return results
