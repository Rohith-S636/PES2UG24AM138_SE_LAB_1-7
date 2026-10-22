"""Educational income-tax, PAN, and Form 16 processing examples."""

import re
import secrets
from xml.parsers.expat import ExpatError

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from defusedxml.common import DefusedXmlException
from defusedxml.minidom import parseString

STANDARD_DEDUCTION_NEW = 75000
STANDARD_DEDUCTION_OLD = 50000
REBATE_LIMIT_NEW = 1200000
CESS = 0.04
NEW_SLABS = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30),
]
OLD_SLABS = [
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]
PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")


def slab_rate(income):
    """Return the marginal new-regime rate for an income amount."""
    for upper_limit, rate in NEW_SLABS:
        if income <= upper_limit:
            return rate
    return NEW_SLABS[-1][1]


def _progressive_tax(income, slabs, starting_point=0):
    """Calculate tax progressively across the supplied upper-limit slabs."""
    taxable_income = max(0, income)
    tax_amount = 0.0
    lower_limit = starting_point
    for upper_limit, rate in slabs:
        band_income = min(taxable_income, upper_limit) - lower_limit
        if band_income > 0:
            tax_amount += band_income * rate
        lower_limit = upper_limit
        if taxable_income <= upper_limit:
            break
    return tax_amount


def new_regime_tax(salary):
    """Calculate educational new-regime tax after the standard deduction."""
    taxable = max(0, salary - STANDARD_DEDUCTION_NEW)
    tax_amount = _progressive_tax(taxable, NEW_SLABS)
    if taxable <= REBATE_LIMIT_NEW:
        tax_amount = 0
    return int(tax_amount * (1 + CESS))


def basic_exemption(age):
    """Return the educational old-regime exemption for the taxpayer's age."""
    if 60 <= age < 80:
        return 300000
    if age >= 80:
        return 500000
    return 250000


def old_regime_tax(salary, age, deductions):
    """Calculate educational old-regime tax with deductions and cess."""
    taxable = salary - STANDARD_DEDUCTION_OLD
    taxable -= sum(deductions.values())
    exemption = basic_exemption(age)
    tax_amount = _progressive_tax(taxable, OLD_SLABS, exemption)
    return int(tax_amount * (1 + CESS))


def better_regime(salary, age, deductions):
    """Return the regime with the lower educational tax estimate."""
    new_tax = new_regime_tax(salary)
    old_tax = old_regime_tax(salary, age, deductions)
    if new_tax > old_tax:
        return "old"
    return "new"


def is_valid_pan(pan):
    """Check PAN format; this does not verify that a PAN was issued."""
    return isinstance(pan, str) and PAN_PATTERN.fullmatch(pan) is not None


def encrypt_pan(pan, key):
    """Encrypt a PAN with AES-GCM and a fresh nonce."""
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes")
    nonce = secrets.token_bytes(12)
    ciphertext = AESGCM(key).encrypt(nonce, pan.encode("utf-8"), None)
    return nonce + ciphertext


def signing_key():
    """Generate a 2048-bit RSA signing key for the demonstration."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def parse_form16(xml_text):
    """Read salary and TDS from safe XML, raising ValueError for bad input."""
    try:
        document = parseString(xml_text)
    except (DefusedXmlException, ExpatError) as exc:
        raise ValueError("Form 16 contains malformed or unsafe XML") from exc

    salary_nodes = document.getElementsByTagName("salary")
    tds_nodes = document.getElementsByTagName("tds")
    if not salary_nodes or not salary_nodes[0].firstChild:
        raise ValueError("Form 16 is missing a salary value")
    if not tds_nodes or not tds_nodes[0].firstChild:
        raise ValueError("Form 16 is missing a TDS value")
    try:
        return (
            int(salary_nodes[0].firstChild.data),
            int(tds_nodes[0].firstChild.data),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Form 16 salary and TDS must be integers") from exc


def main():
    """Run synthetic examples without exposing real personal data."""
    print(f"New regime, salary 12,75,000: {new_regime_tax(1275000)}")
    print(f"New regime, salary 18,00,000: {new_regime_tax(1800000)}")
    deductions = {"80C": 200000, "80D": 30000}
    print(
        f"Old regime, salary 18,00,000: "
        f"{old_regime_tax(1800000, 35, deductions)}"
    )
    print(
        f"Better regime: {better_regime(1800000, 35, deductions)}"
    )
    print(f"Basic exemption at age 80: {basic_exemption(80)}")
    print(f"PAN format valid? {is_valid_pan('ABCDE1234F')}")
    temporary_key = AESGCM.generate_key(bit_length=128)
    first_ciphertext = encrypt_pan("ABCDE1234F", temporary_key)
    second_ciphertext = encrypt_pan("ABCDE1234F", temporary_key)
    print(
        "Same synthetic PAN encrypts the same way twice?",
        first_ciphertext == second_ciphertext,
    )
    print(
        "Form 16:",
        parse_form16("<form16><salary>1800000</salary><tds>150000</tds>"
                     "</form16>"),
    )
    print(f"Signing key size: {signing_key().key_size}")


if __name__ == "__main__":
    main()
