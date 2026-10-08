from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from scrapers.wwr import scrape_wwr
from scrapers.remoteok import scrape_remoteok
from scrapers.remotive import scrape_remotive
from scrapers.trulyremote import scrape_trulyremote


app = Flask(__name__)
CORS(app)


def scrape_all_jobs():
    """
    Run all scrapers concurrently.
    """

    scrapers = {
        "wwr": scrape_wwr,
        "remoteok": scrape_remoteok,
        "remotive": scrape_remotive,
        "trulyremote": scrape_trulyremote,
    }

    all_jobs = {
        "wwr": [],
        "remoteok": [],
        "remotive": [],
        "trulyremote": [],
    }

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_source = {
            executor.submit(scraper): source
            for source, scraper in scrapers.items()
        }

        for future in as_completed(future_to_source):
            source = future_to_source[future]

            try:
                jobs = future.result()

                if isinstance(jobs, list):
                    all_jobs[source] = jobs

                    print(
                        f"[SCRAPER] {source}: "
                        f"{len(jobs)} jobs loaded"
                    )

            except Exception as error:
                print(
                    f"[SCRAPER ERROR] {source}: {error}"
                )

                all_jobs[source] = []

    return all_jobs


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/jobs")
def get_jobs():
    try:
        page = max(
            int(request.args.get("page", 1)),
            1
        )

        per_page = max(
            min(
                int(request.args.get("per_page", 20)),
                100
            ),
            1
        )

    except ValueError:
        return jsonify({
            "error": "page and per_page must be numbers"
        }), 400

    source = request.args.get("source")

    # Run all scrapers
    all_jobs = scrape_all_jobs()

    # Filter by source
    if source:
        if source not in all_jobs:
            return jsonify({
                "error": "Invalid source",
                "available_sources": list(all_jobs.keys())
            }), 400

        jobs = all_jobs[source]

    # Combine all sources
    else:
        combined = []

        max_len = max(
            (len(jobs) for jobs in all_jobs.values()),
            default=0
        )

        for index in range(max_len):
            for source_name in all_jobs:
                source_jobs = all_jobs[source_name]

                if index < len(source_jobs):
                    combined.append(
                        source_jobs[index]
                    )

        jobs = combined

    # Pagination
    total = len(jobs)

    start = (page - 1) * per_page
    end = start + per_page

    paginated_jobs = jobs[start:end]

    total_pages = (
        (total + per_page - 1) // per_page
        if total > 0
        else 0
    )

    return jsonify({
        "jobs": paginated_jobs,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "sources": {
            source_name: len(source_jobs)
            for source_name, source_jobs in all_jobs.items()
        }
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )