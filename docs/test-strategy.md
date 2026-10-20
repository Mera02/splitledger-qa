# SplitLedger QA Test Strategy

## 1. Purpose

This repository provides independent quality assurance for SplitLedger.

The QA project tests the application externally through its public interfaces rather than importing its internal business logic.

The main testing surfaces are:

- REST API
- Command-line interface
- React user interface
- Cross-layer consistency

## 2. Testing Approach

The project uses a risk-based testing approach.

The highest-risk area is financial correctness because incorrect splitting, balances, or settlements could produce incorrect monetary results.

Testing therefore focuses on:

- monetary validation
- deterministic equal splitting
- balance correctness
- settlement correctness
- validation failures
- consistency between API, CLI, and UI

## 3. Test Levels

### API Testing

API tests use `httpx` to interact with the running FastAPI application.

Coverage includes:

- health checks
- group creation
- member creation
- expense creation
- balances
- settlements
- boundary values
- invalid input
- business-rule validation

### CLI Testing

CLI tests execute the real SplitLedger CLI through Python `subprocess`.

The QA repository does not import the CLI implementation directly.

Coverage includes:

- group creation
- member creation
- expense creation
- balance output
- settlement output
- JSON output
- invalid values
- invalid payer relationships
- duplicate members

### UI Testing

UI tests use Playwright to interact with the React application through a real browser.

Coverage includes:

- application loading
- group creation
- member creation
- expense creation
- visible balances
- visible settlements

### Cross-Layer Testing

Cross-layer tests verify that the API, CLI, and UI produce results that agree with an independently defined expected result.

The test does not assume that agreement between application layers proves correctness.

Instead, each layer is compared against an independent oracle.

## 4. Financial Test Oracle

Monetary expectations are calculated independently from the application implementation.

Example:

An expense of `100.00 BAM` equals `10000` cents.

For three members:

- first member share: `3334` cents
- second member share: `3333` cents
- third member share: `3333` cents

If the first member paid the full amount, expected balances are:

- payer: `+6666` cents
- member 2: `-3333` cents
- member 3: `-3333` cents

The sum of all balances must always equal zero.

## 5. Key Invariants

The test suite checks important financial invariants:

- expense shares must sum to the original expense amount
- balances must sum to zero
- money must not be created or lost
- settlement amounts must be positive
- payer must belong to the group
- duplicate member names within a group are rejected

## 6. Test Isolation

API tests use unique group names to reduce collisions between test runs.

CLI tests use temporary SQLite databases where isolation is required.

Cross-layer tests intentionally use the running application's shared database so that API, CLI, and UI can observe the same state.

## 7. Current Scope

The current MVP supports:

- BAM currency
- equal expense splitting
- groups
- members
- expenses
- balances
- settlements

Out of scope for the current QA scope:

- authentication
- multiple currencies
- percentage splits
- unequal custom splits
- production load testing