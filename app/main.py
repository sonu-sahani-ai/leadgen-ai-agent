from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.scraper import get_leads
from app.qualifier import qualify_lead
from app.scorer import save_lead
from app.database import Base, engine, SessionLocal
from app.models import Lead

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Jinja2 templates
templates = Jinja2Templates(directory="templates")


# HOME ROUTE - HTML Page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = SessionLocal()
    leads = db.query(Lead).all()  # Show all leads initially
    return templates.TemplateResponse("index.html", {"request": request, "leads": leads})


# RUN AGENT ROUTE - Scrape & Save Leads
@app.get("/run-agent")
def run_agent():
    leads = get_leads()

    for lead in leads:
        score = qualify_lead(lead["name"], lead["website"])
        save_lead(
            name=lead["name"],
            website=lead["website"],
            email=lead["email"],
            score=score
        )

    return {"status": "Agent completed successfully"}


# SEARCH LEADS ROUTE - Filter by clinic type & location
@app.get("/search-leads")
def search_leads(clinic: str = Query(...), location: str = Query(...)):
    db = SessionLocal()
    
    # Filter leads by name or website (adjust if you have location field)
    leads = db.query(Lead).filter(
        Lead.name.ilike(f"%{clinic}%"),
        Lead.website.ilike(f"%{location}%")
    ).all()

    result = []
    for lead in leads:
        result.append({
            "name": lead.name,
            "website": lead.website,
            "email": lead.email,
            "score": lead.score
        })

    return result


# VIEW LEADS ROUTE - JSON output
@app.get("/leads")
def view_leads():
    db = SessionLocal()
    leads = db.query(Lead).all()

    result = []
    for lead in leads:
        result.append({
            "name": lead.name,
            "website": lead.website,
            "email": lead.email,
            "score": lead.score
        })

    return result
