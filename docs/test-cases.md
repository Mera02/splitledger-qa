# SplitLedger Test Cases

## TC-API-001 — Health Check

**Type:** Smoke  
**Layer:** API

**Steps:**
1. Send `GET /api/health`.
2. Inspect the response.

**Expected Result:**
- HTTP status is `200`.
- Response body is:

```json
{
  "status": "ok"
}
```

---

## TC-API-002 — Complete Equal Split Flow

**Type:** Positive / Regression  
**Layer:** API

**Preconditions:**
- SplitLedger API is running.

**Steps:**
1. Create a group.
2. Add Faris, Ada, and Amar.
3. Create an expense of `100.00 BAM`.
4. Set Faris as payer.
5. Request balances.
6. Request settlements.

**Expected Result:**
- Faris balance is `+6666` cents.
- Ada balance is `-3333` cents.
- Amar balance is `-3333` cents.
- Sum of balances equals zero.
- Ada owes Faris `3333` cents.
- Amar owes Faris `3333` cents.

---

## TC-API-003 — Minimum Valid Amount

**Type:** Boundary  
**Layer:** API

**Steps:**
1. Create a group with three members.
2. Create an expense of `0.01 BAM`.
3. Request balances.

**Expected Result:**
- Expense is accepted.
- Exactly one cent is distributed.
- No money is created or lost.
- Sum of balances equals zero.

---

## TC-API-004 — Reject Zero Amount

**Type:** Negative / Boundary  
**Layer:** API

**Input:**

```text
0.00
```

**Expected Result:**
- HTTP status is `400`.
- Expense is rejected.
- Error states that the amount must be greater than zero.

---

## TC-API-005 — Reject Negative Amount

**Type:** Negative  
**Layer:** API

**Input:**

```text
-10.00
```

**Expected Result:**
- HTTP status is `400`.
- Expense is rejected.

---

## TC-API-006 — Reject Excess Decimal Precision

**Type:** Negative / Boundary  
**Layer:** API

**Input:**

```text
12.345
```

**Expected Result:**
- HTTP status is `400`.
- Expense is rejected because more than two decimal places are not allowed.

---

## TC-API-007 — Reject Payer Outside Group

**Type:** Business Rule / Negative  
**Layer:** API

**Steps:**
1. Create group A.
2. Create group B.
3. Add a member to group B.
4. Attempt to use that member as payer for an expense in group A.

**Expected Result:**
- HTTP status is `400`.
- Expense is rejected.
- Error indicates that the payer must belong to the group.

---

## TC-API-008 — Reject Duplicate Member

**Type:** Business Rule / Negative  
**Layer:** API

**Steps:**
1. Add member `Faris`.
2. Attempt to add `  FARIS  ` to the same group.

**Expected Result:**
- HTTP status is `400`.
- Duplicate member is rejected after name normalization.

---

## TC-CLI-001 — Complete CLI Flow

**Type:** Positive / Regression  
**Layer:** CLI

**Steps:**
1. Create a group using the CLI.
2. Add Faris and Ada.
3. Create a `90.00 BAM` expense paid by Faris.
4. Request balances using `--json`.
5. Request settlements using `--json`.

**Expected Result:**
- Faris balance is `+4500` cents.
- Ada balance is `-4500` cents.
- Ada owes Faris `4500` cents.
- CLI exits successfully.

---

## TC-CLI-002 — Reject Negative Expense

**Type:** Negative  
**Layer:** CLI

**Expected Result:**
- CLI exits with code `1`.
- JSON output contains an error.
- Negative amount is rejected.

---

## TC-CLI-003 — Reject Duplicate Member

**Type:** Negative / Business Rule  
**Layer:** CLI

**Expected Result:**
- CLI exits with code `1`.
- Duplicate member is rejected.

---

## TC-CLI-004 — Reject Payer Outside Group

**Type:** Negative / Business Rule  
**Layer:** CLI

**Expected Result:**
- CLI exits with code `1`.
- Expense is rejected because the payer does not belong to the group.

---

## TC-UI-001 — Application Smoke Test

**Type:** Smoke  
**Layer:** UI

**Expected Result:**
- SplitLedger heading is visible.
- New group button is visible.
- Members section is visible.
- Add expense section is visible.

---

## TC-UI-002 — Complete Expense Flow

**Type:** End-to-End / Regression  
**Layer:** UI

**Steps:**
1. Open SplitLedger.
2. Create a new group.
3. Add Faris.
4. Add Ada.
5. Add a `90.00 BAM` expense paid by Faris.
6. Inspect balances.
7. Inspect settlements.

**Expected Result:**
- Expense appears in expense history.
- Faris displays `+45.00 KM`.
- Ada displays `-45.00 KM`.
- Settlement displays `Ada → Faris`.
- Settlement amount is `45.00 KM`.

---

## TC-CROSS-001 — Cross-Layer Balance Consistency

**Type:** Cross-Layer / Regression  
**Layers:** API, CLI, UI

**Scenario:**
- Three members.
- `100.00 BAM` expense.
- Faris pays.

**Independent Expected Result:**

```text
Faris: +6666 cents
Ada:   -3333 cents
Amar:  -3333 cents
```

**Verification:**
- API result matches the independent oracle.
- CLI result matches the independent oracle.
- UI representation matches the independent oracle.

**Invariant:**
- Sum of balances equals zero.