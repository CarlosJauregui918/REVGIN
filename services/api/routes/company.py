from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..core.database import get_db
from ..models.company import Company, RevenueEngine, Contact, Task, Analytics
from ..schemas.company import (
    CompanyCreate, CompanyUpdate, CompanyInDB,
    RevenueEngineCreate, RevenueEngineInDB,
    ContactCreate, ContactInDB,
    TaskCreate, TaskInDB,
    AnalyticsCreate, AnalyticsInDB
)

router = APIRouter()

@router.post("/companies/", response_model=CompanyInDB)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/companies/", response_model=List[CompanyInDB])
def list_companies(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    industry: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Company)
    
    if search:
        query = query.filter(Company.name.ilike(f"%{search}%"))
    if industry:
        query = query.filter(Company.industry == industry)
    
    return query.offset(skip).limit(limit).all()

@router.get("/companies/{company_id}", response_model=CompanyInDB)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/companies/{company_id}", response_model=CompanyInDB)
def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db)
):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for field, value in company_update.model_dump(exclude_unset=True).items():
        setattr(db_company, field, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}

# Revenue Engine endpoints
@router.post("/companies/{company_id}/revenue-engines/", response_model=RevenueEngineInDB)
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

@router.get("/companies/{company_id}/revenue-engines/", response_model=List[RevenueEngineInDB])
def list_revenue_engines(company_id: int, db: Session = Depends(get_db)):
    return db.query(RevenueEngine).filter(RevenueEngine.company_id == company_id).all()

# Analytics endpoints
@router.post("/companies/{company_id}/analytics/", response_model=AnalyticsInDB)
def create_analytics(
    company_id: int,
    analytics: AnalyticsCreate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_analytics = Analytics(**analytics.model_dump(), timestamp=datetime.utcnow())
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    return db_analytics

@router.get("/companies/{company_id}/analytics/", response_model=List[AnalyticsInDB])
def get_company_analytics(
    company_id: int,
    category: Optional[str] = None,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Analytics).filter(Analytics.company_id == company_id)
    
    if category:
        query = query.filter(Analytics.category == category)
    if start_date:
        query = query.filter(Analytics.timestamp >= start_date)
    if end_date:
        query = query.filter(Analytics.timestamp <= end_date)
    
    return query.order_by(Analytics.timestamp.desc()).all()

@router.get("/companies/{company_id}/analytics/summary")
def get_analytics_summary(company_id: int, db: Session = Depends(get_db)):
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
@router.post("/companies/{company_id}/tasks/", response_model=TaskInDB)
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

@router.get("/companies/{company_id}/tasks/", response_model=List[TaskInDB])
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
@router.post("/companies/{company_id}/contacts/", response_model=ContactInDB)
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

@router.get("/companies/{company_id}/contacts/", response_model=List[ContactInDB])
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