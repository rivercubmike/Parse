"""ZOHO CRM API client for creating leads."""
import requests
from typing import Dict, Optional
from app.config import settings
from app.models import ZohoLead, ParsedLeadData, ContactInfo


class ZohoClient:
    """Client for interacting with ZOHO CRM API."""

    def __init__(self):
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[int] = None

    def _get_access_token(self) -> str:
        """
        Get or refresh access token for ZOHO CRM API.

        Returns:
            Access token string
        """
        # Use refresh token to get access token
        url = f"https://accounts.zoho.{settings.ZOHO_REGION.lower()}/oauth/v2/token"

        params = {
            "refresh_token": settings.ZOHO_REFRESH_TOKEN,
            "client_id": settings.ZOHO_CLIENT_ID,
            "client_secret": settings.ZOHO_CLIENT_SECRET,
            "grant_type": "refresh_token"
        }

        response = requests.post(url, params=params)
        response.raise_for_status()

        data = response.json()
        self.access_token = data["access_token"]
        self.token_expires_at = data.get("expires_in")

        return self.access_token

    def create_lead(self, lead_data: ZohoLead) -> Dict:
        """
        Create a lead in ZOHO CRM.

        Args:
            lead_data: ZohoLead object with lead information

        Returns:
            Response from ZOHO API
        """
        token = self._get_access_token()

        url = f"{settings.ZOHO_API_DOMAIN}/crm/v2/Leads"

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}",
            "Content-Type": "application/json"
        }

        # Convert Pydantic model to dict and remove None values
        lead_dict = {k: v for k, v in lead_data.model_dump().items() if v is not None}

        payload = {
            "data": [lead_dict]
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()

    def convert_to_zoho_lead(self, parsed_data: ParsedLeadData) -> ZohoLead:
        """
        Convert ParsedLeadData to ZohoLead format.

        Args:
            parsed_data: Parsed data from document

        Returns:
            ZohoLead object ready for API submission
        """
        # Use owner contact as primary, fallback to architect
        primary_contact = parsed_data.owner_contact or parsed_data.architect_contact

        if not primary_contact:
            # If no contacts, create a minimal lead with project info only
            primary_contact = ContactInfo(
                name="Unknown Contact",
                company=parsed_data.project_info.project_name or "Unknown Company"
            )

        # Split name into first and last
        name_parts = (primary_contact.name or "Unknown Contact").split(maxsplit=1)
        first_name = name_parts[0] if len(name_parts) > 0 else None
        last_name = name_parts[1] if len(name_parts) > 1 else name_parts[0]

        # Build description with all project and contact details
        description_parts = []

        if parsed_data.project_info.project_name:
            description_parts.append(f"Project: {parsed_data.project_info.project_name}")

        if parsed_data.project_info.dr_number:
            description_parts.append(f"DR#: {parsed_data.project_info.dr_number}")

        if parsed_data.project_info.contract_number:
            description_parts.append(f"Contract: {parsed_data.project_info.contract_number}")

        if parsed_data.project_info.status:
            description_parts.append(f"Status: {parsed_data.project_info.status}")

        if parsed_data.project_info.description:
            description_parts.append(f"\nProject Details:\n{parsed_data.project_info.description}")

        # Add other contacts to description
        if parsed_data.architect_contact and parsed_data.architect_contact != primary_contact:
            description_parts.append(
                f"\nArchitect: {parsed_data.architect_contact.name} - "
                f"{parsed_data.architect_contact.company} - "
                f"{parsed_data.architect_contact.email or 'N/A'}"
            )

        for eng in parsed_data.engineer_contacts:
            description_parts.append(
                f"\n{eng.title or 'Engineer'}: {eng.name} - {eng.company} - {eng.email or 'N/A'}"
            )

        description = "\n".join(description_parts)

        # Create ZOHO lead
        zoho_lead = ZohoLead(
            First_Name=first_name,
            Last_Name=last_name,
            Email=primary_contact.email,
            Phone=primary_contact.phone,
            Company=primary_contact.company or parsed_data.project_info.project_name or "Unknown",
            Title=primary_contact.title,
            Lead_Source=parsed_data.source,
            Lead_Status="New",
            Street=parsed_data.project_info.address,
            City=parsed_data.project_info.city,
            State=parsed_data.project_info.state,
            Zip_Code=parsed_data.project_info.zip_code,
            Website=primary_contact.website,
            Description=description,
            Annual_Revenue=parsed_data.project_info.valuation,  # Project value
            Industry=parsed_data.project_info.project_type,
        )

        return zoho_lead
