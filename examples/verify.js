/**
 * Verify PDF digital signatures using ContractLayer API.
 *
 * Usage:
 *   node verify.js contract.pdf
 *
 * Requirements:
 *   Node.js 18+ (native fetch)
 */

const fs = require("fs");
const path = require("path");

const API_URL = "https://api.econtract.online/verify-pdf";

async function verifyPdf(filePath) {
  const file = fs.readFileSync(filePath);
  const fileName = path.basename(filePath);

  const form = new FormData();
  form.append("file", new Blob([file], { type: "application/pdf" }), fileName);

  const res = await fetch(API_URL, { method: "POST", body: form });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(`API error ${res.status}: ${error.message || res.statusText}`);
  }

  return res.json();
}

function printReport(result) {
  const { document: doc, signatures, summary } = result;

  console.log(`\n📄 File: ${doc.filename} (${doc.size.toLocaleString()} bytes)`);
  console.log(`🔐 Hash: ${doc.hash}`);
  console.log(`🔒 Tampered: ${doc.tampered ? "🚨 YES!" : "✅ No"}`);
  console.log(`\n📊 Signatures: ${summary.total} total, ${summary.valid} valid, ${summary.invalid} invalid`);

  const icons = { all_valid: "✅", has_invalid: "❌", no_signatures: "⚠️" };
  console.log(`🏷️  Verdict: ${icons[summary.verdict] || "❓"} ${summary.verdict}`);

  signatures.forEach((sig, i) => {
    const s = sig.signer;
    console.log(`\n--- Signature #${i + 1} ---`);
    console.log(`  Name:         ${s.name || "Unknown"}`);
    console.log(`  Email:        ${s.email || "N/A"}`);
    console.log(`  Organization: ${s.organization || "N/A"}`);
    console.log(`  Signed at:    ${sig.signed_at || "N/A"}`);
    console.log(`  Verdict:      ${sig.verdict === "valid" ? "✅" : "❌"} ${sig.verdict}`);
  });

  console.log(`\n🕐 Verified at: ${result.verified_at}`);
}

// CLI
const filePath = process.argv[2];
if (!filePath) {
  console.log("Usage: node verify.js <pdf-file>");
  process.exit(1);
}

console.log(`🔍 Verifying: ${filePath}`);
verifyPdf(filePath)
  .then(printReport)
  .catch((err) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  });
