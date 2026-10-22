# Lab 5 — Static Analysis Issue Log

Project: `L5_53_income-tax-calculator`

## Baseline summary (before editing)

- Pylint: **4.57/10**, from `pylint_report_before.txt`.
- Bandit: **6 findings** — 1 low, 3 medium, 2 high, from `bandit_report_before.txt`.
- Flake8: **23 diagnostic lines**, counted from the supplied `flake8_report_before.txt`.

These are baseline results only. Fill the “After result” column after running the tools against the edited code.

## Issue and fix register

| ID | Baseline evidence | Planned fix | After result (fill from actual report) |
|---|---|---|---|
| SEC-01 | Bandit B305: AES ECB mode in `encryptPan` | Replace ECB with AES-GCM and a fresh random nonce; avoid hard-coded production keys | Pending after scan |
| SEC-02 | Bandit B505: RSA `key_size=1024` | Increase RSA key size to 2048 bits | Pending after scan |
| SEC-03 | Bandit B408/B318: `minidom` import and `parseString` | Use `defusedxml`; handle malformed XML and missing elements | Pending after scan |
| SEC-04 | Bandit B412: `CGIHandler` import/use | Remove CGI functionality if not required; otherwise document reviewed decision | Pending after scan |
| QUAL-01 | Pylint W0702; Flake8 E722: bare `except:` | Catch expected exceptions or remove unnecessary exception handling | Pending after scan |
| QUAL-02 | Pylint/Flake8: unused imports `os`, `sys`, `json` | Remove imports not used in final implementation | Pending after scan |
| QUAL-03 | Pylint/Flake8: unused `bracket`, `checked` | Remove or use meaningfully | Pending after scan |
| QUAL-04 | Pylint C0103: camelCase names | Convert to `snake_case`; update call sites | Pending after scan |
| QUAL-05 | Pylint C0114/C0116: missing module/function docstrings | Add useful docstrings | Pending after scan |
| QUAL-06 | Pylint C0321; Flake8 E702: multiple statements on one line | Split statements onto separate lines | Pending after scan |
| QUAL-07 | Pylint C0301; Flake8 E501: long lines | Wrap lines to configured limits | Pending after scan |
| QUAL-08 | Pylint R1705: unnecessary `elif` after `return` | Simplify control flow where appropriate | Pending after scan |
| QUAL-09 | Pylint R1716: chained comparison suggestion | Use `60 <= age < 80` if that matches the intended rule | Pending after scan |
| QUAL-10 | Pylint R0911: too many returns in `slabRate` | Simplify slab lookup using a documented table/helper | Pending after scan |
| QUAL-11 | Pylint W0613: unused `strict` and `debug` arguments | Remove if not required; otherwise implement/document | Pending after scan |
| QUAL-12 | Pylint C0209: formatting could use f-strings | Use clear f-strings where helpful | Pending after scan |
| TAX-01 | Original output includes slab-rate/tax diagnostics; source logic needs review | Verify progressive slab calculation and boundaries against lab rules | Pending tests |
| PAN-01 | Original output says repeated PAN encryption is identical | Confirm fresh AES-GCM nonce with synthetic test data | Pending test |
| PAN-02 | Original output says sample PAN format is valid | Use anchored format validation; note this does not prove authenticity | Pending test |

## Evidence to attach

- `pylint_report_before.txt`
- `bandit_report_before.txt`
- `flake8_report_before.txt`
- `pylint_report_after.txt`
- `bandit_report_after.txt`
- `flake8_report_after.txt`
- `baseline_output.txt`, if saved
- Screenshots of changed source and `git log -3 --oneline`, if requested

## Completion rule

For every row, record the actual after result, including remaining findings or test output. If an issue remains, state that explicitly. Do not write “fixed” unless the new report or a relevant test supports that conclusion.
