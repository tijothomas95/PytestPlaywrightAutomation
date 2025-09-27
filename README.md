# Pytest + Playwright Automation Framework

This repository contains an **end-to-end test automation framework** built with [Pytest](https://docs.pytest.org), [Playwright](https://playwright.dev/python/), [Allure Reporting](https://allurereport.org/) and uses [GitHub Actions CICD](https://docs.github.com/en/actions/get-started/quickstart).  
It supports running tests **locally** and inside **Docker Compose**, with parallel execution and cross-browser support.  

---

## Tech Stack
- **Test Runner**: `pytest`
- **Browsers**: `chromium`, `firefox`, `webkit`  
- **Framework**: `playwright` + `pytest-playwright`
- **Parallel Execution**: `pytest-xdist`
- **Reporting**: `allure-pytest`, `pytest-html`
- **Test Data**: `faker`

---

## CI/CD Pipeline (GitHub Actions)

This project uses **GitHub Actions** for automated CI/CD.  
Every push or pull request to `main` will:

1. **Set up environment**  
   - Python 
   - Dependencies

2. **Run tests in Docker / Playwright**  
   - Parallel execution with `pytest-xdist`  
   - Retry on failure (`pytest-rerunfailures`)  

3. **Generate Allure Report**  
   - Test results uploaded as artifacts  
   - Published to GitHub Pages for live viewing  

---

## Installation

### Clone the repo
```bash
git clone https://github.com/your-org/pytest-playwright-automation.git
cd pytest-playwright-automation
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Install browsers (first-time setup)
```bash
playwright install
```

---

## Running Tests

### Local Run
Run all tests in **Chromium**:
```bash
pytest --browser=chromium
```

Run **smoke tests** in **Firefox**:
```bash
pytest -m smoke --browser=firefox
```

Run in **parallel** across CPU cores:
```bash
pytest -n auto --browser=chromium
```

---

### Docker Run
Spin up containers:
```bash
docker compose up --build
```

Run tests inside container:
```bash
docker compose run tests pytest -n auto --browser=firefox
```

Tear down:
```bash
docker compose down
```

---

## Reporting

### Allure Reports
Generate results:
```bash
pytest -n auto -m smoke --browser=chromium --alluredir=allure-results
```

Open report:
```bash
allure serve allure-results
```

### HTML Report
```bash
pytest --html=report.html --self-contained-html
```

---

## Demo
Recording attachement: https://github.com/tijothomas95/PytestPlaywrightAutomation/releases/tag/v1.0.0

---

## Pytest Markers
Markers are defined in `pytest.ini`:

- `@pytest.mark.smoke` → Quick validation tests
- `@pytest.mark.regression` → Full regression suite

---

## Supported Browsers
This framework supports:
- `chromium`
- `firefox`
- `webkit`

Pass via CLI:
```bash
pytest --browser=firefox
```

---

## Project Structure

```
├── src/
│   ├── model/           # Page objects
│   ├── tests/           # Test cases
│   └── utils/           # Helpers (logger, config, etc.)
├── pytest.ini           # Pytest configuration
├── requirements.txt     # Dependencies
├── docker-compose.yml   # Docker config
├── README.md            # Documentation
```

---

## Utilities
- **Logging** → Centralized logger for debugging
- **Faker** → Fake user data generation

---

