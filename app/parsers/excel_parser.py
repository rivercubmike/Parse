"""Excel parser for construction bid or lead data."""
import pandas as pd
from typing import List, Optional
from app.models import ParsedLeadData, ProjectInfo, ContactInfo


class ExcelParser:
    """Parser for Excel files containing lead data."""

    def parse(self, file_path: str) -> List[ParsedLeadData]:
        """
        Parse an Excel file and extract lead data.

        Args:
            file_path: Path to the Excel file

        Returns:
            List of ParsedLeadData objects
        """
        # Read Excel file
        df = pd.read_excel(file_path)

        # Normalize column names (lowercase, replace spaces with underscores)
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        leads = []

        # Iterate through rows and create lead objects
        for _, row in df.iterrows():
            lead_data = self._parse_row(row)
            if lead_data:
                leads.append(lead_data)

        return leads

    def _parse_row(self, row: pd.Series) -> Optional[ParsedLeadData]:
        """
        Parse a single row from Excel into ParsedLeadData.

        Expected columns (flexible):
        - project_name, company, contact_name, email, phone
        - address, city, state, zip, valuation
        - project_type, description, etc.
        """
        # Skip empty rows
        if row.isna().all():
            return None

        # Extract project info
        project_info = ProjectInfo(
            project_name=self._get_value(row, ['project_name', 'project', 'name']),
            address=self._get_value(row, ['address', 'street']),
            city=self._get_value(row, ['city']),
            state=self._get_value(row, ['state']),
            zip_code=self._get_value(row, ['zip', 'zip_code', 'zipcode']),
            valuation=self._get_value(row, ['valuation', 'value', 'project_value', 'budget']),
            project_type=self._get_value(row, ['project_type', 'type']),
            description=self._get_value(row, ['description', 'notes', 'details']),
            contract_number=self._get_value(row, ['contract_number', 'contract', 'contract_no']),
            bid_date=self._get_value(row, ['bid_date', 'date']),
        )

        # Extract contact info
        contact = ContactInfo(
            name=self._get_value(row, ['contact_name', 'contact', 'name']),
            company=self._get_value(row, ['company', 'organization', 'firm']),
            email=self._get_value(row, ['email', 'email_address']),
            phone=self._get_value(row, ['phone', 'telephone', 'phone_number']),
            title=self._get_value(row, ['title', 'position', 'role']),
        )

        return ParsedLeadData(
            project_info=project_info,
            owner_contact=contact if contact.name or contact.email else None,
            source="Excel Upload"
        )

    def _get_value(self, row: pd.Series, column_names: List[str]) -> Optional[str]:
        """
        Get value from row by trying multiple possible column names.

        Args:
            row: Pandas Series (row from DataFrame)
            column_names: List of possible column names to try

        Returns:
            Value as string or None
        """
        for col in column_names:
            if col in row.index and pd.notna(row[col]):
                value = str(row[col]).strip()
                return value if value else None
        return None
