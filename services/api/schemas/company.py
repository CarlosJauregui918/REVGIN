from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    industry: str
    website: Optional[str] = None
    description: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    employee_count: Optional[int] = None
    founded_year: Optional[int] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    industry: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None
    integrations: Optional[Dict[str, Any]] = None

class CompanyInDB(CompanyBase):
    id: int
    monthly_revenue: float
    total_leads: int
    conversion_rate: float
    customer_satisfaction: float
    market_share: float
    metrics: Optional[Dict[str, Any]]
    settings: Optional[Dict[str, Any]]
    integrations: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RevenueEngineBase(BaseModel):
    name: str
    type: str
    status: str
    configuration: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class RevenueEngineCreate(RevenueEngineBase):
    company_id: int

class RevenueEngineUpdate(RevenueEngineBase):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None

class RevenueEngineInDB(RevenueEngineBase):
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    position: Optional[str] = None
    status: str
    deal_value: Optional[float] = 0.0
    pipeline_stage: str
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ContactCreate(ContactBase):
    company_id: int

class ContactUpdate(ContactBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    pipeline_stage: Optional[str] = None

class ContactInDB(ContactBase):
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    progress: float = 0.0
    category: Optional[str] = None
    dependencies: Optional[List[int]] = None
    metadata: Optional[Dict[str, Any]] = None

class TaskCreate(TaskBase):
    company_id: int

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    progress: Optional[float] = None

class TaskInDB(TaskBase):
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnalyticsBase(BaseModel):
    metric_name: str
    metric_value: float
    category: str
    metadata: Optional[Dict[str, Any]] = None

class AnalyticsCreate(AnalyticsBase):
    company_id: int

class AnalyticsInDB(AnalyticsBase):
    id: int
    company_id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 