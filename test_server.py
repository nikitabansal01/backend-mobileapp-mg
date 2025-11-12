"""
Simple test server for hormone scoring API
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append('/Users/mohanganesh/Auvra1/AuvraJuly15')

from app.services.hormone_scoring_service import HormoneScoringService
from app.services.root_cause_engine import RootCauseEngine

app = FastAPI(title="Hormone Scoring Test API")


class QuestionData(BaseModel):
    period_description: Optional[str] = None
    cycle_length: Optional[str] = None
    period_concerns: Optional[List[str]] = []
    body_concerns: Optional[List[str]] = []
    mood_concerns: Optional[List[str]] = []
    hair_concerns: Optional[List[str]] = []
    skin_concerns: Optional[List[str]] = []
    sleep_concerns: Optional[List[str]] = []
    symptom_others: Optional[str] = None
    family_history: Optional[List[str]] = []
    family_others: Optional[str] = None
    sleep_hours: Optional[str] = None
    stress_level: Optional[str] = None
    workout_frequency: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "Hormone Scoring Test API",
        "endpoints": {
            "POST /analyze": "Analyze hormone imbalances"
        }
    }


@app.post("/analyze")
async def analyze_hormones(data: QuestionData):
    """Analyze hormone imbalances from survey data"""
    
    # Convert to dict
    user_data = data.dict()
    
    # Get root cause analysis (this internally calculates hormone scores)
    analysis = await RootCauseEngine.analyze_hormone_imbalance(user_data)
    
    # Extract scores from analysis
    hormone_scores = analysis.get("hormone_scores", {})
    
    return {
        "hormone_scores": hormone_scores,
        "analysis": analysis,
        "gemini_api_active": hormone_scores.get("confidence", 0) > 0
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Hormone Scoring Test API on http://localhost:8000")
    print("📋 API Docs available at http://localhost:8000/docs")
    print("✅ Gemini API configured from .env file")
    uvicorn.run(app, host="0.0.0.0", port=8000)
