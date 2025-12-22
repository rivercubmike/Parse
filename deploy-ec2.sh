#!/bin/bash
#
# AWS EC2 T2 Micro Deployment Script for ZOHO Lead Parser
# This script automates the deployment on a fresh Ubuntu 22.04 EC2 instance
#
# Usage: bash deploy-ec2.sh
#

set -e  # Exit on any error

echo "=========================================="
echo "ZOHO Lead Parser - EC2 T2 Micro Deployment"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as ubuntu user
if [ "$USER" != "ubuntu" ]; then
    echo -e "${YELLOW}Warning: This script is designed to run as 'ubuntu' user${NC}"
    echo "Current user: $USER"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}[1/9] Updating system packages...${NC}"
sudo apt update
sudo apt upgrade -y

echo ""
echo -e "${GREEN}[2/9] Installing Python 3.11 and dependencies...${NC}"
sudo apt install -y python3.11 python3.11-venv python3-pip git

echo ""
echo -e "${GREEN}[3/9] Setting up swap space (2GB) for memory optimization...${NC}"
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo -e "${GREEN}✓ Swap space created${NC}"
else
    echo -e "${YELLOW}✓ Swap space already exists${NC}"
fi

echo ""
echo -e "${GREEN}[4/9] Cloning repository...${NC}"
cd ~
if [ -d "Parse" ]; then
    echo -e "${YELLOW}Parse directory already exists. Pulling latest changes...${NC}"
    cd Parse
    git pull origin claude/zoho-lead-parser-ISVda
else
    read -p "Enter your Git repository URL: " REPO_URL
    git clone "$REPO_URL" Parse
    cd Parse
fi

echo ""
echo -e "${GREEN}[5/9] Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo ""
echo -e "${GREEN}[6/9] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo -e "${GREEN}[7/9] Setting up environment variables...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ .env file created from template${NC}"
    echo -e "${YELLOW}⚠ You MUST edit .env and add your ZOHO credentials!${NC}"
    echo ""
    echo "Please enter your ZOHO credentials:"
    read -p "ZOHO_CLIENT_ID: " CLIENT_ID
    read -p "ZOHO_CLIENT_SECRET: " CLIENT_SECRET
    read -p "ZOHO_REDIRECT_URI: " REDIRECT_URI
    read -p "ZOHO_REFRESH_TOKEN: " REFRESH_TOKEN

    # Update .env file
    sed -i "s/your_client_id_here/$CLIENT_ID/" .env
    sed -i "s/your_client_secret_here/$CLIENT_SECRET/" .env
    sed -i "s|your_redirect_uri_here|$REDIRECT_URI|" .env
    sed -i "s/your_refresh_token_here/$REFRESH_TOKEN/" .env

    echo -e "${GREEN}✓ .env file configured${NC}"
else
    echo -e "${YELLOW}✓ .env file already exists${NC}"
fi

echo ""
echo -e "${GREEN}[8/9] Testing ZOHO connection...${NC}"
python test_zoho.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ ZOHO connection successful!${NC}"
else
    echo -e "${RED}✗ ZOHO connection failed. Please check your credentials in .env${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}[9/9] Setting up systemd service...${NC}"
sudo cp zoho-parser.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable zoho-parser
sudo systemctl start zoho-parser

echo ""
echo -e "${GREEN}Checking service status...${NC}"
sleep 3
sudo systemctl status zoho-parser --no-pager

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Your ZOHO Lead Parser is now running!"
echo ""
echo "API Endpoints:"
echo "  • Health Check: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo "  • API Docs: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000/docs"
echo ""
echo "Useful Commands:"
echo "  • Check status: sudo systemctl status zoho-parser"
echo "  • View logs: sudo journalctl -u zoho-parser -f"
echo "  • Restart: sudo systemctl restart zoho-parser"
echo "  • Stop: sudo systemctl stop zoho-parser"
echo ""
echo "Memory Usage:"
free -h
echo ""
echo -e "${YELLOW}Note: Make sure your EC2 Security Group allows inbound traffic on port 8000${NC}"
