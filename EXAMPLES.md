# Housefinder Examples

This document provides practical examples of using Housefinder.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Google Sheets Setup](#google-sheets-setup)
3. [Processing Single Employee](#processing-single-employee)
4. [Analyzing Responses](#analyzing-responses)
5. [Custom Workflows](#custom-workflows)

## Basic Usage

### Quick Start

```python
from src.main import HousefinderApp

# Create app instance
app = HousefinderApp()

# Setup sheets (first time only)
app.setup_sheets()

# Process all employees
app.process_all_employees()
```

### Scheduled Mode

```python
from src.main import HousefinderApp

app = HousefinderApp()

# Run continuously
# - Urgent: every 2 hours
# - Normal: every 24 hours
app.run_scheduled()
```

## Google Sheets Setup

### Example Employee Data

In the "Mitarbeiter" sheet:

| Employee | Start Date | Location | ZIP | City | State | Urgent (Yes/No) | Budget | Num Persons |
|----------|------------|----------|-----|------|-------|-----------------|--------|-------------|
| Max Müller | 15.01.2026 | ATU Berlin | 13585 | Berlin | Berlin | No | 1200 | 1 |
| Anna Schmidt | 20.01.2026 | ATU München | 80331 | München | Bayern | Yes | 1500 | 2 |
| Peter Wagner | 10.02.2026 | ATU Hamburg | 20095 | Hamburg | Hamburg | No | 1000 | 1 |

### Creating Sheets Programmatically

```python
from src.sheets import EmployeeSheetReader, ResultsSheetWriter

# Setup employee sheet
reader = EmployeeSheetReader()
reader.connect()
reader.create_mitarbeiter_sheet_template()

# Setup results sheet
writer = ResultsSheetWriter()
writer.connect()
writer.create_results_sheet()

print("✅ Sheets created successfully!")
```

## Processing Single Employee

### Manual Employee Processing

```python
from src.main import HousefinderApp
from src.models import Employee
from datetime import datetime

# Create app
app = HousefinderApp()

# Create employee manually
employee = Employee(
    name="John Doe",
    start_date=datetime(2026, 1, 15),
    location="ATU Berlin",
    zip_code="13585",
    city="Berlin",
    state="Berlin",
    urgent=False,
    budget_max=1200,
    num_persons=1
)

# Process this employee
app.process_employee(employee)
```

### Reading from Sheet

```python
from src.sheets import EmployeeSheetReader

reader = EmployeeSheetReader()
reader.connect()

# Get all employees
employees = reader.get_employees()

# Filter urgent employees
urgent = [e for e in employees if e.urgent]

# Process urgent ones
app = HousefinderApp()
for employee in urgent:
    app.process_employee(employee)
```

## Scraping Examples

### Scrape Single Platform

```python
from src.scrapers import MonteurzimmerScraper

scraper = MonteurzimmerScraper()
listings = scraper.scrape(city="Berlin", zip_code="13585")

print(f"Found {len(listings)} listings")

for listing in listings[:5]:  # Show first 5
    print(f"Title: {listing.title}")
    print(f"Price: €{listing.price_per_month}")
    print(f"Contact: {listing.phone or listing.email}")
    print("---")
```

### Scrape All Platforms

```python
from src.scrapers import (
    MonteurzimmerScraper,
    BookingScraper,
    WGGesuchtScraper
)

scrapers = [
    MonteurzimmerScraper(),
    BookingScraper(),
    WGGesuchtScraper(),
]

all_listings = []
for scraper in scrapers:
    listings = scraper.scrape("Berlin")
    all_listings.extend(listings)
    print(f"{scraper.platform_name}: {len(listings)} listings")

print(f"Total: {len(all_listings)} listings")
```

## Filtering Examples

### Basic Filtering

```python
from src.filters import ListingFilter
from src.models import Employee

filter = ListingFilter()

employee = Employee(
    name="Test",
    start_date="01.01.2026",
    location="Berlin",
    zip_code="13585",
    city="Berlin",
    state="Berlin",
    budget_max=1000
)

# Filter listings
filtered = filter.filter_listings(listings, employee)

print(f"Filtered: {len(listings)} → {len(filtered)}")
```

### Remove Duplicates

```python
from src.filters import ListingFilter

filter = ListingFilter()

# Remove duplicates from list
unique = filter.remove_duplicates(all_listings)

print(f"Removed {len(all_listings) - len(unique)} duplicates")
```

### Distance Filtering

```python
from src.utils import RegionCalculator

calculator = RegionCalculator()

# Get work location coordinates
work_coords = calculator.get_coordinates("13585", "Berlin")

# Check if listing is within radius
for listing in listings:
    if listing.city:
        listing_coords = calculator.get_coordinates("", listing.city)
        if listing_coords:
            distance = calculator.calculate_distance(work_coords, listing_coords)
            if distance <= 35:
                print(f"✓ {listing.title} - {distance:.1f}km")
            else:
                print(f"✗ {listing.title} - {distance:.1f}km (too far)")
```

## Communication Examples

### Send Email

```python
from src.communication import EmailSender
from src.models import Employee, Listing

sender = EmailSender()

employee = Employee(
    name="Max Müller",
    start_date="15.01.2026",
    location="ATU Berlin",
    zip_code="13585",
    city="Berlin",
    state="Berlin"
)

listing = Listing(
    title="Monteurzimmer in Berlin",
    platform="Monteurzimmer.de",
    url="https://example.com/listing",
    city="Berlin",
    email="landlord@example.com"
)

# Send inquiry email
success = sender.send_inquiry(employee, listing)
print(f"Email sent: {success}")
```

### Send WhatsApp Message

```python
from src.communication import WhatsAppSender

whatsapp = WhatsAppSender()

# Send initial inquiry
success = whatsapp.send_inquiry(employee, listing)
print(f"WhatsApp sent: {success}")

# Send follow-up later
success = whatsapp.send_followup(employee, "+4912345678")
print(f"Follow-up sent: {success}")
```

### Batch Communication

```python
from src.communication import EmailSender, WhatsAppSender

email_sender = EmailSender()
whatsapp_sender = WhatsAppSender()

# Send to all valid listings
email_results = email_sender.send_batch_inquiries(employee, valid_listings)
whatsapp_results = whatsapp_sender.send_batch_inquiries(employee, valid_listings)

print(f"Emails: {email_results['sent']} sent, {email_results['failed']} failed")
print(f"WhatsApp: {whatsapp_results['sent']} sent, {whatsapp_results['failed']} failed")
```

## Analyzing Responses

### Analyze Single Response

```python
from src.ai import ResponseAnalyzer

analyzer = ResponseAnalyzer()

# Example landlord response
response_text = """
Hallo,

ja, die Wohnung ist verfügbar ab 15.01.2026.

Preis: 850 EUR pro Monat (inkl. Nebenkosten)
Kaution: 2 Monatsmieten
Adresse: Hauptstraße 10, 13585 Berlin
Internet und Parkplatz vorhanden.

Mindestmietdauer: 3 Monate

Freundliche Grüße
Peter Müller
Tel: +49 30 12345678
"""

# Analyze with GPT
result = analyzer.analyze_response(
    response_text=response_text,
    employee=employee,
    listing_url="https://example.com/listing",
    response_source="Email"
)

if result:
    print(f"Available: {result.verfuegbar}")
    print(f"Price: {result.preis_monat}")
    print(f"Address: {result.adresse_unterkunft}")
    print(f"Contact: {result.telefon}")
```

### Quick Availability Check

```python
analyzer = ResponseAnalyzer()

responses = [
    "Ja, die Wohnung ist verfügbar!",
    "Leider nein, bereits vermietet.",
    "Gerne können wir einen Termin vereinbaren.",
]

for response in responses:
    available = analyzer.quick_check_availability(response)
    print(f"'{response[:30]}...' → {'Available' if available else 'Not available'}")
```

## Recommendation Examples

### Rank Results

```python
from src.ai import RecommendationEngine

engine = RecommendationEngine()

# Rank all results
ranked = engine.rank_results(results, employee)

# Show top 3
print("TOP 3 Recommendations:\n")
for result in ranked[:3]:
    print(f"{result.rank}. {result.adresse_unterkunft}")
    print(f"   Price: {result.preis_monat}")
    print(f"   Distance: {result.entfernung_km}")
    if result.warnings:
        print(f"   ⚠️ {result.warnings}")
    print()
```

### Generate Summary

```python
# Generate management summary
summary = engine.generate_summary(ranked, employee)
print(summary)
```

### Write to Sheet

```python
from src.sheets import ResultsSheetWriter

writer = ResultsSheetWriter()
writer.connect()
writer.create_results_sheet()

# Write all results
writer.write_results(ranked)

print("✅ Results written to Google Sheets")
```

## Custom Workflows

### Custom Scraping Schedule

```python
import schedule
import time

def scrape_urgent():
    """Scrape for urgent employees"""
    app = HousefinderApp()
    app._process_urgent_employees()

def scrape_normal():
    """Scrape for normal employees"""
    app = HousefinderApp()
    app._process_normal_employees()

# Custom schedule
schedule.every(1).hour.do(scrape_urgent)  # Every hour
schedule.every(12).hours.do(scrape_normal)  # Twice daily

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Custom Email Template

```python
from src.communication.templates import EmailTemplate

# Override template
class CustomEmailTemplate(EmailTemplate):
    @staticmethod
    def create_inquiry_email(employee, listing):
        subject = f"Urgent Housing Request - {employee.name}"
        body = f"""
        Dear Landlord,
        
        We urgently need accommodation for {employee.name}.
        
        Details:
        - Start: {employee.start_date.strftime('%d.%m.%Y')}
        - Location: {employee.location}
        - Budget: €{employee.budget_max}
        
        Your listing: {listing.url}
        
        Please respond ASAP.
        
        Best regards,
        Housing Team
        """
        return {'subject': subject, 'body': body}
```

### Export Results to PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_pdf(results, filename="report.pdf"):
    """Export results to PDF"""
    c = canvas.Canvas(filename, pagesize=letter)
    
    y = 750
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Accommodation Search Results")
    
    y -= 40
    c.setFont("Helvetica", 12)
    
    for result in results[:10]:  # Top 10
        if y < 100:
            c.showPage()
            y = 750
        
        c.drawString(50, y, f"{result.adresse_unterkunft}")
        y -= 20
        c.drawString(70, y, f"Price: {result.preis_monat}")
        y -= 15
        c.drawString(70, y, f"Contact: {result.telefon}")
        y -= 30
    
    c.save()
    print(f"✅ PDF saved: {filename}")

# Use it
export_to_pdf(ranked_results, "reports/results.pdf")
```

## Error Handling

### Robust Scraping

```python
def safe_scrape(scraper, city):
    """Scrape with error handling"""
    try:
        listings = scraper.scrape(city)
        return listings
    except Exception as e:
        logger.error(f"Scraping failed for {scraper.platform_name}: {e}")
        return []

# Use for all scrapers
all_listings = []
for scraper in scrapers:
    listings = safe_scrape(scraper, "Berlin")
    all_listings.extend(listings)
```

### Retry Logic

```python
import time
from functools import wraps

def retry(times=3, delay=5):
    """Retry decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(times=3, delay=10)
def scrape_with_retry(scraper, city):
    return scraper.scrape(city)
```

---

For more examples, see the test suite in `tests/` directory.
