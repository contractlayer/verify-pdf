#!/bin/bash
# Verify a signed PDF using ContractLayer API
# Usage: ./verify.sh contract.pdf

if [ -z "$1" ]; then
  echo "Usage: ./verify.sh <pdf-file>"
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "Error: File '$1' not found"
  exit 1
fi

echo "🔍 Verifying: $1"
echo ""

RESPONSE=$(curl -s -X POST https://api.econtract.online/verify-pdf \
  -F "file=@$1")

VERDICT=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['summary']['verdict'])" 2>/dev/null)
TAMPERED=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['document']['tampered'])" 2>/dev/null)
TOTAL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['summary']['total'])" 2>/dev/null)

if [ "$VERDICT" = "all_valid" ]; then
  echo "✅ Verdict: ALL VALID ($TOTAL signature(s))"
elif [ "$VERDICT" = "no_signatures" ]; then
  echo "⚠️  Verdict: No signatures found"
else
  echo "❌ Verdict: $VERDICT"
fi

if [ "$TAMPERED" = "True" ]; then
  echo "🚨 WARNING: Document has been TAMPERED with!"
else
  echo "🔒 Document integrity: OK"
fi

echo ""
echo "Full response:"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
