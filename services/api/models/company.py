from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from typing import Optional, List, Dict, Any

from .base import Base

class Company(Base):
    """Company model representing a client company"""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    website = Column(String)
    description = Column(String)
    
    # Revenue and metrics
    monthly_revenue = Column(Float)
    total_leads = Column(Integer)
    conversion_rate = Column(Float)
    customer_satisfaction = Column(Float)
    
    # Contact information
    contact_email = Column(String)
    contact_phone = Column(String)
    address = Column(String)
    
    # Additional metadata
    employee_count = Column(Integer)
    founded_year = Column(Integer)
    market_share = Column(Float)
    
    # Status
    is_active = Column(Boolean, default=False)  # Whether the company page is published
    
    # JSON fields for flexible data storage
    metrics = Column(JSONB)  # For storing various performance metrics
    settings = Column(JSONB)  # For storing company-specific settings
    integrations = Column(JSONB)  # For storing integration configurations
    
    # Relationships
    revenue_engines = relationship("RevenueEngine", back_populates="company", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="company", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="company", cascade="all, delete-orphan")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class RevenueEngine(Base):
    """Revenue Engine model representing a company's revenue generation system"""
    __tablename__ = "revenue_engines"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # e.g., "Sales", "Marketing", "Combined"
    status = Column(String, nullable=False)  # e.g., "Active", "Paused", "In Setup"
    configuration = Column(JSONB)  # Stores engine-specific configuration
    performance_metrics = Column(JSONB)  # Stores performance data
    
    # Relationships
    company = relationship("Company", back_populates="revenue_engines")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Contact(Base):
    """Contact model for CRM functionality"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    position = Column(String)
    status = Column(String, nullable=False)  # e.g., "Lead", "Prospect", "Customer"
    deal_value = Column(Float)
    pipeline_stage = Column(String, nullable=False)
    notes = Column(Text)
    meta_data = Column(JSONB)  # Changed from metadata to meta_data
    
    # Relationships
    company = relationship("Company", back_populates="contacts")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    """Task model for roadmap and project management"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False)  # e.g., "Planned", "In Progress", "Completed"
    priority = Column(String, nullable=False)  # e.g., "High", "Medium", "Low"
    due_date = Column(DateTime)
    assigned_to = Column(String)
    progress = Column(Float, nullable=False, default=0.0)
    category = Column(String)
    dependencies = Column(JSONB)  # Store task dependencies
    meta_data = Column(JSONB)  # Changed from metadata to meta_data
    
    # Relationships
    company = relationship("Company", back_populates="tasks")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Analytics(Base):
    """Analytics model for storing company performance data"""
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    category = Column(String, nullable=False)  # e.g., "Revenue", "Leads", "Conversion"
    timestamp = Column(DateTime, nullable=False)
    meta_data = Column(JSONB)  # Changed from metadata to meta_data
    
    # Relationships
    company = relationship("Company", back_populates="analytics")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 