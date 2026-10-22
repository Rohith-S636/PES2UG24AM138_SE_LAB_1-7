# Lab 5 — Static Analysis Issue Log

Project: `L5_53_income-tax-calculator`

## Baseline and after results

| Tool | Before | After |
|---|---|---|
| Pylint | 4.57/10 | 10.00/10 |
| Bandit | 6 findings: 1 low, 3 medium, 2 high | No issues identified; 0 skipped |
| Flake8 | 23 diagnostic lines | 0 diagnostic lines |

The baseline files were preserved unchanged. The after reports were generated
from the final `tax_calculator.py`.

## Issue and fix register

| ID | Baseline evidence | Fix applied | After result |
|---|---|---|---|
| SEC-01 | Bandit B305: AES ECB mode in `encryptPan` | Replaced ECB with AES-GCM, a fresh 12-byte nonce, and an explicit key parameter | Resolved; Bandit reports no issues |
| SEC-02 | Bandit B505: RSA `key_size=1024` | Increased the RSA key size to 2048 bits | Resolved; program reports 2048 |
| SEC-03 | Bandit B408/B318: `minidom` import and `parseString` | Used `defusedxml.minidom.parseString`; malformed XML and missing values raise `ValueError` | Resolved; Bandit reports no issues and error checks pass |
| SEC-04 | Bandit B412: `CGIHandler` import/use | Removed CGI functionality because it is not required by the calculator lab; updated README | Resolved; Bandit reports no issues |
| QUAL-01 | Pylint W0702; Flake8 E722: bare `except:` | Replaced broad handling with type checks and specific exception tuples | Resolved; Pylint and Flake8 are clean |
| QUAL-02 | Unused imports `os`, `sys`, `json` | Removed unused imports | Resolved |
| QUAL-03 | Unused `bracket`, `checked` | Removed unused variables | Resolved |
| QUAL-04 | Pylint C0103: camelCase names | Renamed functions and variables to `snake_case` | Resolved |
| QUAL-05 | Pylint C0114/C0116: missing docstrings | Added module and function docstrings | Resolved |
| QUAL-06 | Pylint C0321; Flake8 E702 | Split multiple statements onto separate lines | Resolved |
| QUAL-07 | Pylint C0301; Flake8 E501 | Wrapped long lines | Resolved |
| QUAL-08 | Pylint R1705 | Simplified return control flow | Resolved |
| QUAL-09 | Pylint R1716 | Used the chained comparison `60 <= age < 80` | Resolved |
| QUAL-10 | Pylint R0911: too many returns in `slabRate` | Replaced repeated returns with a table-driven lookup | Resolved |
| QUAL-11 | Pylint W0613: unused `strict` and `debug` arguments | Removed both unused arguments along with CGI support | Resolved |
| QUAL-12 | Pylint C0209 | Replaced applicable formatting with f-strings | Resolved |
| TAX-01 | Original calculation applied one marginal rate to all taxable income | Added a documented progressive slab helper and checked slab/rebate boundaries | Boundary checks pass; educational calculation only |
| PAN-01 | Original output showed repeated PAN encryption was identical | AES-GCM uses a fresh nonce; repeated synthetic encryption differs | Test passed: `False` for equality |
| PAN-02 | Original PAN check accepted extra trailing characters | Added an anchored compiled pattern and `fullmatch` with type checking | Valid and invalid synthetic checks pass |

## Validation evidence

- `python -m py_compile tax_calculator.py`: passed.
- `python tax_calculator.py`: passed; reports AES-GCM ciphertext differs and RSA
  key size is 2048.
- Synthetic tax boundary, PAN, valid XML, and missing XML value checks: passed.
- `pylint_report_after.txt`: 10.00/10.
- `bandit_report_after.txt`: no issues, no skipped findings.
- `flake8_report_after.txt`: empty, meaning no diagnostics.

These calculations are educational examples and are not official tax advice.
