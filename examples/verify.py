"""
Verify PDF digital signatures using ContractLayer API.

Usage:
    python verify.py contract.pdf

Requirements:
    pip install requests
"""

import sys
import requests

API_URL = "https://api.econtract.online/verify-pdf"


def verify_pdf(file_path: str) -> dict:
    """Verify digital signatures in a PDF file."""
    with open(file_path, "rb") as f:
        response = requests.post(API_URL, files={"file": f})
    response.raise_for_status()
    return response.json()


def print_report(result: dict):
    """Print a human-readable verification report."""
    doc = result["document"]
    summary = result["summary"]

    print(f"\n📄 File: {doc['filename']} ({doc['size']:,} bytes)")
    print(f"🔐 Hash: {doc['hash']}")
    print(f"🔒 Tampered: {'🚨 YES!' if doc['tampered'] else '✅ No'}")
    print(f"\n📊 Signatures: {summary['total']} total, {summary['valid']} valid, {summary['invalid']} invalid")

    verdict_icons = {
        "all_valid": "✅",
        "has_invalid": "❌",
        "no_signatures": "⚠️",
    }
    icon = verdict_icons.get(summary["verdict"], "❓")
    print(f"🏷️  Verdict: {icon} {summary['verdict']}")

    for i, sig in enumerate(result.get("signatures", []), 1):
        signer = sig["signer"]
        print(f"\n--- Signature #{i} ---")
        print(f"  Name:         {signer.get('name', 'Unknown')}")
        print(f"  Email:        {signer.get('email', 'N/A')}")
        print(f"  Organization: {signer.get('organization', 'N/A')}")
        print(f"  Country:      {signer.get('country', 'N/A')}")
        print(f"  Signed at:    {sig.get('signed_at', 'N/A')}")
        print(f"  Verdict:      {'✅' if sig['verdict'] == 'valid' else '❌'} {sig['verdict']}")
        print(f"  Integrity:    {'✅' if sig['integrity'] else '❌'}")
        print(f"  Signature:    {'✅' if sig['signature'] else '❌'}")
        print(f"  Chain:        {'✅' if sig['chain'] else '❌'}")
        print(f"  Expired:      {'⚠️ Yes' if sig['expired'] else '✅ No'}")

    print(f"\n🕐 Verified at: {result['verified_at']}")
    print(f"🔗 Verified by: {result['verified_by']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify.py <pdf-file>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"🔍 Verifying: {file_path}")

    try:
        result = verify_pdf(file_path)
        print_report(result)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e.response.status_code} — {e.response.text}")
        sys.exit(1)
