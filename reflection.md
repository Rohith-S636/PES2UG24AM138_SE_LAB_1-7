# Lab 5 — Reflection

## 1. Which issues were most important?

The most important issues were the AES-ECB encryption, unsafe XML parsing, and
the weak 1024-bit RSA key. ECB reveals patterns and does not authenticate the
message, while unsafe XML parsing can expose applications to XML attacks. The
RSA key was below the minimum strength expected by the Bandit check. Removing
the unused CGI integration also removed an unrelated security surface.

## 2. What changed in the tax calculation?

The original new-regime calculation selected one rate and multiplied that rate
by all taxable income. The corrected implementation applies each slab rate
only to the income in that slab. It also clamps negative taxable income,
applies the configured rebate at the documented boundary, and keeps cess
separate in the final calculation. The slab values remain the educational
values configured by the lab and are not official tax advice.

## 3. How was the result tested?

The source compiled successfully and the demonstration ran successfully.
Additional synthetic checks covered slab and rebate boundaries, PAN strings
with extra characters, non-string PAN input, age 80, valid XML, and XML
missing a required value. The after reports then confirmed Pylint 10.00/10,
zero Bandit findings, and zero Flake8 diagnostics.

## 4. What would be different in production?

Production code would load encryption keys from a secret-management system
instead of generating a temporary demonstration key in `main`. It would use
authoritative, versioned tax rules, stronger domain validation for deductions
and monetary values, structured logging without sensitive data, automated
tests in continuous integration, and a review by a tax professional. A PAN
format check alone does not prove that a PAN was issued or is genuine.
