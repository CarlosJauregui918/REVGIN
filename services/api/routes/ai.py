from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta
import openai

from ..core.database import get_db
from ..models.company import Company, Analytics, Task
from pydantic import BaseModel

router = APIRouter()

class InsightRequest(BaseModel):
    company_id: int
    timeframe_days: int = 30
    categories: List[str] = ["revenue", "leads", "tasks", "engagement"]

class RecommendationRequest(BaseModel):
    company_id: int
    focus_area: str
    current_goals: List[str]

class RoadmapRequest(BaseModel):
    company_id: int
    timeframe_months: int
    objectives: List[str]
    constraints: Dict[str, Any] = {}

def get_company_data(company_id: int, db: Session) -> Dict[str, Any]:
    """Gather relevant company data for AI analysis"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Get recent analytics
    recent_analytics = db.query(Analytics).filter(
        Analytics.company_id == company_id,
        Analytics.timestamp >= datetime.utcnow() - timedelta(days=30)
    ).all()

    # Get active tasks
    active_tasks = db.query(Task).filter(
        Task.company_id == company_id,
        Task.status.in_(["in_progress", "pending"])
    ).all()

    return {
        "company": {
            "name": company.name,
            "industry": company.industry,
            "monthly_revenue": company.monthly_revenue,
            "total_leads": company.total_leads,
            "conversion_rate": company.conversion_rate,
            "customer_satisfaction": company.customer_satisfaction,
        },
        "analytics": [
            {
                "category": a.category,
                "metric_name": a.metric_name,
                "metric_value": a.metric_value,
                "timestamp": a.timestamp
            }
            for a in recent_analytics
        ],
        "active_tasks": [
            {
                "title": t.title,
                "status": t.status,
                "priority": t.priority,
                "progress": t.progress
            }
            for t in active_tasks
        ]
    }

@router.post("/ai/insights")
async def generate_insights(
    request: InsightRequest,
    db: Session = Depends(get_db)
):
    """Generate AI-powered insights based on company data"""
    company_data = get_company_data(request.company_id, db)
    
    prompt = f"""
    Analyze the following company data and provide key insights:
    Company: {company_data['company']}
    Recent Analytics: {company_data['analytics']}
    Active Tasks: {company_data['active_tasks']}
    
    Focus on the following categories: {request.categories}
    Timeframe: Last {request.timeframe_days} days
    
    Provide insights on:
    1. Key trends and patterns
    2. Areas of improvement
    3. Notable achievements
    4. Potential risks or concerns
    """
    
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI business analyst specializing in revenue and growth analysis."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return {
        "insights": response.choices[0].message.content,
        "analyzed_at": datetime.utcnow(),
        "data_timeframe": {
            "start": datetime.utcnow() - timedelta(days=request.timeframe_days),
            "end": datetime.utcnow()
        }
    }

@router.post("/ai/recommendations")
async def generate_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Generate AI-powered recommendations for specific focus areas"""
    company_data = get_company_data(request.company_id, db)
    
    prompt = f"""
    Based on the following company data and goals, provide strategic recommendations:
    
    Company Information:
    {company_data['company']}
    
    Current Goals:
    {request.current_goals}
    
    Focus Area: {request.focus_area}
    
    Recent Performance:
    Analytics: {company_data['analytics']}
    Active Tasks: {company_data['active_tasks']}
    
    Provide specific, actionable recommendations for achieving the stated goals,
    focusing on {request.focus_area}.
    Include:
    1. Short-term actions (next 30 days)
    2. Medium-term strategies (1-3 months)
    3. Key metrics to track
    4. Potential challenges and mitigation strategies
    """
    
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI business strategist specializing in growth and optimization."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return {
        "recommendations": response.choices[0].message.content,
        "focus_area": request.focus_area,
        "generated_at": datetime.utcnow()
    }

@router.post("/ai/generate-roadmap")
async def generate_roadmap(
    request: RoadmapRequest,
    db: Session = Depends(get_db)
):
    """Generate an AI-powered strategic roadmap"""
    company_data = get_company_data(request.company_id, db)
    
    prompt = f"""
    Create a strategic roadmap based on the following information:
    
    Company Profile:
    {company_data['company']}
    
    Objectives:
    {request.objectives}
    
    Constraints:
    {request.constraints}
    
    Timeframe: {request.timeframe_months} months
    
    Current Status:
    Analytics: {company_data['analytics']}
    Active Tasks: {company_data['active_tasks']}
    
    Generate a detailed roadmap that includes:
    1. Key milestones and deliverables
    2. Resource requirements
    3. Dependencies and critical paths
    4. Risk assessment and mitigation strategies
    5. Success metrics and KPIs
    6. Timeline breakdown by month
    """
    
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI strategic planning expert specializing in business roadmap development."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return {
        "roadmap": response.choices[0].message.content,
        "timeframe": {
            "months": request.timeframe_months,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=30 * request.timeframe_months)
        },
        "generated_at": datetime.utcnow()
    } 