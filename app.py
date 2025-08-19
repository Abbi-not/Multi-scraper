from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from scrapers.wwr import scrape_wwr
from scrapers.remoteok import scrape_remoteok
from scrapers.remotive import scrape_remotive
from scrapers.trulyremote import scrape_trulyremote
import random

app = Flask(__name__)
CORS(app)

# cache all jobs in memory
all_jobs = {
    "wwr": [],
    "remoteok": [],
    "remotive": [],
    "trulyremote": []
}

@app.route("/")
def home():
    return render_template("index.html")   # 👈 instead of plain text

@app.route("/api/jobs")
def get_jobs():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))

    # Combine all jobs equally across sources
    jobs = []
    sources = list(all_jobs.keys())
    for i in range(per_page):
        for source in sources:
            if all_jobs[source]:
                job = all_jobs[source].pop(0)  # take one from each
                jobs.append(job)
        if len(jobs) >= per_page:
            break

    total = sum(len(v) for v in all_jobs.values()) + len(jobs)

    return jsonify({"jobs": jobs, "total": total})

if __name__ == "__main__":
    # load jobs once on startup
    all_jobs["wwr"] = scrape_wwr()
    print(f"[CACHE] weworkremotely: {len(all_jobs['wwr'])} jobs loaded.")

    all_jobs["remoteok"] = scrape_remoteok()
    print(f"[CACHE] remoteok: {len(all_jobs['remoteok'])} jobs loaded.")

    all_jobs["remotive"] = scrape_remotive()
    print(f"[CACHE] remotive: {len(all_jobs['remotive'])} jobs loaded.")

    all_jobs["trulyremote"] = scrape_trulyremote()
    print(f"[CACHE] trulyremote: {len(all_jobs['trulyremote'])} jobs loaded.")

    app.run(debug=True)
