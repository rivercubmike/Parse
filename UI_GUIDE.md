# User-Friendly Upload Interface

## Overview

The ZOHO Lead Parser now includes a simple, clean web interface that your sales team can use without any technical knowledge.

## Features

✅ **Drag & Drop Upload** - Just drag files onto the page
✅ **Browse Button** - Click to select files from your computer
✅ **Real-time Feedback** - See upload progress and results instantly
✅ **Mobile Friendly** - Works on phones and tablets
✅ **Recent Uploads** - Track what's been uploaded
✅ **No Training Required** - Intuitive interface anyone can use

## How to Access

Simply go to: **http://YOUR_EC2_IP:8000**

Example: `http://54.163.39.14:8000`

## How to Use

### For Sales Team Members:

1. **Open the web page** in any browser (Chrome, Firefox, Safari, Edge)

2. **Upload a file** using one of two methods:
   - **Drag & Drop**: Drag a PDF or Excel file onto the upload area
   - **Browse**: Click the "Browse Files" button and select a file

3. **Wait for confirmation**:
   - You'll see a loading message
   - Then a success message with the lead details
   - Or an error message if something went wrong

4. **Done!** The lead is now in ZOHO CRM

## Supported File Types

- **PDF** files (construction bid documents)
- **Excel** files (.xlsx, .xls)

## File Size Limit

- Maximum: **5 MB** per file
- This is plenty for most construction bid documents

## What Happens Behind the Scenes

1. File is uploaded to the server
2. System extracts contact and project information
3. Lead is automatically created in ZOHO CRM
4. You see confirmation with lead details

## Troubleshooting

### "Invalid file type" error
- Make sure you're uploading a PDF or Excel file
- Check the file extension (.pdf, .xlsx, or .xls)

### "File too large" error
- File exceeds 5MB limit
- Try compressing the PDF or splitting large Excel files

### "Upload failed" error
- Check your internet connection
- Try refreshing the page
- Contact IT support if issue persists

## For IT/Administrators

### Accessing the Technical API

The Swagger API documentation is still available at:
`http://YOUR_EC2_IP:8000/docs`

### Health Check

Check if the system is running:
`http://YOUR_EC2_IP:8000/api/health`

### Customization

The UI can be customized by editing:
- `static/index.html` - The HTML structure and styling
- Color scheme is currently purple/blue gradient
- Company logo can be added to the header

## Screenshots

### Main Interface
- Clean, modern design
- Purple gradient header
- Large drag-and-drop area
- Supported file types clearly shown

### Success State
- Green checkmark
- Lead details displayed
- Contact name, company, email, phone
- Project information

### Recent Uploads
- List of recently uploaded files
- Shows filename and upload time
- Keeps last 5 uploads

## Mobile Support

The interface is fully responsive and works on:
- Desktop computers
- Laptops
- Tablets (iPad, Android tablets)
- Smartphones (iPhone, Android phones)

## Security Notes

- All uploads are processed securely
- Files are temporarily stored and deleted after processing
- HTTPS recommended for production (see AWS_SETUP_GUIDE.md)

## Need Help?

Contact your IT administrator or refer to:
- Main documentation: `README.md`
- AWS setup guide: `AWS_SETUP_GUIDE.md`
- API documentation: `http://YOUR_IP:8000/docs`
