# scrapers/trulyremote.py
import requests

BASE_URL = "https://trulyremote.co/api/getListing"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "https://trulyremote.co/",
}


def _first_or_str(x):
    """Return first element if list, else the value or empty string."""
    if isinstance(x, list):
        return x[0] if x else ""
    return x or ""


def _regions_from_fields(fields):
    """Combine listingRegions (list) and companyRegions (comma string) into a normalized list."""
    regions = []
    lr = fields.get("listingRegions") or []
    if isinstance(lr, list):
        regions.extend([str(r).strip() for r in lr if r])

    cr = fields.get("companyRegions")
    if isinstance(cr, str):
        regions.extend([s.strip() for s in cr.split(",") if s.strip()])

    # de-duplicate & keep only non-empty
    return list({r for r in regions if r})


def _is_africa(fields):
    regions = [r.lower() for r in _regions_from_fields(fields)]
    return "africa" in regions


def scrape_trulyremote(category="Development"):
    """Fetch jobs from TrulyRemote API. Filter for Africa region."""
    payload = {"locations": [], "category": [category]}

    try:
        resp = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=20)
        print("TrulyRemote status:", resp.status_code)
        resp.raise_for_status()
        data = resp.json()

        # Airtable-style: {"records": [{"id": "...","fields": {...}}, ...]}
        records = data.get("records", data)
        if not isinstance(records, list):
            print("DEBUG: Unexpected response shape:", type(records))
            return []

        jobs = []
        total = 0
        for item in records:
            fields = item.get("fields", item)
            total += 1

            # Only keep Africa jobs
            if not _is_africa(fields):
                continue

            title = fields.get("role") or fields.get("title") or ""
            company = _first_or_str(fields.get("companyName"))
            logo = _first_or_str(fields.get("companyLogoURL"))
            url = fields.get("roleApplyURL") or fields.get("listingURL") or "#"
            summary = (fields.get("listingSummary") or "").strip()
            date = fields.get("publishDate") or fields.get("createdOn") or ""

            jobs.append({
                "title": title,
                "company": company,
                "logo": logo,
                "url": url,
                "summary": summary,
                "date": date,
                "source": "trulyremote"
            })

        print(f"TrulyRemote: Found {len(jobs)} Africa jobs out of {total} total.")
        jobs.sort(key=lambda j: j["date"] or "", reverse=True)
        return jobs

    except Exception as e:
        print("ERROR fetching TrulyRemote jobs:", repr(e))
        return []
