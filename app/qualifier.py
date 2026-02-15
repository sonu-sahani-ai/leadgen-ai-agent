import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def qualify_lead(name, website):

    prompt = f"""
    Analyze this business:

    Name: {name}
    Website: {website}

    Rate from 1-10 how much they need digital marketing services.
    Only return number.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    score = int(response.choices[0].message.content.strip())

    return score
