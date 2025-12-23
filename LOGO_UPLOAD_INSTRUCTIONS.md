# Adding Your TIDY Services Logo

The UI currently has a text placeholder for your logo. Follow these steps to add your actual logo image:

## Option 1: Add Logo via EC2 (Recommended)

### Step 1: Upload Logo to EC2

From your local computer where you have the logo file:

```bash
# If using SCP (Mac/Linux/Windows PowerShell)
scp -i zoho-parser-key.pem /path/to/your/logo.png ubuntu@54.163.39.14:/home/ubuntu/parse/static/logo.png

# Replace /path/to/your/logo.png with your actual logo file path
```

**Or use EC2 Instance Connect file upload:**
1. Connect via EC2 Instance Connect
2. Use the "Actions" → "Upload file" option in the browser terminal
3. Upload logo to `/home/ubuntu/parse/static/logo.png`

### Step 2: Update HTML to Use the Logo

In your EC2 terminal:

```bash
cd ~/parse
nano static/index.html
```

Find this line (around line 291):

```html
<img src="data:image/svg+xml;base64,..." alt="TIDY Services Logo" class="logo">
```

Replace it with:

```html
<img src="/static/logo.png" alt="TIDY Services Logo" class="logo">
```

Save and exit (`Ctrl+X`, `Y`, `Enter`)

### Step 3: Restart the Service

```bash
sudo systemctl restart zoho-parser
```

## Option 2: Add Logo to Repository

### Step 1: Add Logo Locally

On your development machine:

```bash
cd /home/user/Parse
cp /path/to/your/logo.png static/logo.png
```

### Step 2: Update the HTML

Edit `static/index.html` and change line 291 from:

```html
<img src="data:image/svg+xml;base64,..." alt="TIDY Services Logo" class="logo">
```

To:

```html
<img src="/static/logo.png" alt="TIDY Services Logo" class="logo">
```

### Step 3: Commit and Push

```bash
git add static/logo.png static/index.html
git commit -m "Add TIDY Services logo image"
git push origin claude/zoho-lead-parser-ISVda
```

### Step 4: Update EC2

In your EC2 terminal:

```bash
cd ~/parse
git pull origin claude/zoho-lead-parser-ISVda
sudo systemctl restart zoho-parser
```

## Logo Requirements

**Recommended Specifications:**
- **Format**: PNG with transparent background (or JPG/SVG)
- **Size**: 600-800px wide, 150-250px tall
- **Aspect Ratio**: Wide horizontal format works best
- **File Size**: Under 500KB
- **Background**: Transparent or white (matches the green header)

**Current Placeholder:**
- Text-based "TIDY SERVICES" with "Keeping Your Site Clean" tagline
- White text on green background

## Testing

After uploading, visit:
```
http://54.163.39.14:8000
```

You should see your logo in the green header at the top of the page.

## Troubleshooting

**Logo not showing:**
1. Check file path: `/home/ubuntu/parse/static/logo.png`
2. Verify file permissions: `ls -l ~/parse/static/logo.png`
3. Check browser console for errors (F12)
4. Try hard refresh: `Ctrl+F5` or `Cmd+Shift+R`

**Logo too large/small:**
Edit `static/index.html` and adjust the `.logo` CSS:
```css
.logo {
    max-width: 350px;  /* Adjust this value */
    width: 100%;
    height: auto;
}
```

**Wrong colors:**
- Use a version with white/light colors for visibility on green background
- Or use PNG with transparent background

## Alternative: Use External URL

If your logo is hosted elsewhere (company website, CDN, etc.):

```html
<img src="https://your-website.com/logo.png" alt="TIDY Services Logo" class="logo">
```

This avoids uploading the file to the server.
