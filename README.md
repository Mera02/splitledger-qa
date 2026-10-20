# SplitLedger QA

Independent quality assurance and test automation project for SplitLedger.

This repository tests the SplitLedger application externally through its public interfaces rather than importing its internal business logic.

The goal is to verify financial correctness, validation, user workflows, and consistency across the REST API, command-line interface, and React user interface.

---

## Testing Scope

The QA suite currently covers four main areas:

- REST API testing
- CLI testing
- UI end-to-end testing
- Cross-layer consistency testing

The highest-risk area is financial correctness, especially:

- equal expense splitting
- remainder handling
- balances
- settlements
- monetary validation
- cross-interface consistency

---

## Technology Stack

- Python 3.11
- pytest
- httpx
- Playwright
- subprocess
- Chromium

---

## Test Architecture

```text
                     Independent Oracle
                    /        |        \
                   /         |         \
               REST API     CLI        UI
                httpx    subprocess  Playwright
                   \         |         /
                    \        |        /
                      SplitLedger
```

The QA repository does not import SplitLedger's internal service or domain code.

This helps keep the automated tests independent from the implementation being tested.

---

## Project Structure

```text
splitledger-qa/
├── docs/
│   ├── exploratory-testing.md
│   ├── test-cases.md
│   ├── test-strategy.md
│   └── traceability.md
│
├── tests/
│   ├── api/
│   │   ├── conftest.py
│   │   ├── test_expense_flow.py
│   │   ├── test_health.py
│   │   └── test_validation.py
│   │
│   ├── cli/
│   │   ├── conftest.py
│   │   ├── test_cli_flow.py
│   │   └── test_cli_validation.py
│   │
│   ├── cross_layer/
│   │   ├── conftest.py
│   │   └── test_cross_layer_balances.py
│   │
│   └── ui/
│       ├── test_smoke.py
│       └── test_ui_expense_flow.py
│
└── README.md
```

---

## API Testing

API tests use `httpx` against the running FastAPI application.

Coverage includes:

- health check
- group creation
- member creation
- expense creation
- balances
- settlements
- minimum valid amount
- zero amount rejection
- negative amount rejection
- decimal precision validation
- payer-group validation
- duplicate member validation

Example scenario:

```text
Create group
    ↓
Add Faris, Ada, Amar
    ↓
Create 100.00 BAM expense
    ↓
Faris pays
    ↓
Verify balances
    ↓
Verify settlements
```

Expected balances:

```text
Faris   +66.66 BAM
Ada     -33.33 BAM
Amar    -33.33 BAM
```

---

## CLI Testing

CLI tests execute the real SplitLedger command-line interface using Python `subprocess`.

The tests verify:

- process exit codes
- machine-readable JSON output
- group creation
- member creation
- expense creation
- balances
- settlements
- invalid monetary input
- duplicate members
- invalid payer relationships

CLI tests use isolated temporary SQLite databases where appropriate.

---

## UI Testing

UI tests use Playwright with Chromium.

The automated browser tests verify that a user can:

1. Open SplitLedger.
2. Create a group.
3. Add members.
4. Create an expense.
5. Select a payer.
6. View expense history.
7. View balances.
8. View suggested settlements.

Locators are based primarily on accessible roles, labels, and visible user-facing text.

---

## Cross-Layer Testing

Cross-layer testing verifies the same financial scenario through multiple application interfaces.

A test scenario is created and checked through:

- API
- CLI
- UI

Each result is compared against an independently defined expected result.

For example:

```text
100.00 BAM
3 members
Faris pays
```

Independent expected result:

```text
Faris   +6666 cents
Ada     -3333 cents
Amar    -3333 cents
```

The API, CLI, and UI must each represent this result correctly.

Agreement between application layers alone is not treated as proof of correctness because multiple layers could share the same underlying defect.

---

## Financial Invariants

Important invariants include:

- expense shares sum to the original expense amount
- member balances sum to zero
- money is not created or lost
- settlement amounts are positive
- payer must belong to the group
- duplicate member names within a group are rejected

---

## Setup

Create and activate a virtual environment.

### Windows

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Install dependencies:

```cmd
python -m pip install pytest httpx pytest-playwright
python -m playwright install chromium
```

---

## Running the System Under Test

The SplitLedger application repository must be available separately.

Start the FastAPI backend from the SplitLedger repository:

```cmd
cd backend
uvicorn app.main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

Start the React frontend:

```cmd
cd frontend
npm run dev
```

The UI should be available at:

```text
http://localhost:5173
```

---

## Running the Tests

Run the complete QA suite:

```cmd
python -m pytest -v
```

Run only API tests:

```cmd
python -m pytest tests/api -v
```

Run only CLI tests:

```cmd
python -m pytest tests/cli -v
```

Run only UI tests:

```cmd
python -m pytest tests/ui -v
```

Run UI tests with a visible browser:

```cmd
python -m pytest tests/ui -v --headed
```

Run cross-layer tests:

```cmd
python -m pytest tests/cross_layer -v
```

---

## QA Documentation

Additional QA documentation is available in the `docs/` directory:

- `test-strategy.md` — testing approach and risk priorities
- `test-cases.md` — documented test scenarios and expected results
- `traceability.md` — requirement-to-test coverage mapping
- `exploratory-testing.md` — exploratory testing charters and observations

---

## Testing Principles

The project follows several testing principles:

- test externally where possible
- prioritize high-risk financial behavior
- use deterministic expected results
- keep test data isolated where appropriate
- test boundaries and invalid input
- avoid unnecessary duplication across layers
- distinguish test infrastructure failures from product defects
- never report a defect without reproducing and verifying it