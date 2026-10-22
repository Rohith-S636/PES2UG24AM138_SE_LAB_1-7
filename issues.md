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

## Known issue table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| AES-ECB PAN encryption (Bandit B305) | Security | 77 | ECB encrypted identical PAN input deterministically and did not authenticate ciphertext. | Replace ECB with AES-GCM, use a fresh 12-byte nonce for every call, and pass the key explicitly. **After:** Bandit reports no issues; repeated synthetic encryptions differ. |
| Weak RSA key (Bandit B505) | Security | 83 | The original signing key used `key_size=1024`, which Bandit identifies as breakable. | Increase the RSA key size to 2048 bits. **After:** the program reports key size 2048. |
| Unsafe XML parsing (Bandit B408/B318) | Security | 5, 86 | `xml.dom.minidom` was used to parse untrusted XML, and required elements were accessed without validation. | Use `defusedxml.minidom.parseString`, catch parser/security exceptions, validate `salary` and `tds`, and raise clear `ValueError` exceptions. **After:** Bandit reports no issues and XML error tests pass. |
| CGI handler exposure (Bandit B412) | Security | 6, 91–92 | Unneeded `CGIHandler` support added a security-sensitive web integration surface. | Remove the import and `runAsCgi` function because CGI is not required by this calculator; update the README. **After:** Bandit reports no issues. |
| Bare exception and weak PAN matching (Pylint W0702, Flake8 E722) | Bug / Input validation | 70–74 | A bare `except:` hid all errors, and `re.match` was not anchored, so extra characters could be accepted. | Validate the input type and use an anchored compiled pattern with `fullmatch`; remove unnecessary exception handling. **After:** PAN boundary tests pass and both tools are clean. |
| Unused imports and variables (Pylint/Flake8) | Code quality | 2–4, 36 | `os`, `sys`, `json`, `bracket`, and `checked` were unused. | Remove unused imports and variables. **After:** no unused-code findings remain. |
| Non-snake-case identifiers (Pylint C0103) | Code quality | 18–92 | Functions and variables such as `slabRate`, `newRegimeTax`, and `parseForm16` violated Python naming conventions. | Rename identifiers to `snake_case` and update all call sites. **After:** Pylint is clean. |
| Missing documentation (Pylint C0114/C0116) | Code quality | 1, 18–106 | The module and functions lacked useful docstrings. | Add a module docstring and concise function docstrings describing behavior and validation. **After:** Pylint is clean. |
| Formatting and layout findings (Pylint/Flake8) | Code quality | 16, 18–106 | The baseline included long lines, missing blank lines, semicolon-separated statements, unnecessary `elif`, and `%` formatting. | Wrap long lines, use required blank lines, split statements, simplify control flow, and use f-strings. **After:** Flake8 reports zero diagnostics and Pylint is 10.00/10. |
| Unnecessary function arguments (Pylint W0613) | Code quality | 85, 91 | `strict` and `debug` were accepted but unused. | Remove the unused arguments with their unused CGI function. **After:** no unused-argument findings remain. |
| Non-progressive new-regime tax (Logic bug) | Bug | 34–40 | The original code applied one marginal rate to all taxable income instead of taxing each slab band separately. | Add one documented slab table and a progressive helper that taxes only the income portion in each band; test boundaries and rebate behavior. **After:** boundary checks pass; calculation remains educational, not tax advice. |
| Repeated PAN ciphertext (Behavioral security issue) | Security / Test | 76–80, 98–104 | The original demonstration showed that encrypting the same PAN twice produced identical output. | Use AES-GCM with a fresh nonce and test two synthetic encryptions for inequality. **After:** equality test returns `False`. |
| Age-80 exemption boundary | Logic bug | 43–47 | The original `age > 80` condition treated age 80 as a lower exemption category. | Use the documented inclusive boundary `age >= 80` and test age 80 explicitly. **After:** age 80 returns the senior exemption of 500000. |

## Validation evidence

- `python -m py_compile tax_calculator.py`: passed.
- `python tax_calculator.py`: passed; reports AES-GCM ciphertext differs and RSA
  key size is 2048.
- Synthetic tax boundary, PAN, valid XML, and missing XML value checks: passed.
- `pylint_report_after.txt`: 10.00/10.
- `bandit_report_after.txt`: no issues, no skipped findings.
- `flake8_report_after.txt`: empty, meaning no diagnostics.

These calculations are educational examples and are not official tax advice.
