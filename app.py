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
    source = request.args.get("source")  # 👈 new filter param

    jobs = []

    if source and source in all_jobs:
        # return only jobs from one source
        start = (page - 1) * per_page
        end = start + per_page
        jobs = all_jobs[source][start:end]
        total = len(all_jobs[source])
    else:
        # combine all jobs equally across sources
        sources = list(all_jobs.keys())
        while len(jobs) < per_page:
            added_any = False
            for s in sources:
                if all_jobs[s]:
                    jobs.append(all_jobs[s].pop(0))
                    added_any = True
                if len(jobs) >= per_page:
                    break
            if not added_any:
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
