from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from datetime import datetime, timedelta

from api.core.database import get_db
from api.models.company import Company, RevenueEngine, Contact, Task, Analytics
from api.schemas.company import (
    CompanyCreate, CompanyUpdate, CompanyInDB,
    RevenueEngineCreate, RevenueEngineInDB,
    ContactCreate, ContactInDB,
    TaskCreate, TaskInDB,
    AnalyticsCreate, AnalyticsInDB
)
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for request/response
class CompanyBase(BaseModel):
    name: str
    industry: str
    website: Optional[str] = None
    description: Optional[str] = None
    monthly_revenue: Optional[float] = None
    total_leads: Optional[int] = None
    conversion_rate: Optional[float] = None
    customer_satisfaction: Optional[float] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    employee_count: Optional[int] = None
    founded_year: Optional[int] = None
    market_share: Optional[float] = None

class CompanyResponse(CompanyBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Company endpoints
@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Create a new company.
    """
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/", response_model=List[CompanyResponse])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve all companies.
    """
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@router.get("/{company_id}", response_model=CompanyResponse)
def read_company(
    company_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get company by ID.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Update a company.
    """
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for field, value in company.dict(exclude_unset=True).items():
        setattr(db_company, field, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a company.
    """
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}

@router.put("/{company_id}/publish")
def publish_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Publish a company's page.
    """
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_company.is_active = True
    db.commit()
    return {"message": "Company published successfully"}

@router.put("/{company_id}/unpublish")
def unpublish_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Unpublish a company's page.
    """
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_company.is_active = False
    db.commit()
    return {"message": "Company unpublished successfully"}

# Revenue Engine endpoints
@router.post("/{company_id}/revenue-engines/", response_model=RevenueEngineInDB)
def create_revenue_engine(
    company_id: int,
    revenue_engine: RevenueEngineCreate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_revenue_engine = RevenueEngine(**revenue_engine.model_dump())
    db.add(db_revenue_engine)
    db.commit()
    db.refresh(db_revenue_engine)
    return db_revenue_engine

@router.get("/{company_id}/revenue-engines/", response_model=List[RevenueEngineInDB])
def list_revenue_engines(
    company_id: int,
    db: Session = Depends(get_db)
):
    return db.query(RevenueEngine).filter(RevenueEngine.company_id == company_id).all()

# Analytics endpoints
@router.post("/{company_id}/analytics/")
def create_analytics(
    company_id: int,
    metric_name: str,
    metric_value: float,
    category: str,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_analytics = Analytics(
        company_id=company_id,
        metric_name=metric_name,
        metric_value=metric_value,
        category=category
    )
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    return db_analytics

@router.get("/{company_id}/analytics/")
def get_company_analytics(
    company_id: int,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Analytics).filter(Analytics.company_id == company_id)
    
    if category:
        query = query.filter(Analytics.category == category)
    if start_date:
        query = query.filter(Analytics.timestamp >= start_date)
    if end_date:
        query = query.filter(Analytics.timestamp <= end_date)
    
    return query.all()

@router.get("/{company_id}/analytics/summary")
def get_analytics_summary(
    company_id: int,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Calculate summary metrics
    total_revenue = db.query(Analytics).filter(
        Analytics.company_id == company_id,
        Analytics.category == "revenue",
        Analytics.timestamp >= datetime.utcnow() - timedelta(days=30)
    ).order_by(Analytics.timestamp.desc()).first()
    
    total_leads = db.query(Analytics).filter(
        Analytics.company_id == company_id,
        Analytics.category == "leads",
        Analytics.timestamp >= datetime.utcnow() - timedelta(days=30)
    ).order_by(Analytics.timestamp.desc()).first()
    
    return {
        "monthly_revenue": total_revenue.metric_value if total_revenue else 0,
        "total_leads": total_leads.metric_value if total_leads else 0,
        "conversion_rate": company.conversion_rate,
        "customer_satisfaction": company.customer_satisfaction
    }

# Task endpoints
@router.post("/{company_id}/tasks/", response_model=TaskInDB)
def create_task(
    company_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{company_id}/tasks/", response_model=List[TaskInDB])
def list_tasks(
    company_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.company_id == company_id)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    
    return query.order_by(Task.due_date.asc()).all()

# Contact endpoints
@router.post("/{company_id}/contacts/", response_model=ContactInDB)
def create_contact(
    company_id: int,
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/{company_id}/contacts/", response_model=List[ContactInDB])
def list_contacts(
    company_id: int,
    status: Optional[str] = None,
    pipeline_stage: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Contact).filter(Contact.company_id == company_id)
    
    if status:
        query = query.filter(Contact.status == status)
    if pipeline_stage:
        query = query.filter(Contact.pipeline_stage == pipeline_stage)
    
    return query.order_by(Contact.created_at.desc()).all() 