from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from scrapers.wwr import scrape_wwr
from scrapers.remoteok import scrape_remoteok
from scrapers.remotive import scrape_remotive
from scrapers.trulyremote import scrape_trulyremote

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
    return render_template("index.html")


@app.route("/api/jobs")
def get_jobs():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    source = request.args.get("source")  # 👈 optional filter

    jobs = []

    if source and source in all_jobs:
        # return only jobs from one source
        start = (page - 1) * per_page
        end = start + per_page
        jobs = all_jobs[source][start:end]
        total = len(all_jobs[source])
    else:
        # mix jobs fairly across all sources
        combined = []
        max_len = max(len(v) for v in all_jobs.values() if v)

        for i in range(max_len):
            for s in all_jobs:
                if i < len(all_jobs[s]):
                    combined.append(all_jobs[s][i])

        total = len(combined)
        start = (page - 1) * per_page
        end = start + per_page
        jobs = combined[start:end]

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
