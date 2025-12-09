# Deployment Guide - Housefinder

This guide explains how to deploy and run the Housefinder system in production.

## Prerequisites

- Python 3.9 or higher
- Google Cloud account with Sheets API enabled
- SendGrid account (for email)
- WhatsApp Business Cloud API account (optional but recommended)
- OpenAI API account (for GPT-4)

## Step-by-Step Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/devshift-stack/Housefinder.git
cd Housefinder
```

### 2. Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Google Cloud Setup

#### Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable Google Sheets API
4. Create a Service Account
5. Download JSON credentials
6. Save as `credentials/google-credentials.json`

#### Create Google Sheet

1. Create a new Google Spreadsheet
2. Copy the Sheet ID from URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
3. Share sheet with service account email (from credentials JSON)
4. Give "Editor" permissions

### 4. API Keys Setup

#### SendGrid

1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create API Key with "Mail Send" permissions
3. Verify sender email: `housing@step2job.com`

#### WhatsApp Business API

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a Business App
3. Add WhatsApp product
4. Get:
   - Access Token
   - Phone Number ID
   - Business Account ID
5. Setup webhook (see Webhook Setup section)

#### OpenAI

1. Sign up at [OpenAI](https://platform.openai.com/)
2. Create API key
3. Ensure GPT-4 access

### 5. Environment Configuration

```bash
# Copy example
cp .env.example .env

# Edit with your credentials
nano .env
```

Fill in all required values:

```env
# Google Sheets
GOOGLE_SHEET_ID=your-actual-sheet-id
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/google-credentials.json

# Email
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
FROM_EMAIL=housing@step2job.com
FROM_NAME=Step2Job Housing Team

# WhatsApp
WHATSAPP_BUSINESS_ACCOUNT_ID=123456789
WHATSAPP_ACCESS_TOKEN=EAA...
WHATSAPP_PHONE_NUMBER_ID=987654321
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your-secure-token

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-4-turbo-preview

# Configuration
LOG_LEVEL=INFO
DEBUG_MODE=False
```

### 6. Initialize Google Sheets

```bash
# Run setup
python -c "
from src.main import HousefinderApp
app = HousefinderApp()
app.setup_sheets()
print('✅ Sheets setup complete')
"
```

### 7. Test Configuration

```bash
# Run quickstart test
python quickstart.py
# Choose option 4 to test configuration
```

### 8. Run the Application

#### One-Time Run

```bash
python -m src.main
```

#### Scheduled Mode (Recommended)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/housefinder.service
```

Add:

```ini
[Unit]
Description=Housefinder Accommodation Finder
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/Housefinder
Environment="PATH=/path/to/Housefinder/venv/bin"
ExecStart=/path/to/Housefinder/venv/bin/python -m src.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable housefinder
sudo systemctl start housefinder

# Check status
sudo systemctl status housefinder

# View logs
sudo journalctl -u housefinder -f
```

#### Alternative: Screen or tmux

```bash
# Using screen
screen -S housefinder
source venv/bin/activate
python -m src.main
# Detach: Ctrl+A, D

# Reattach
screen -r housefinder
```

### 9. Webhook Setup (for WhatsApp)

If using WhatsApp, you need to setup a webhook endpoint:

#### Create webhook endpoint

```python
# webhook_server.py
from flask import Flask, request, jsonify
from src.communication import WhatsAppSender
from src.ai import ResponseAnalyzer

app = Flask(__name__)
whatsapp = WhatsAppSender()

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verify webhook"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN:
        return challenge, 200
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming WhatsApp messages"""
    data = request.get_json()
    
    # Process webhook
    message_info = whatsapp.handle_webhook(data)
    
    if message_info and message_info.get('text'):
        # TODO: Process the response
        # - Analyze with GPT
        # - Write to Google Sheets
        # - Send confirmation
        pass
    
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### Setup with Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /webhook {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Configure in Meta

1. Go to WhatsApp App Settings
2. Add webhook URL: `https://your-domain.com/webhook`
3. Add verify token from `.env`
4. Subscribe to `messages` events

### 10. Monitoring

#### Log Files

```bash
# View application logs
tail -f logs/housefinder.log

# View system logs
sudo journalctl -u housefinder -f
```

#### Metrics to Monitor

- Scraping success rate
- Email delivery rate
- WhatsApp message status
- Response analysis accuracy
- Error frequency

#### Setup Alerts

Create monitoring script:

```python
# monitor.py
import logging
from datetime import datetime, timedelta

def check_recent_errors():
    """Check for errors in last hour"""
    log_file = "logs/housefinder.log"
    errors = []
    
    with open(log_file, 'r') as f:
        for line in f:
            if 'ERROR' in line or 'CRITICAL' in line:
                errors.append(line)
    
    if len(errors) > 10:
        # Send alert email
        print(f"⚠️ {len(errors)} errors found in logs!")
    
    return errors

if __name__ == "__main__":
    check_recent_errors()
```

Run with cron:

```bash
# Edit crontab
crontab -e

# Add (check every hour)
0 * * * * cd /path/to/Housefinder && venv/bin/python monitor.py
```

## Maintenance

### Daily Tasks

- Check logs for errors
- Verify scraping is working
- Review results in Google Sheets

### Weekly Tasks

- Review and respond to failed communications
- Update scraper selectors if websites changed
- Check API rate limits and usage

### Monthly Tasks

- Review and optimize filters
- Analyze success rates
- Update documentation
- Review and update templates

## Troubleshooting

### Scraping Issues

**Problem:** No listings found

```bash
# Test individual scraper
python -c "
from src.scrapers import MonteurzimmerScraper
scraper = MonteurzimmerScraper()
listings = scraper.scrape('Berlin')
print(f'Found: {len(listings)}')
"
```

**Solution:** Website structure may have changed. Update selectors in scraper file.

### Google Sheets Issues

**Problem:** Permission denied

**Solution:** 
- Verify service account email has access to sheet
- Check credentials file path
- Ensure Sheets API is enabled

### Email Issues

**Problem:** Emails not sending

**Solution:**
- Verify SendGrid API key
- Check sender email is verified
- Review SendGrid dashboard for bounces

### WhatsApp Issues

**Problem:** Messages not sending

**Solution:**
- Verify WhatsApp Business API is activated
- Check access token validity
- Ensure phone number is verified
- Review Meta Business Manager

## Scaling

### Handling More Employees

The system is designed to scale. For large deployments:

1. **Database**: Consider moving from Google Sheets to PostgreSQL
2. **Queue**: Use Celery for job queue
3. **Caching**: Add Redis for caching
4. **Load Balancing**: Use multiple workers

### High-Availability Setup

```
┌─────────────┐
│   Nginx     │  Load Balancer
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│ App1│ │ App2│  Multiple instances
└──┬──┘ └──┬──┘
   │       │
   └───┬───┘
       │
  ┌────▼────┐
  │  Redis  │  Shared cache
  └────┬────┘
       │
  ┌────▼────┐
  │   DB    │  Shared database
  └─────────┘
```

## Security Checklist

- [ ] All API keys in `.env` (not in code)
- [ ] `.env` file has restricted permissions (600)
- [ ] Credentials directory excluded from git
- [ ] HTTPS enabled for webhooks
- [ ] Webhook verify token is strong
- [ ] Regular security updates
- [ ] Log files don't contain sensitive data
- [ ] Service runs as non-root user
- [ ] Firewall configured properly

## Backup

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/housefinder"

# Backup logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" logs/

# Backup data
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" data/

# Backup configuration (without secrets)
cp .env.example "$BACKUP_DIR/.env.example_$DATE"

# Keep only last 30 days
find "$BACKUP_DIR" -mtime +30 -delete

echo "✅ Backup complete: $DATE"
```

Add to crontab:

```bash
0 2 * * * /path/to/backup.sh
```

## Support

For issues or questions:

- Email: housing@step2job.com
- GitHub Issues: https://github.com/devshift-stack/Housefinder/issues

## License

Proprietary - Step2Job GmbH
