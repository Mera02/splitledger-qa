# SplitLedger Exploratory Testing Notes

## Purpose

Exploratory testing was used alongside automated testing to investigate areas where unexpected user behavior, state changes, or integration issues could reveal problems that scripted tests might miss.

The focus was on financial correctness, validation, usability, and consistency between application layers.

---

## Charter 1 — Expense Amount Validation

**Goal:** Explore how the application behaves when users enter unusual or invalid monetary values.

**Areas explored:**
- zero amount
- negative amount
- minimum valid amount
- more than two decimal places
- non-numeric input
- very large values

**Questions:**
- Does the application reject invalid input cleanly?
- Are invalid values prevented from reaching persistence?
- Does the application return a controlled error instead of crashing?
- Are valid boundary values processed correctly?

**Automated follow-up coverage:**
- `0.00`
- `-10.00`
- `0.01`
- `12.345`

---

## Charter 2 — Group and Member Validation

**Goal:** Explore member and group creation behavior.

**Areas explored:**
- duplicate member names
- different capitalization
- surrounding whitespace
- empty names
- members belonging to different groups

**Questions:**
- Are duplicate members prevented?
- Is name normalization consistent?
- Can a member from one group incorrectly act as payer in another group?
- Are invalid names handled without application crashes?

**Observed behavior:**
- Duplicate member names are rejected after normalization.
- A payer from another group is rejected.
- Invalid operations return controlled errors.

---

## Charter 3 — Financial Consistency

**Goal:** Explore whether SplitLedger preserves financial invariants after expenses are created.

**Areas explored:**
- equal splitting
- remainder cents
- multiple members
- multiple expenses
- different payers

**Key invariants checked:**
- Sum of expense shares equals the original expense amount.
- Sum of all member balances equals zero.
- No cents are created or lost.
- Settlement amounts are positive.
- Settlements resolve debtor and creditor balances consistently.

**Example explored:**

`100.00 BAM` split between three members:

- Member 1 share: `33.34 BAM`
- Member 2 share: `33.33 BAM`
- Member 3 share: `33.33 BAM`

When member 1 pays the full amount:

- Member 1 balance: `+66.66 BAM`
- Member 2 balance: `-33.33 BAM`
- Member 3 balance: `-33.33 BAM`

The total balance remains `0.00 BAM`.

---

## Charter 4 — Cross-Interface Consistency

**Goal:** Explore whether API, CLI, and UI represent the same underlying financial state consistently.

**Approach:**
1. Create test data.
2. Read balances through the API.
3. Read balances through the CLI.
4. Inspect balances through the UI.
5. Compare each result against an independent expected result.

**Questions:**
- Does every interface observe the same stored state?
- Do all interfaces represent balances consistently?
- Can one interface update data that another interface fails to observe?
- Are rounding rules consistent across interfaces?

**Observed behavior:**
- Data created through the CLI was visible through the React UI.
- Data created through the API was visible through the CLI and UI.
- API, CLI, and UI returned equivalent balance results in the tested cross-layer scenario.

---

## Charter 5 — UI Workflow and Usability

**Goal:** Explore the main user workflow through the React interface.

**Workflow explored:**
1. Create a group.
2. Add members.
3. Create an expense.
4. Select a payer.
5. Review expense history.
6. Review balances.
7. Review suggested settlements.
8. Switch between groups.

**Observed behavior:**
- Newly created groups appear immediately in the sidebar.
- Newly added members appear without requiring a manual page refresh.
- Expense creation updates expense history, balances, and settlements.
- Empty groups display appropriate empty states.
- Switching groups updates the visible data.

---

## Test Automation Observations

During UI automation, a Playwright locator initially matched multiple visible elements containing the same member name.

For example, `Faris` appeared in:
- the Members section
- the payer dropdown
- the Balances section

The test was improved by scoping locators to the relevant UI section.

This was a test automation issue rather than a confirmed application defect.

A separate pytest collection issue occurred because API and UI test files initially shared the same filename.

The files were renamed to use unique test module names.

This was also a test infrastructure issue rather than an application defect.

---

## Confirmed Product Defects

No confirmed SplitLedger product defects have been recorded from the exploratory sessions completed so far.

Only defects that are reproduced and verified against expected behavior should be added to this section.