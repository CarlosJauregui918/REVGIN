from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Company(BaseModel):
    """Company model representing a client company"""
    __tablename__ = "companies"

    name = Column(String, index=True)
    industry = Column(String)
    website = Column(String)
    description = Column(String)
    
    # Revenue and metrics
    monthly_revenue = Column(Float, default=0.0)
    total_leads = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    customer_satisfaction = Column(Float, default=0.0)
    
    # Contact information
    contact_email = Column(String)
    contact_phone = Column(String)
    address = Column(String)
    
    # Additional metadata
    employee_count = Column(Integer)
    founded_year = Column(Integer)
    market_share = Column(Float, default=0.0)
    
    # JSON fields for flexible data storage
    metrics = Column(JSON)  # For storing various performance metrics
    settings = Column(JSON)  # For storing company-specific settings
    integrations = Column(JSON)  # For storing integration configurations
    
    # Relationships
    revenue_engines = relationship("RevenueEngine", back_populates="company")
    contacts = relationship("Contact", back_populates="company")
    tasks = relationship("Task", back_populates="company")
    analytics = relationship("Analytics", back_populates="company")

class RevenueEngine(BaseModel):
    """Revenue Engine model representing a company's revenue generation system"""
    __tablename__ = "revenue_engines"

    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String)
    type = Column(String)  # e.g., "Sales", "Marketing", "Combined"
    status = Column(String)  # e.g., "Active", "Paused", "In Setup"
    configuration = Column(JSON)  # Stores engine-specific configuration
    performance_metrics = Column(JSON)  # Stores performance data
    
    # Relationships
    company = relationship("Company", back_populates="revenue_engines")

class Contact(BaseModel):
    """Contact model for CRM functionality"""
    __tablename__ = "contacts"

    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    position = Column(String)
    status = Column(String)  # e.g., "Lead", "Prospect", "Customer"
    deal_value = Column(Float, default=0.0)
    pipeline_stage = Column(String)
    notes = Column(String)
    metadata = Column(JSON)  # For additional contact information
    
    # Relationships
    company = relationship("Company", back_populates="contacts")

class Task(BaseModel):
    """Task model for roadmap and project management"""
    __tablename__ = "tasks"

    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String)
    description = Column(String)
    status = Column(String)  # e.g., "Planned", "In Progress", "Completed"
    priority = Column(String)  # e.g., "High", "Medium", "Low"
    due_date = Column(DateTime)
    assigned_to = Column(String)
    progress = Column(Float, default=0.0)
    category = Column(String)
    dependencies = Column(JSON)  # Store task dependencies
    metadata = Column(JSON)  # For additional task data
    
    # Relationships
    company = relationship("Company", back_populates="tasks")

class Analytics(BaseModel):
    """Analytics model for storing company performance data"""
    __tablename__ = "analytics"

    company_id = Column(Integer, ForeignKey("companies.id"))
    metric_name = Column(String)
    metric_value = Column(Float)
    timestamp = Column(DateTime)
    category = Column(String)  # e.g., "Revenue", "Leads", "Conversion"
    metadata = Column(JSON)  # For additional analytics data
    
    # Relationships
    company = relationship("Company", back_populates="analytics") 