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
git clone https://github.com/tijothomas95/PytestPlaywrightAutomation.git
cd PytestPlaywrightAutomation
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
Spin up containers and by default tests run in chromium and generate allure report:
```bash
docker compose up --build
```

Run tests using firefox browser inside container and generate allure report:
```bash
docker compose run tests pytest -n auto --browser=firefox --alluredir=allure-results
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

<img width="1438" height="823" alt="Screenshot 2025-09-27 at 12 31 15" src="https://github.com/user-attachments/assets/8634bb0b-a67d-4e2b-a74f-0b84ac1190e6" />

<img width="1435" height="554" alt="image" src="https://github.com/user-attachments/assets/c37426ea-229c-441d-aa8c-390ebee14bb7" />

<img width="1440" height="773" alt="Screenshot 2025-09-27 at 12 31 29" src="https://github.com/user-attachments/assets/545a2391-1813-42d2-839d-36d78d085e97" />

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
