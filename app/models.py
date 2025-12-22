"""Data models for parsed lead information."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class ContactInfo(BaseModel):
    """Contact information for a company representative."""
    name: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    website: Optional[str] = None


class ProjectInfo(BaseModel):
    """Construction project details."""
    project_name: Optional[str] = None
    dr_number: Optional[str] = None
    action_stage: Optional[str] = None
    bid_date: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    valuation: Optional[str] = None
    project_type: Optional[str] = None
    delivery_system: Optional[str] = None
    status: Optional[str] = None
    target_start_date: Optional[str] = None
    contract_number: Optional[str] = None
    owner_type: Optional[str] = None
    type_of_work: Optional[str] = None
    description: Optional[str] = None


class ParsedLeadData(BaseModel):
    """Complete parsed lead data from document."""
    project_info: ProjectInfo
    owner_contact: Optional[ContactInfo] = None
    architect_contact: Optional[ContactInfo] = None
    engineer_contacts: List[ContactInfo] = Field(default_factory=list)
    other_contacts: List[ContactInfo] = Field(default_factory=list)
    source: str = "Document Upload"
    parsed_at: datetime = Field(default_factory=datetime.now)


class ZohoLead(BaseModel):
    """ZOHO CRM Lead structure."""
    First_Name: Optional[str] = None
    Last_Name: str
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Mobile: Optional[str] = None
    Company: Optional[str] = None
    Title: Optional[str] = None
    Lead_Source: str = "Document Upload"
    Lead_Status: str = "New"
    Street: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Zip_Code: Optional[str] = None
    Country: Optional[str] = "USA"
    Website: Optional[str] = None
    Description: Optional[str] = None

    # Custom fields for project data
    Annual_Revenue: Optional[str] = None  # We'll use this for project valuation
    Industry: Optional[str] = None  # We'll use this for project type

    class Config:
        populate_by_name = True
