# Contributing to Housefinder

Thank you for your interest in contributing to Housefinder!

## Team Responsibilities

### Arman
**Areas:** Web Scraping, Data Filtering, Region Generation

**Tasks:**
- Implement and maintain web scrapers for all platforms
- Develop filtering and validation logic
- Optimize duplicate detection
- Improve region calculation algorithms
- Handle scraping edge cases and errors

### Denis
**Areas:** Data Management, Email Communication, Urgency Logic

**Tasks:**
- Manage Google Sheets integration
- Design and maintain email templates
- Implement urgency priority system
- Configure scheduling logic
- Setup email infrastructure

### Emir
**Areas:** WhatsApp Integration, AI Analysis, Results Management

**Tasks:**
- Implement WhatsApp Business API integration
- Develop webhook handlers for incoming messages
- Integrate GPT-4 for response analysis
- Manage results storage in Google Sheets
- Handle JSON mapping and data extraction

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/devshift-stack/Housefinder.git
cd Housefinder

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Follow Python PEP 8 style guidelines
- Add docstrings to all functions and classes
- Write unit tests for new functionality
- Update documentation as needed

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_models.py
```

### 5. Code Quality

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/
```

### 6. Commit Changes

```bash
git add .
git commit -m "feat: description of your feature"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `style:` - Code style changes

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style Guidelines

### Python Style

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where possible
- Follow PEP 8 conventions

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """
    pass
```

### Logging

Use appropriate log levels:

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Detailed information for debugging")
logger.info("General information about execution")
logger.warning("Warning about potential issues")
logger.error("Error occurred but program continues")
logger.critical("Critical error, program may stop")
```

## Testing Guidelines

### Unit Tests

- Test one thing per test
- Use descriptive test names
- Use fixtures for common setup
- Mock external dependencies

Example:

```python
import pytest
from src.models import Employee

class TestEmployee:
    """Test Employee model"""
    
    @pytest.fixture
    def employee(self):
        """Create test employee"""
        return Employee(
            name="Test",
            start_date="01.01.2026",
            location="Berlin",
            zip_code="12345",
            city="Berlin",
            state="Berlin"
        )
    
    def test_employee_creation(self, employee):
        """Test creating an employee"""
        assert employee.name == "Test"
        assert employee.city == "Berlin"
```

### Integration Tests

Test interactions between components:

```python
def test_scraping_and_filtering():
    """Test scraping followed by filtering"""
    scraper = MonteurzimmerScraper()
    listings = scraper.scrape("Berlin")
    
    filter = ListingFilter()
    filtered = filter.filter_listings(listings, employee)
    
    assert len(filtered) <= len(listings)
```

## Documentation

### Update README

When adding major features, update:
- Features section
- Usage examples
- Configuration options

### Add Inline Comments

Comment complex logic:

```python
# Calculate score based on distance, price, and amenities
# Distance: closer is better (up to 30 points)
# Price: within budget gets bonus (up to 20 points)
# Amenities: internet and parking add points (5 each)
score = self._calculate_score(result, employee)
```

## Project Structure

```
housefinder/
├── src/
│   ├── models/          # Data models (add new models here)
│   ├── scrapers/        # Web scrapers (add new platforms here)
│   ├── filters/         # Filtering logic
│   ├── communication/   # Email/WhatsApp senders
│   ├── ai/             # AI analysis modules
│   ├── sheets/         # Google Sheets integration
│   ├── utils/          # Utility functions
│   └── config/         # Configuration
├── tests/              # Test suite
├── data/               # Data storage
├── logs/               # Application logs
└── docs/               # Additional documentation
```

## Adding New Features

### Adding a New Scraper

1. Create file in `src/scrapers/new_scraper.py`
2. Inherit from `BaseScraper`
3. Implement `scrape()` method
4. Add to `src/scrapers/__init__.py`
5. Add tests in `tests/test_scrapers.py`
6. Update documentation

### Adding a New Filter

1. Add method to `ListingFilter` class
2. Write unit tests
3. Update filter workflow in main.py
4. Document the new filter

### Modifying Templates

1. Edit `src/communication/templates.py`
2. Test with sample data
3. Get approval from Denis before deploying

## Questions?

Contact the team leads:
- Arman (Scraping): arman@step2job.com
- Denis (Data/Email): denis@step2job.com
- Emir (WhatsApp/AI): emir@step2job.com

## License

Proprietary - Step2Job GmbH
