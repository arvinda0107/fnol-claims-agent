# 🏦 FNOL Claims Processing Agent

An autonomous AI agent that processes **First Notice of Loss (FNOL)** insurance documents — extracting key fields, detecting missing data, classifying claims, and routing them to the correct workflow.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Architecture](#architecture)
5. [Routing Rules](#routing-rules)
6. [Prerequisites](#prerequisites)
7. [Installation](#installation)
8. [Configuration](#configuration)
9. [Running the Agent](#running-the-agent)
10. [Output Format](#output-format)
11. [Sample FNOL Documents](#sample-fnol-documents)
12. [Technologies Used](#technologies-used)

---

## Overview

Insurance companies receive hundreds of FNOL documents daily. Processing them manually is slow, error-prone, and inconsistent. This agent automates the entire pipeline — from reading raw documents to routing them to the correct team — in seconds.

| Without Agent | With Agent |
|---------------|------------|
| 10–15 mins per FNOL | Seconds per FNOL |
| Human errors in extraction | Consistent AI extraction |
| Inconsistent routing decisions | Rule-based, auditable routing |
| No explanation for decisions | Clear reasoning in every output |

---

## Features

- 📄 **Auto-reads** FNOL documents from a folder (`.txt` and `.pdf`)
- 🤖 **AI-powered extraction** of 17 structured fields using LLaMA 3.1 8B
- ✅ **Validates** all mandatory fields and flags missing ones
- 🔀 **Routes** each claim to the correct workflow automatically
- 💬 **Explains** every routing decision in plain English
- 💾 **Saves** structured JSON output for each processed FNOL
- ⚡ **Free to run** — uses Groq free tier, no credit card needed

---

## Project Structure

```
fnol-agent/
├── agent.py              # Main agent script
├── requirements.txt      # Python dependencies
├── sample_fnols/         # Input FNOL documents (.txt or .pdf)
│   ├── fnol_001.txt      # Motor claim – fast track
│   ├── fnol_002.txt      # Injury claim – specialist queue
│   ├── fnol_003.txt      # Fraud flag claim
│   ├── fnol_004.txt      # Missing fields – manual review
│   └── fnol_005.txt      # Small motor – fast track
└── outputs/              # Auto-created; JSON results saved here
    ├── fnol_001_result.json
    ├── fnol_002_result.json
    ├── fnol_003_result.json
    ├── fnol_004_result.json
    └── fnol_005_result.json
```

---

## Architecture

```
📄 FNOL Document (.txt / .pdf)
          │
          ▼
  ┌───────────────┐
  │  Step 1       │  Read raw document from sample_fnols/
  │  Read         │
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │  Step 2       │  Send to Groq API → LLaMA 3.1 8B
  │  Extract      │  Returns 17 structured fields as JSON
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │  Step 3       │  Check 13 mandatory fields
  │  Validate     │  Flag any missing or blank fields
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │  Step 4       │  Apply priority-based routing rules
  │  Route        │  Generate plain English reasoning
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │  Step 5       │  Save result to outputs/ as JSON
  │  Save         │
  └───────────────┘
```

---

## Routing Rules

Claims are routed based on the following priority order:

| Priority | Condition | Route |
|----------|-----------|-------|
| 1 | Description contains "fraud", "staged", "inconsistent", "suspicious" | 🚩 Investigation Flag |
| 2 | Claim type = Injury | 🏥 Specialist Queue |
| 3 | Any mandatory field is missing or blank | 📋 Manual Review |
| 4 | Estimated damage < ₹25,000 | ⚡ Fast-track |
| 5 | Everything else | 📦 Standard Queue |

---

## Prerequisites

Before running this project, make sure you have:

- **Python 3.9 or above** installed
- **pip** (Python package manager)
- A free **Groq API key** from [console.groq.com](https://console.groq.com/keys)
- **Git** installed (to clone the repo)

---

## Installation

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/fnol-agent.git
cd fnol-agent
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

### Step 1 — Get your free Groq API key
1. Go to 👉 [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up with your email (free, no credit card needed)
3. Click **Create API Key**
4. Copy the key

### Step 2 — Set your API key

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_key_here"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your_key_here
```

**Linux / Mac:**
```bash
export GROQ_API_KEY="your_key_here"
```

> ⚠️ The key must be set in the same terminal session before running the agent.

---

## Running the Agent

```bash
python agent.py
```

Expected output:
```
=======================================================
  Processing: fnol_001.txt
=======================================================
  [1/4] Extracting fields via Groq (free)...
  [2/4] Checking for missing fields...
         All mandatory fields present.
  [3/4] Routing claim...
         Route -> Fast-track
  [4/4] Building output...
  Saved -> outputs\fnol_001_result.json

=======================================================
  PROCESSING SUMMARY
=======================================================
  fnol_001.txt         -> Fast-track
  fnol_002.txt         -> Specialist Queue
  fnol_003.txt         -> Investigation Flag
  fnol_004.txt         -> Manual Review
  fnol_005.txt         -> Fast-track
=======================================================
```

---

## Output Format

Each FNOL is saved as a structured JSON file in the `outputs/` folder:

```json
{
  "extractedFields": {
    "policy_number": "POL-2024-78432",
    "policyholder_name": "Rajesh Kumar",
    "policy_effective_date": "2024-01-01",
    "policy_expiry_date": "2025-01-01",
    "incident_date": "2024-11-15",
    "incident_time": "14:30",
    "incident_location": "MG Road, Bangalore",
    "incident_description": "Vehicle hit a divider",
    "claimant_name": "Rajesh Kumar",
    "third_party": null,
    "contact_details": "9876543210",
    "asset_type": "Car",
    "asset_id": "KA-01-AB-1234",
    "estimated_damage": 18000,
    "claim_type": "vehicle",
    "attachments": "photos, repair estimate",
    "initial_estimate": 18000
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Estimated damage (18,000) is below the 25,000 threshold and all mandatory fields are present. Eligible for fast-track."
}
```

---

## Sample FNOL Documents

| File | Claim Type | Route | Notes |
|------|------------|-------|-------|
| fnol_001.txt | Motor | ⚡ Fast-track | All fields present, damage below ₹25,000 |
| fnol_002.txt | Injury | 🏥 Specialist Queue | Injury claim detected |
| fnol_003.txt | Motor | 🚩 Investigation Flag | Suspicious keywords in description |
| fnol_004.txt | Motor | 📋 Manual Review | 3 mandatory fields missing |
| fnol_005.txt | Motor | ⚡ Fast-track | All fields present, damage below ₹25,000 |

---

## Technologies Used

| Component | Technology |
|-----------|------------|
| Language | Python 3.13 |
| AI Model | LLaMA 3.1 8B |
| API Provider | Groq (free tier) |
| Output Format | JSON |
| Version Control | Git + GitHub |

---

## 👤 Author

Built for the **Insurance Claims Processing Agent Assessment**.
