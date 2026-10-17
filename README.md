<p align="center">
  <img src="https://img.shields.io/badge/API-Live-brightgreen?style=flat-square" alt="API Status">
  <img src="https://img.shields.io/badge/Auth-Not%20Required-blue?style=flat-square" alt="No Auth">
  <img src="https://img.shields.io/badge/Rate%20Limit-50%2Fday-orange?style=flat-square" alt="Rate Limit">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

# 🔐 verify-pdf

**Verify digital signatures in any PDF.** One API call. No API key. Free.

Check who signed a document, when it was signed, and whether it's been tampered with.

```
POST https://api.econtract.online/verify-pdf
```

> 🌐 **Try it now** — [verify.econtract.online](https://verify.econtract.online)

---

## ⚡ Quick Start

```bash
curl -X POST https://api.econtract.online/verify-pdf \
  -F "file=@contract.pdf"
```

**Response:**

```json
{
  "document": {
    "filename": "contract.pdf",
    "hash": "sha256:a11f904a0b23f1c8...",
    "size": 245780,
    "tampered": false
  },
  "signatures": [
    {
      "signer": {
        "name": "John Doe",
        "email": "john@acme.com",
        "organization": "Acme Corp",
        "country": "US"
      },
      "signed_at": "2026-03-21T10:54:51.000Z",
      "verdict": "valid",
      "integrity": true,
      "signature": true,
      "chain": true,
      "expired": false,
      "certificate": {
        "issuer": "CN=eContract CA,O=eContract",
        "serial": "7A3B...",
        "valid_from": "2025-03-21",
        "valid_until": "2029-03-21"
      },
      "timestamp": {
        "time": "2026-03-21T10:54:52.000Z",
        "tsa": "DigiCert Timestamp Authority"
      }
    }
  ],
  "summary": {
    "total": 1,
    "valid": 1,
    "invalid": 0,
    "verdict": "all_valid"
  },
  "verified_at": "2026-03-21T15:15:55.123Z",
  "verified_by": "eContract - https://verify.econtract.online"
}
```

---

## 📦 Language Examples

### JavaScript / Node.js

```javascript
const form = new FormData();
form.append("file", fileInput.files[0]);

const res = await fetch("https://api.econtract.online/verify-pdf", {
  method: "POST",
  body: form,
});

const data = await res.json();

if (data.summary.verdict === "all_valid") {
  console.log("✅ All signatures valid");
} else {
  console.log("❌ Verification failed");
}
```

### Python

```python
import requests

with open("contract.pdf", "rb") as f:
    res = requests.post(
        "https://api.econtract.online/verify-pdf",
        files={"file": f}
    )

data = res.json()
print(f"Verdict: {data['summary']['verdict']}")
print(f"Tampered: {data['document']['tampered']}")

for sig in data["signatures"]:
    print(f"  {sig['signer']['name']} — {sig['verdict']}")
```

### PHP

```php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://api.econtract.online/verify-pdf");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, [
    "file" => new CURLFile("contract.pdf")
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = json_decode(curl_exec($ch));
echo "Verdict: " . $response->summary->verdict . "\n";
echo "Tampered: " . ($response->document->tampered ? "YES" : "No") . "\n";
```

### Go

```go
file, _ := os.Open("contract.pdf")
defer file.Close()

body := &bytes.Buffer{}
writer := multipart.NewWriter(body)
part, _ := writer.CreateFormFile("file", "contract.pdf")
io.Copy(part, file)
writer.Close()

resp, _ := http.Post(
    "https://api.econtract.online/verify-pdf",
    writer.FormDataContentType(),
    body,
)
defer resp.Body.Close()

var result map[string]interface{}
json.NewDecoder(resp.Body).Decode(&result)
fmt.Println(result["summary"])
```

---

## 🔍 What It Checks

| Check | Description |
|-------|-------------|
| **Integrity** | SHA-256 hash verification — has the document been modified after signing? |
| **Signature** | RSA cryptographic signature validation |
| **Certificate Chain** | Validates signer cert → intermediate CA → root CA |
| **Certificate Expiry** | Are all certificates in the chain still valid? |
| **Timestamp** | RFC 3161 TSA timestamp verification (when present) |

### Verdict Values

| Verdict | Meaning |
|---------|---------|
| `all_valid` | All signatures verified, document intact |
| `has_invalid` | One or more signatures failed verification |
| `no_signatures` | PDF has no digital signatures |

---

## 📋 Supported Formats

- ✅ **PAdES** — PDF Advanced Electronic Signatures (EU standard)
- ✅ **CMS / PKCS#7** — Embedded CMS signatures
- ✅ **RSA + SHA-256** — Standard cryptographic signatures
- ✅ **RFC 3161** — Trusted timestamps from any TSA
- ✅ **Multi-signature** — Documents with multiple signers
- ✅ **Any signing tool** — DocuSign, Adobe Sign, GlobalSign, eContract, or any PKI-based signer

---

## 🤖 AI Agent Integration

verify-pdf is built for AI agents that need to make trust decisions about contracts.

```python
# AI agent workflow: verify before processing
result = requests.post(API_URL, files={"file": pdf}).json()

if result["document"]["tampered"]:
    return "REJECT: Document has been tampered with"

if result["summary"]["verdict"] != "all_valid":
    return "REJECT: Invalid signatures detected"

# Extract signer info for downstream processing
signers = [s["signer"]["name"] for s in result["signatures"]]
return f"APPROVED: Signed by {', '.join(signers)}"
```

### From an MCP client (Claude, ChatGPT, Cursor, …)

The same check is the `verify_pdf` tool of the eContract MCP server, so an assistant can verify a PDF the user attaches without any code:

```text
https://api.econtract.online/mcp
```

Setup for each client: [contractlayer/contractlayer → mcp](https://github.com/contractlayer/contractlayer/tree/main/mcp). Connecting to the MCP server needs a free eContract account; `verify_pdf` itself needs no extra permission scope. The plain HTTP API above needs no account at all.

**Use cases for AI agents:**
- Contract review automation — verify before analyzing content
- CRM integrations — auto-validate incoming signed documents
- HR systems — verify offer letters and employment contracts
- Legal workflows — chain-of-custody signature validation

---

## ⚙️ API Reference

### `POST /verify-pdf`

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (PDF binary, max 50 MB)
- Authentication: None required
- Rate limit: 50 requests/day per IP

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `document.filename` | string | Original filename |
| `document.hash` | string | SHA-256 hash (`sha256:...`) |
| `document.size` | number | File size in bytes |
| `document.tampered` | boolean | `true` if document was modified after signing |
| `signatures[]` | array | List of signature objects |
| `signatures[].signer.name` | string | Signer common name |
| `signatures[].signer.email` | string | Signer email (if available) |
| `signatures[].signer.organization` | string | Signer organization |
| `signatures[].signer.country` | string | Signer country code |
| `signatures[].signed_at` | string | ISO 8601 signing timestamp |
| `signatures[].verdict` | string | `"valid"` or `"invalid"` |
| `signatures[].integrity` | boolean | Document integrity check |
| `signatures[].signature` | boolean | Cryptographic signature check |
| `signatures[].chain` | boolean | Certificate chain check |
| `signatures[].expired` | boolean | Certificate expiry check |
| `signatures[].certificate` | object | Certificate details |
| `signatures[].timestamp` | object | RFC 3161 timestamp (if present) |
| `summary.total` | number | Total signatures found |
| `summary.valid` | number | Valid signature count |
| `summary.invalid` | number | Invalid signature count |
| `summary.verdict` | string | `"all_valid"`, `"has_invalid"`, or `"no_signatures"` |

**Error responses:**

```json
// 400 — Invalid file
{ "statusCode": 400, "message": "No PDF file provided" }

// 413 — File too large
{ "statusCode": 413, "message": "File size exceeds 50MB limit" }

// 429 — Rate limited
{ "statusCode": 429, "message": "Rate limit exceeded. Try again tomorrow." }
```

---

## 🏗️ Self-Hosting

Coming soon. We're working on a Docker image for self-hosted deployment.

In the meantime, use the free hosted API at `api.econtract.online`.

---

## 🗺️ Roadmap

- [x] PAdES / CMS signature verification
- [x] Certificate chain validation
- [x] RFC 3161 timestamp verification
- [x] Free hosted API (live)
- [x] Web UI at [verify.econtract.online](https://verify.econtract.online)
- [ ] Trust Store v2 (Mozilla CA bundle + Adobe AATL)
- [ ] CRL / OCSP revocation checking
- [ ] Docker image for self-hosting
- [ ] npm / pip packages
- [ ] Webhook notifications
- [ ] Batch verification endpoint

---

## 🔗 Related Projects

| Project | Description |
|---------|-------------|
| [contractlayer](https://github.com/contractlayer/contractlayer) | The eContract MCP server and a config for every AI client |
| [contract-manager](https://github.com/contractlayer/contract-manager) | Send contracts for e-signature with the REST API (Node.js, Python) |

---

## 📄 License

[MIT](LICENSE) — free for commercial and personal use.

---

<p align="center">
  <b>Built by <a href="https://econtract.online">eContract</a></b><br>
  Tamper-proof digital signatures for the modern web.
</p>
