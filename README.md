# 🏠 Housefinder - Automated Monteur Accommodation Finder

**Version 4.0** - Complete automated system for finding worker accommodation

## 📋 Overview

Housefinder is an automated system designed to find and manage accommodation for Monteur (construction/industrial workers) in Germany. The system scrapes multiple accommodation platforms, filters suitable options, automatically contacts landlords via email and WhatsApp, analyzes responses using AI, and provides ranked recommendations.

## ✨ Features

### Core Functionality

- **Automated Web Scraping** - Searches 5+ platforms for accommodation
  - Monteurzimmer.de
  - Booking.com (long-term stays)
  - Airbnb (private rooms)
  - WG-Gesucht
  - Ebay Kleinanzeigen

- **Smart Filtering** - Validates listings based on:
  - Distance (20-35km radius from work location)
  - Budget constraints
  - Contact information availability
  - Duplicate detection across platforms

- **Automated Communication**
  - Email outreach to landlords via SendGrid
  - WhatsApp messaging via Business Cloud API
  - Personalized messages per employee
  - Automatic follow-ups (6-12 hours)

- **AI-Powered Analysis**
  - GPT-4 extracts structured data from landlord responses
  - Analyzes availability, pricing, amenities, location details
  - Works with both email and WhatsApp responses

- **Google Sheets Integration**
  - Read employee data from "Mitarbeiter" sheet
  - Write results to "Ergebnisse" sheet
  - Real-time updates

- **Intelligent Recommendations**
  - Ranks accommodation options by distance, price, amenities
  - Generates TOP 3 recommendations
  - Provides warnings for unsuitable options
  - Creates management summaries

- **Urgency Handling**
  - Priority processing for urgent cases
  - Faster scraping intervals (2 hours vs 24 hours)
  - Immediate WhatsApp messaging
  - Faster follow-ups (6 hours vs 12 hours)

## 🏗️ Architecture

```
housefinder/
├── src/
│   ├── models/          # Data models (Employee, Listing, Result)
│   ├── scrapers/        # Web scrapers for each platform
│   ├── filters/         # Filtering and validation logic
│   ├── communication/   # Email and WhatsApp senders
│   ├── ai/             # GPT response analysis & recommendations
│   ├── sheets/         # Google Sheets integration
│   ├── utils/          # Utilities (region calculator, logger)
│   ├── config/         # Configuration management
│   └── main.py         # Main application orchestrator
├── data/               # Data storage
├── reports/            # Generated reports
├── logs/               # Application logs
├── credentials/        # API credentials
├── tests/              # Test suite
└── requirements.txt    # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Google Cloud account with Sheets API enabled
- SendGrid account for email
- WhatsApp Business Cloud API account
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/devshift-stack/Housefinder.git
   cd Housefinder
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Setup Google Sheets credentials**
   - Create a service account in Google Cloud Console
   - Download JSON credentials
   - Save as `credentials/google-credentials.json`

6. **Create Google Sheets**
   - Create a new Google Spreadsheet
   - Copy the Sheet ID from URL
   - Add to `.env` as `GOOGLE_SHEET_ID`
   - Share sheet with service account email

### Configuration

Edit `.env` file with your credentials:

```env
# Google Sheets
GOOGLE_SHEET_ID=your-sheet-id-here

# Email
SENDGRID_API_KEY=your-sendgrid-key
FROM_EMAIL=housing@step2job.com

# WhatsApp
WHATSAPP_ACCESS_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id

# OpenAI
OPENAI_API_KEY=your-openai-key
```

## 📊 Usage

### Web Interface (Recommended for Replit)

**Start the web interface:**
```bash
python app.py
```

Then open your browser to `http://localhost:5000` to access the dashboard.

The web interface provides:
- System status monitoring
- Employee management
- Quick actions (setup sheets, run search)
- Real-time updates

### Command Line Interface

**Setup Google Sheets:**

Run once to create sheet templates:

```python
from src.main import HousefinderApp

app = HousefinderApp()
app.setup_sheets()
```

### Add Employees

In Google Sheets "Mitarbeiter" tab, add employee data:

| Employee | Start Date | Location | ZIP | City | State | Urgent (Yes/No) | Budget | Num Persons |
|----------|------------|----------|-----|------|-------|-----------------|--------|-------------|
| John Doe | 15.01.2026 | ATU Berlin | 13585 | Berlin | Berlin | No | 1200 | 1 |

### Run Application

**Web Interface (recommended):**
```bash
python app.py
```

**One-time run (CLI):**
```bash
python -m src.main
```

**Scheduled mode (continuous):**
```python
from src.main import HousefinderApp

app = HousefinderApp()
app.run_scheduled()
```

The system will:
1. Read employees from Google Sheets
2. Calculate search regions (20-35km radius)
3. Scrape all platforms
4. Filter and validate listings
5. Send emails and WhatsApp messages
6. Wait for responses
7. Analyze responses with AI
8. Write results to "Ergebnisse" sheet
9. Generate TOP 3 recommendations

## 📝 Workflow

### Step 0: Employee Input (Denis)
- Enter employee data in "Mitarbeiter" Google Sheet
- Mark urgent cases with "Yes"

### Step 0.1: Region Generation (Denis + ChatGPT)
- System calculates 20-35km search radius
- Identifies nearby towns automatically

### Step 1: Web Scraping (Arman)
- Scrapes 5 platforms for listings
- Extracts: title, address, price, contact info, description

### Step 2: Filtering (Arman)
- Removes listings outside 35km radius
- Filters by budget
- Removes duplicates
- Validates contact information

### Step 3: Email Outreach (Denis + Make)
- Sends personalized emails from housing@step2job.com
- Subject marked "DRINGEND" for urgent cases
- Includes employee details and requirements

### Step 4: WhatsApp Messaging (Emir)
- Sends WhatsApp messages to landlords
- Immediate for urgent cases
- Automatic follow-ups after 6-12 hours
- Handles incoming responses

### Step 5: AI Response Analysis (Emir + Make)
- GPT-4 extracts structured data from responses
- Analyzes availability, pricing, amenities
- Works with both email and WhatsApp

### Step 6: Results Storage (Emir)
- Writes all results to "Ergebnisse" sheet
- Includes employee info and all extracted fields

### Step 7: Recommendations (Denis + ChatGPT)
- Ranks results by distance, price, amenities
- Generates TOP 3 recommendations
- Creates management summary
- Identifies warnings (too far, too expensive)

### Step 8: Urgency Priority (Denis)
- Urgent cases processed every 2 hours
- Normal cases processed every 24 hours
- Faster follow-ups for urgent (6h vs 12h)
- Manager notifications

## 🔧 API Integration

### SendGrid Email
```python
from src.communication import EmailSender

sender = EmailSender()
sender.send_inquiry(employee, listing)
```

### WhatsApp Business API
```python
from src.communication import WhatsAppSender

whatsapp = WhatsAppSender()
whatsapp.send_inquiry(employee, listing)
```

### OpenAI GPT-4
```python
from src.ai import ResponseAnalyzer

analyzer = ResponseAnalyzer()
result = analyzer.analyze_response(response_text, employee)
```

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## 📦 Dependencies

Key dependencies:
- `gspread` - Google Sheets integration
- `sendgrid` - Email sending
- `requests` - WhatsApp API calls
- `openai` - GPT-4 integration
- `beautifulsoup4` - Web scraping
- `selenium` - Dynamic content scraping
- `geopy` - Distance calculations
- `pydantic` - Data validation
- `schedule` - Job scheduling

## 🔐 Security

- Store API keys in `.env` file (never commit)
- Use service accounts for Google Sheets
- Secure WhatsApp webhook with verification token
- Follow data protection regulations (GDPR)

## 📈 Monitoring

Logs are stored in `logs/housefinder.log`

Monitor:
- Scraping success rates
- Email/WhatsApp delivery
- Response analysis accuracy
- System errors

## 🤝 Contributing

### Responsibilities

- **Arman**: Scraping, Filtering, Region generation
- **Denis**: Employee data, Email templates, Urgency logic
- **Emir**: WhatsApp integration, Results storage, AI analysis

## 📄 License

Proprietary - Step2Job GmbH

## 🆘 Support

For support, contact: housing@step2job.com

## 🚧 Future Enhancements (Step 9 - Optional)

- Voice module for WhatsApp audio messages
- Automated audio summaries
- Spoken notifications for managers
- Video property tours integration

## 📚 Documentation

- [Configuration Guide](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

---

**Built with ❤️ by Step2Job Team**