#!/usr/bin/env python
"""Test script to verify ZOHO CRM credentials and connection."""
import sys
from app.zoho.client import ZohoClient
from app.config import settings


def test_zoho_connection():
    """Test ZOHO CRM API connection."""
    print("Testing ZOHO CRM Connection...")
    print(f"Region: {settings.ZOHO_REGION}")
    print(f"API Domain: {settings.ZOHO_API_DOMAIN}")
    print()

    try:
        # Initialize client
        client = ZohoClient()
        print("✓ ZOHO client initialized")

        # Try to get access token
        print("Attempting to get access token...")
        token = client._get_access_token()

        if token:
            print("✓ Successfully obtained access token")
            print(f"  Token (first 20 chars): {token[:20]}...")
            print()
            print("✅ ZOHO CRM connection successful!")
            print()
            print("You can now start uploading documents to create leads.")
            return True
        else:
            print("✗ Failed to obtain access token")
            return False

    except Exception as e:
        print(f"✗ Error connecting to ZOHO CRM: {str(e)}")
        print()
        print("Please check:")
        print("1. Your ZOHO credentials in .env file")
        print("2. The refresh token is still valid")
        print("3. API permissions are correctly configured")
        return False


if __name__ == "__main__":
    success = test_zoho_connection()
    sys.exit(0 if success else 1)
