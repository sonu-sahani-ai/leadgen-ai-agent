from fastapi import FastAPI
from app.scraper import get_leads
from app.qualifier import qualify_lead
from app.scorer import save_lead
from app.database import Base, engine, SessionLocal
from app.models import Lead

# create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# HOME ROUTE
@app.get("/")
def home():
    return {"message": "LeadGen AI Agent is running"}


# RUN AGENT ROUTE
@app.get("/run-agent")
def run_agent():

    try:

        leads = get_leads()

        for lead in leads:

            # TEMP SAFE SCORE (no AI call)
            score = 5

            save_lead(
                name=lead["name"],
                website=lead["website"],
                email=lead["email"],
                score=score
            )

        return {"status": "Agent completed successfully"}

    except Exception as e:

        return {"error": str(e)}

# VIEW LEADS ROUTE
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
