# AWS EC2 T2 Micro Setup Guide for ZOHO Lead Parser

This guide walks you through setting up your ZOHO Lead Parser on AWS EC2 T2 Micro (optimized for 1GB RAM).

## 📋 Prerequisites

- AWS Account (free tier eligible)
- ZOHO CRM API credentials (Client ID, Secret, Refresh Token)
- Basic terminal/SSH knowledge

## 💰 Cost

- **T2 Micro**: FREE for first 12 months (750 hours/month)
- After free tier: ~$8.50/month

---

## Part 1: Launch EC2 Instance on AWS

### Step 1: Sign in to AWS Console

1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Sign in with your account
3. Select your preferred region (e.g., **us-east-1** - N. Virginia)

### Step 2: Launch EC2 Instance

1. **Navigate to EC2**:
   - In the AWS Console search bar, type "EC2"
   - Click on "EC2" (Virtual Servers in the Cloud)

2. **Click "Launch Instance"** (orange button)

3. **Configure Instance**:

   **Name and Tags:**
   - Name: `zoho-lead-parser`

   **Application and OS Images (Amazon Machine Image):**
   - Click **"Quick Start"**
   - Select **"Ubuntu"**
   - Choose **"Ubuntu Server 22.04 LTS (HVM), SSD Volume Type"**
   - Architecture: **64-bit (x86)**

   **Instance Type:**
   - Select **"t2.micro"** (should be pre-selected)
   - Shows: 1 vCPU, 1 GiB Memory
   - ✅ Look for "Free tier eligible" tag

   **Key Pair (login):**
   - Click **"Create new key pair"**
   - Key pair name: `zoho-parser-key`
   - Key pair type: **RSA**
   - Private key file format: **`.pem`** (for Mac/Linux) or **`.ppk`** (for Windows/PuTTY)
   - Click **"Create key pair"**
   - ⚠️ **IMPORTANT**: The `.pem` file will download automatically. Save it securely!

   **Network Settings:**
   - Click **"Edit"** next to Network settings
   - Auto-assign public IP: **Enable**
   - Firewall (security groups): **Create security group**
   - Security group name: `zoho-parser-sg`
   - Description: `Security group for ZOHO Lead Parser`

   **Add Security Group Rules:**
   - ✅ **SSH** (already there)
     - Type: SSH
     - Protocol: TCP
     - Port: 22
     - Source: **My IP** (or 0.0.0.0/0 for access from anywhere - less secure)

   - ➕ Click **"Add security group rule"**
     - Type: **Custom TCP**
     - Protocol: TCP
     - Port Range: **8000**
     - Source type: **Anywhere** (0.0.0.0/0)
     - Description: "API access"

   **Configure Storage:**
   - Size: **8 GiB** (default is fine)
   - Volume type: **gp3** (General Purpose SSD)
   - ✅ Keep "Delete on Termination" checked

   **Advanced Details:** (Leave as default)

4. **Review and Launch**:
   - Review your configuration in the Summary panel (right side)
   - Number of instances: **1**
   - Click **"Launch instance"** (orange button)

5. **Success!**
   - You'll see "Successfully initiated launch of instance"
   - Click **"View all instances"**
   - Wait for **Instance State** to show **"Running"** (takes ~2 minutes)
   - Wait for **Status Check** to show **"2/2 checks passed"**

### Step 3: Note Your Instance Details

Once your instance is running, note these details:

1. Click on your instance (checkbox)
2. In the details panel below, copy:
   - **Public IPv4 address** (e.g., 3.85.123.45) - you'll need this!
   - **Public IPv4 DNS** (optional)

---

## Part 2: Connect to Your EC2 Instance

### For Mac/Linux Users:

1. **Open Terminal**

2. **Set permissions on your key file**:
```bash
cd ~/Downloads  # or wherever you saved the key
chmod 400 zoho-parser-key.pem
```

3. **Connect via SSH**:
```bash
ssh -i zoho-parser-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```
Replace `YOUR_EC2_PUBLIC_IP` with your actual IP from Step 3 above.

Example:
```bash
ssh -i zoho-parser-key.pem ubuntu@3.85.123.45
```

4. **Accept the connection**:
- Type `yes` when prompted about authenticity
- You should now see: `ubuntu@ip-xxx-xxx-xxx-xxx:~$`

### For Windows Users:

**Option A: Using PowerShell/CMD (Windows 10+)**

1. Open PowerShell
2. Navigate to where you saved the key:
```powershell
cd Downloads
```

3. Connect:
```powershell
ssh -i zoho-parser-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

**Option B: Using PuTTY**

1. Download and install [PuTTY](https://www.putty.org/)
2. If you downloaded `.pem` file, convert it to `.ppk`:
   - Open **PuTTYgen**
   - Click **Load**, select your `.pem` file
   - Click **Save private key** (save as `.ppk`)
3. Open **PuTTY**
4. Host Name: `ubuntu@YOUR_EC2_PUBLIC_IP`
5. Connection > SSH > Auth > Credentials: Browse and select your `.ppk` file
6. Click **Open**

---

## Part 3: Deploy ZOHO Lead Parser

### Option 1: Automated Deployment (Recommended)

Once connected to your EC2 instance via SSH:

```bash
# Download the deployment script
wget https://raw.githubusercontent.com/YOUR_USERNAME/Parse/claude/zoho-lead-parser-ISVda/deploy-ec2.sh

# Make it executable
chmod +x deploy-ec2.sh

# Run the deployment
bash deploy-ec2.sh
```

The script will:
- ✅ Update system packages
- ✅ Install Python 3.11
- ✅ Create 2GB swap space
- ✅ Clone the repository
- ✅ Install dependencies
- ✅ Configure ZOHO credentials
- ✅ Test the connection
- ✅ Set up systemd service
- ✅ Start the application

**Follow the prompts** to enter your ZOHO API credentials when asked.

### Option 2: Manual Deployment (Step-by-Step)

If you prefer to do it manually:

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git

# 3. Create swap space (important for 1GB RAM!)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 4. Clone repository
git clone YOUR_REPO_URL Parse
cd Parse

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install Python packages
pip install -r requirements.txt

# 7. Configure environment variables
cp .env.example .env
nano .env  # Edit and add your ZOHO credentials

# 8. Test ZOHO connection
python test_zoho.py

# 9. Set up systemd service
sudo cp zoho-parser.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable zoho-parser
sudo systemctl start zoho-parser

# 10. Check status
sudo systemctl status zoho-parser
```

---

## Part 4: Verify Deployment

### Check Service Status

```bash
sudo systemctl status zoho-parser
```

You should see:
- ✅ Active: **active (running)**
- ✅ No errors in the logs

### View Live Logs

```bash
sudo journalctl -u zoho-parser -f
```

Press `Ctrl+C` to exit.

### Test the API

**From your local computer** (not EC2), open a web browser:

```
http://YOUR_EC2_PUBLIC_IP:8000
```

You should see:
```json
{
  "message": "ZOHO Lead Parser API",
  "status": "running",
  "version": "1.0.0"
}
```

### Access Interactive API Documentation

```
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

You'll see the Swagger UI where you can test all endpoints!

---

## Part 5: Using the API

### Upload a PDF

Using the browser at `http://YOUR_EC2_PUBLIC_IP:8000/docs`:

1. Click **POST /upload/pdf**
2. Click **"Try it out"**
3. Click **"Choose File"** and select your PDF
4. Click **"Execute"**
5. Check the response - lead should be created in ZOHO!

### Using curl (Command Line)

```bash
curl -X POST "http://YOUR_EC2_PUBLIC_IP:8000/upload/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

---

## Part 6: Useful Commands

### Service Management

```bash
# Check status
sudo systemctl status zoho-parser

# Restart service
sudo systemctl restart zoho-parser

# Stop service
sudo systemctl stop zoho-parser

# Start service
sudo systemctl start zoho-parser

# View logs (live)
sudo journalctl -u zoho-parser -f

# View last 100 logs
sudo journalctl -u zoho-parser -n 100
```

### System Monitoring

```bash
# Check memory usage
free -h

# Check disk usage
df -h

# Check running processes
htop  # Install with: sudo apt install htop

# Check if port 8000 is listening
sudo netstat -tlnp | grep 8000
```

### Update Code

```bash
cd ~/Parse
git pull origin claude/zoho-lead-parser-ISVda
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart zoho-parser
```

---

## 🔧 Troubleshooting

### Service Won't Start

```bash
# Check detailed logs
sudo journalctl -u zoho-parser -n 50 --no-pager

# Check if port is already in use
sudo lsof -i :8000

# Manually test the application
cd ~/Parse
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Can't Access from Browser

1. **Check Security Group**:
   - AWS Console > EC2 > Security Groups
   - Find `zoho-parser-sg`
   - Verify port 8000 is open for 0.0.0.0/0

2. **Check if service is running**:
```bash
sudo systemctl status zoho-parser
curl http://localhost:8000
```

3. **Check firewall (unlikely on EC2)**:
```bash
sudo ufw status
```

### ZOHO API Errors

```bash
# Test credentials
cd ~/Parse
source venv/bin/activate
python test_zoho.py

# Check .env file
cat .env | grep ZOHO
```

### Out of Memory

```bash
# Check memory usage
free -h

# Verify swap is active
swapon --show

# Restart service
sudo systemctl restart zoho-parser
```

### PDF Parsing Fails

- Ensure PDF is text-based (not scanned image)
- Check file size (limit is 5MB on T2 Micro)
- View logs for specific error

---

## 🚀 Next Steps

### Add HTTPS (Optional but Recommended)

1. **Get a domain name** (e.g., from Namecheap, GoDaddy)
2. **Point domain to EC2 IP**
3. **Install Nginx**:
```bash
sudo apt install nginx
```

4. **Install SSL with Let's Encrypt**:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Add Authentication (Optional)

Consider adding API key authentication for production use.

### Set Up Monitoring

- Enable CloudWatch monitoring in EC2
- Set up billing alerts
- Consider using Datadog or New Relic

### Backup Strategy

- Take regular EC2 snapshots
- Consider S3 for uploaded files
- Backup your `.env` file securely

---

## 💲 Cost Management

### Free Tier Limits (First 12 Months)

- ✅ 750 hours/month T2 Micro (1 instance running 24/7)
- ✅ 30 GB EBS storage
- ✅ 15 GB data transfer out

### After Free Tier

- T2 Micro: ~$8.50/month
- Data transfer: ~$0.09/GB
- EBS storage: ~$0.10/GB-month

### Cost-Saving Tips

1. **Stop instance when not in use** (AWS Console > EC2 > Instance > Stop)
2. **Use Elastic IP** if you stop/start frequently (prevents IP changes)
3. **Set up billing alerts** (AWS Console > Billing > Budgets)
4. **Delete unused snapshots**

---

## 📞 Support

If you encounter issues:

1. Check logs: `sudo journalctl -u zoho-parser -f`
2. Verify ZOHO credentials: `python test_zoho.py`
3. Check memory: `free -h`
4. Review this guide's Troubleshooting section

---

## ✅ Success Checklist

- [ ] EC2 instance launched and running
- [ ] Connected via SSH
- [ ] Deployment completed successfully
- [ ] Service is active (systemd)
- [ ] Can access `http://YOUR_IP:8000` from browser
- [ ] API docs accessible at `/docs`
- [ ] Test PDF upload works
- [ ] Lead created in ZOHO CRM
- [ ] Reviewed monitoring commands
- [ ] Set up billing alerts (recommended)

**Congratulations! Your ZOHO Lead Parser is live on AWS! 🎉**
