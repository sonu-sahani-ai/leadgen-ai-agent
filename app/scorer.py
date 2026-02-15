from app.database import SessionLocal
from app.models import Lead


def save_lead(name, website, email, score):

    db = SessionLocal()

    new_lead = Lead(
        name=name,
        website=website,
        email=email,
        score=score
    )

    db.add(new_lead)
    db.commit()
    db.close()
