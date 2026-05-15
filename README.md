# fnol-claims-agent
AI agent that automates FNOL insurance claims processing — extracts fields, detects missing data, and routes claims using Groq + LLaMA 3.1 (free tier)
# 🏦 FNOL Claims Processing Agent

An autonomous AI agent that processes **First Notice of Loss (FNOL)** insurance documents — extracting key fields, detecting missing data, classifying claims, and routing them to the correct workflow.

---

## 📁 Project Structure
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

---

## ⚙️ How It Works

1. **Read** each FNOL document from `sample_fnols/`
2. **Extract** key fields using Groq (LLaMA 3.1 8B)
3. **Detect** missing or blank mandatory fields
4. **Route** the claim using these rules:

| Condition | Route |
|---|---|
| Description has "fraud / staged / inconsistent" | 🚩 Investigation Flag |
| Claim type = Injury | 🏥 Specialist Queue |
| Any mandatory field is missing | 📋 Manual Review |
| Estimated damage < $25,000 | ⚡ Fast-track |
| Everything else | 📦 Standard Queue |

5. **Save** a structured JSON result for each FNOL

---

## 🚀 Steps to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/fnol-agent.git
cd fnol-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up and create an API key (free, no credit card needed)

### 4. Set your Groq API key

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_key_here"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your_key_here
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your_key_here"
```

### 5. Run the agent
```bash
python agent.py
```

### 6. View results
Results are saved in the `outputs/` folder as JSON files.

---

## 📤 Output Format

```json
{
  "extractedFields": {
    "policy_number": "POL-2024-78432",
    "policyholder_name": "John Smith",
    "incident_date": "2024-11-15",
    "estimated_damage": 18000,
    "claim_type": "vehicle"
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Estimated damage (18,000) is below the 25,000 threshold and all mandatory fields are present. Eligible for fast-track."
}
```

---

## 🛠️ Tech Stack

- **Python 3.13**
- **Groq API** (free tier) — for fast AI inference
- **LLaMA 3.1 8B** — for intelligent field extraction
- No database, no framework — just one clean script

---

## 📊 Test Results

| File | Route | Notes |
|------|-------|-------|
| fnol_001.txt | ⚡ Fast-track | All fields present, low damage |
| fnol_002.txt | 🏥 Specialist Queue | Injury claim detected |
| fnol_003.txt | 🚩 Investigation Flag | Suspicious keywords found |
| fnol_004.txt | 📋 Manual Review | 3 mandatory fields missing |
| fnol_005.txt | ⚡ Fast-track | All fields present, low damage |

---

## 📝 Adding Your Own FNOL Files

Drop any `.txt` FNOL document into `sample_fnols/` and run `agent.py` again.
The agent will automatically pick up and process all files.

---

## 👤 Author

Built for the Insurance Claims Processing Agent Assessment.
