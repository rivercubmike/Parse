"""FastAPI application for parsing documents and creating ZOHO leads."""
import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from app.parsers.pdf_parser import PDFParser
from app.parsers.excel_parser import ExcelParser
from app.zoho.client import ZohoClient
from app.config import settings
from app.models import ParsedLeadData

app = FastAPI(
    title="ZOHO Lead Parser",
    description="Parse PDF/Excel documents and create leads in ZOHO CRM",
    version="1.0.0"
)

pdf_parser = PDFParser()
excel_parser = ExcelParser()
zoho_client = ZohoClient()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "ZOHO Lead Parser API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, parse it, and create a lead in ZOHO CRM.

    Args:
        file: PDF file upload

    Returns:
        JSON response with parsed data and ZOHO lead creation result
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB"
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Parse PDF
        parsed_data = pdf_parser.parse(tmp_file_path)

        # Convert to ZOHO lead
        zoho_lead = zoho_client.convert_to_zoho_lead(parsed_data)

        # Create lead in ZOHO
        zoho_response = zoho_client.create_lead(zoho_lead)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Lead created successfully",
                "parsed_data": parsed_data.model_dump(mode='json'),
                "zoho_response": zoho_response
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


@app.post("/upload/excel")
async def upload_excel(file: UploadFile = File(...)):
    """
    Upload an Excel file, parse it, and create leads in ZOHO CRM.

    Args:
        file: Excel file upload (.xlsx, .xls)

    Returns:
        JSON response with parsed data and ZOHO lead creation results
    """
    # Validate file type
    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are allowed")

    # Check file size
    content = await file.read()
    file_size = len(content)
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB"
        )

    # Save uploaded file temporarily
    suffix = '.xlsx' if file.filename.endswith('.xlsx') else '.xls'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Parse Excel
        parsed_leads = excel_parser.parse(tmp_file_path)

        if not parsed_leads:
            raise HTTPException(status_code=400, detail="No valid lead data found in Excel file")

        # Create leads in ZOHO
        zoho_responses = []
        for lead_data in parsed_leads:
            zoho_lead = zoho_client.convert_to_zoho_lead(lead_data)
            response = zoho_client.create_lead(zoho_lead)
            zoho_responses.append(response)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"Created {len(parsed_leads)} lead(s) successfully",
                "leads_created": len(parsed_leads),
                "parsed_data": [lead.model_dump(mode='json') for lead in parsed_leads],
                "zoho_responses": zoho_responses
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


@app.post("/parse/pdf")
async def parse_pdf_only(file: UploadFile = File(...)):
    """
    Parse a PDF file without creating a ZOHO lead (for testing/preview).

    Args:
        file: PDF file upload

    Returns:
        JSON response with parsed data only
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        parsed_data = pdf_parser.parse(tmp_file_path)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "parsed_data": parsed_data.model_dump(mode='json')
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
