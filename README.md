# 🌍 Multi Job Scraper

A Flask-based job aggregator that scrapes remote job listings from multiple sources and serves them through an API.  
The frontend is a simple Bootstrap-powered UI that lets users browse jobs with infinite scroll (Load More button).

---



---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/multi-job-scraper.git
cd multi-job-scraper
2. Create a virtual environment
bash
Copy code
python -m venv .venv
Activate it:

Windows (PowerShell)

bash
Copy code
.venv\Scripts\Activate
Mac/Linux

bash
Copy code
source .venv/bin/activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Run the app
bash
Copy code
python app.py
Open your browser and visit 👉 http://127.0.0.1:5000

📡 API Usage
Endpoint:

bash
Copy code
GET /api/jobs?page=1&per_page=12
Example response:

json
Copy code
{
  "page": 1,
  "per_page": 12,
  "jobs": [
    {
      "title": "Software Engineer",
      "company": "Tech Inc",
      "summary": "Work on cutting-edge remote projects...",
      "url": "https://example.com/job/software-engineer",
      "source": "remoteok",
      "logo": "https://example.com/logo.png"
    }
  ]
}
📂 Project Structure
pgsql
Copy code
multi-job-scraper/
│── scrapers/
│   ├── wwr.py
│   ├── remoteok.py
│   ├── remotive.py
│   ├── trulyremote.py
│── templates/
│   └── index.html
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
🛠 Tech Stack
Backend: Python, Flask

Frontend: HTML, Bootstrap 5, JavaScript

Scraping: Requests, BeautifulSoup


PS if the req installation didnt work install them separately and

python -m pip install lxml
        
