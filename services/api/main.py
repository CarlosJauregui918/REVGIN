from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class RoadmapRequest(BaseModel):
    company_name: str
    target_audience: str
    brand_voice: str
    goals: str

@app.post("/generate-roadmap")
async def generate_roadmap(data: RoadmapRequest):
    try:
        prompt = (
            f"Create a sales and marketing roadmap for {data.company_name}. "
            f"The target audience is {data.target_audience}. "
            f"The brand voice is {data.brand_voice}. "
            f"The company’s main goals are: {data.goals}. "
            f"Include top-of-funnel, middle-of-funnel, and bottom-of-funnel strategies."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )

        return {"roadmap": response.choices[0].message["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
