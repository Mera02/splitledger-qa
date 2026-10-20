# SplitLedger Requirements Traceability

| Requirement | API | CLI | UI | Cross-Layer |
|---|---:|---:|---:|---:|
| Create group | ✓ | ✓ | ✓ | ✓ |
| Add member | ✓ | ✓ | ✓ | ✓ |
| Record expense | ✓ | ✓ | ✓ | ✓ |
| Select payer | ✓ | ✓ | ✓ | ✓ |
| Equal split | ✓ | ✓ | ✓ | ✓ |
| View balances | ✓ | ✓ | ✓ | ✓ |
| View settlements | ✓ | ✓ | ✓ | ✓ |
| Reject zero amount | ✓ |  |  |  |
| Reject negative amount | ✓ | ✓ |  |  |
| Reject excess decimal precision | ✓ |  |  |  |
| Reject payer outside group | ✓ | ✓ |  |  |
| Reject duplicate member | ✓ | ✓ |  |  |
| Minimum amount boundary | ✓ |  |  |  |
| Balance conservation | ✓ | ✓ |  | ✓ |
| Machine-readable CLI output |  | ✓ |  | ✓ |
| Browser workflow |  |  | ✓ | ✓ |

## Coverage Notes

The matrix shows functional coverage across independent application surfaces.

Not every requirement is intentionally duplicated at every layer.

Detailed monetary validation is primarily covered through API and CLI tests, while the UI suite focuses on high-value user workflows.

Cross-layer tests are used for selected high-risk financial scenarios instead of repeating the complete regression suite through every interface.

This approach keeps the suite focused, reduces unnecessary duplication, and provides strong coverage of the highest-risk SplitLedger functionality.