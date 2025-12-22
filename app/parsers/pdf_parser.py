"""PDF parser for construction bid documents."""
import re
import pdfplumber
from typing import Optional, List
from app.models import ParsedLeadData, ProjectInfo, ContactInfo


class PDFParser:
    """Parser for construction bid PDFs (Dodge Data & Analytics format)."""

    def __init__(self):
        self.text = ""

    def parse(self, file_path: str) -> ParsedLeadData:
        """
        Parse a PDF file and extract lead data.

        Args:
            file_path: Path to the PDF file

        Returns:
            ParsedLeadData object with extracted information
        """
        # Extract text from PDF
        with pdfplumber.open(file_path) as pdf:
            self.text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        # Parse different sections
        project_info = self._parse_project_info()
        owner_contact = self._parse_contact("OWNER")
        architect_contact = self._parse_contact("ARCHITECT")
        engineer_contacts = self._parse_engineer_contacts()

        return ParsedLeadData(
            project_info=project_info,
            owner_contact=owner_contact,
            architect_contact=architect_contact,
            engineer_contacts=engineer_contacts,
            source="PDF Upload"
        )

    def _parse_project_info(self) -> ProjectInfo:
        """Extract project information from the PDF text."""
        info = ProjectInfo()

        # Extract project name (first line typically)
        lines = self.text.split('\n')
        if lines:
            info.project_name = lines[0].strip()

        # DR Number
        dr_match = re.search(r'DR#\s*(\S+)', self.text)
        if dr_match:
            info.dr_number = dr_match.group(1)

        # Action Stage
        action_match = re.search(r'Action Stage\s*\n\s*(.+?)(?:\n|$)', self.text)
        if action_match:
            info.action_stage = action_match.group(1).strip()

        # Bid Date
        bid_match = re.search(r'Bid Date.*?\n\s*(\d{2}/\d{2}/\d{4})', self.text, re.DOTALL)
        if bid_match:
            info.bid_date = bid_match.group(1)

        # Address
        address_match = re.search(r'Address.*?\n\s*(.+?)\n\s*(.+?)\s+(USA)', self.text, re.DOTALL)
        if address_match:
            street = address_match.group(1).strip()
            city_state_zip = address_match.group(2).strip()
            info.address = street

            # Parse city, state, zip
            city_state_match = re.match(r'(.+?),\s*([A-Z]{2})\s+(\d{5})', city_state_zip)
            if city_state_match:
                info.city = city_state_match.group(1)
                info.state = city_state_match.group(2)
                info.zip_code = city_state_match.group(3)

        # Valuation
        val_match = re.search(r'Valuation.*?\n\s*\$?([\d,]+\s*-\s*\$?[\d,]+)', self.text, re.DOTALL)
        if val_match:
            info.valuation = val_match.group(1)

        # Project Type
        type_match = re.search(r'Project Type\s+(.+)', self.text)
        if type_match:
            info.project_type = type_match.group(1).strip()

        # Project Delivery System
        delivery_match = re.search(r'Project Delivery System\s+(.+)', self.text)
        if delivery_match:
            info.delivery_system = delivery_match.group(1).strip()

        # Status
        status_match = re.search(r'Status\s+(.+?)(?:\n\n|\nTarget)', self.text, re.DOTALL)
        if status_match:
            info.status = status_match.group(1).strip()

        # Target Start Date
        start_match = re.search(r'Target Start Date\s+(\d{2}/\d{2}/\d{4})', self.text)
        if start_match:
            info.target_start_date = start_match.group(1)

        # Contract Number
        contract_match = re.search(r'Contract Number\s+(\S+)', self.text)
        if contract_match:
            info.contract_number = contract_match.group(1)

        # Owner Type
        owner_type_match = re.search(r'Owner Type\s+(.+)', self.text)
        if owner_type_match:
            info.owner_type = owner_type_match.group(1).strip()

        # Type of Work
        work_match = re.search(r'Type Of Work\s+(.+)', self.text)
        if work_match:
            info.type_of_work = work_match.group(1).strip()

        # Description (Additional Features)
        desc_match = re.search(r'Additional Features\s+(.+?)(?:\n\n|Latest Updates)', self.text, re.DOTALL)
        if desc_match:
            info.description = desc_match.group(1).strip()

        return info

    def _parse_contact(self, contact_type: str) -> Optional[ContactInfo]:
        """
        Parse a specific contact type from the Companies section.

        Args:
            contact_type: Type of contact (e.g., "OWNER", "ARCHITECT")

        Returns:
            ContactInfo object or None if not found
        """
        # Find the section for this contact type
        pattern = rf'{contact_type}(?:\s*\([^)]+\))?\s*\n\s*(.+?)\n\s*(.+?)\s+Phone\s+([\d-]+)\s*\n\s*(.+?)\s+Fax\s+([\d-]+)\s*\n\s*(.+?)\s+Email\s+(\S*)'
        match = re.search(pattern, self.text, re.DOTALL)

        if not match:
            return None

        company = match.group(1).strip()
        contact_name = match.group(2).strip()
        phone = match.group(3).strip()
        address = match.group(4).strip()
        fax = match.group(5).strip()
        website = match.group(6).strip()
        email = match.group(7).strip() if match.group(7).strip() else None

        return ContactInfo(
            name=contact_name,
            company=company,
            phone=phone,
            fax=fax,
            email=email,
            address=address,
            website=website if website.startswith('http') else None
        )

    def _parse_engineer_contacts(self) -> List[ContactInfo]:
        """Parse all engineer contacts (Civil, Electrical, Mechanical, Structural)."""
        engineers = []
        engineer_types = ["CIVIL ENGINEER", "ELECTRICAL ENGINEER", "MECHANICAL ENGINEER", "STRUCTURAL ENGINEER"]

        for eng_type in engineer_types:
            contact = self._parse_contact(eng_type)
            if contact:
                contact.title = eng_type.title()
                engineers.append(contact)

        return engineers
