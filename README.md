 FNOL Claims Processing Agent

An autonomous AI agent that processes **First Notice of Loss (FNOL)** insurance documents — extracting key fields, detecting missing data, classifying claims, and routing them to the correct workflow.

---

## 🎯 Problem Statement

Insurance companies receive hundreds of FNOL documents daily. Processing them manually is:
- ⏰ Slow — 10 to 15 minutes per document
- ❌ Error-prone — humans miss fields
- 🔀 Inconsistent — different agents make different decisions

This agent automates the entire pipeline in seconds.

---

## 🧠 How It Works
📄 FNOL Document (.txt)
↓
Step 1 — Read Document
↓
Step 2 — Extract Fields using AI (Groq + LLaMA 3.1 8B)
↓
Step 3 — Detect Missing Mandatory Fields
↓
Step 4 — Route Claim by Priority Rules
↓
Step 5 — Save Output as JSON

---

## 🗂️ Project Structure
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

## 🔀 Routing Rules

| Priority | Condition | Route |
|----------|-----------|-------|
| 1 | Description contains "fraud / staged / inconsistent" | 🚩 Investigation Flag |
| 2 | Claim type = Injury | 🏥 Specialist Queue |
| 3 | Any mandatory field is missing | 📋 Manual Review |
| 4 | Estimated damage < ₹25,000 | ⚡ Fast-track |
| 5 | Everything else | 📦 Standard Queue |

---

## 📤 Output Format

Each processed FNOL is saved as a JSON file in the `outputs/` folder:

```json
{
  "extractedFields": {
    "policy_number": "POL-2024-78432",
    "policyholder_name": "Rajesh Kumar",
    "incident_date": "2024-11-15",
    "incident_time": "14:30",
    "incident_location": "MG Road, Bangalore",
    "estimated_damage": 18000,
    "claim_type": "vehicle"
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Estimated damage (₹18,000) is below the ₹25,000 threshold and all mandatory fields are present. Eligible for fast-track."
}
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13 |
| AI Model | LLaMA 3.1 8B |
| API | Groq (free tier) |
| Output | JSON files |

---

## 🚀 Steps to Run

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/fnol-agent.git
cd fnol-agent
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Get a free Groq API key
1. Go to 👉 [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up with your email (free, no credit card needed)
3. Click **Create API Key**
4. Copy the key

### Step 4 — Set your Groq API key

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

### Step 5 — Run the agent
```bash
python agent.py
```

### Step 6 — View results
Results are saved in the `outputs/` folder as JSON files.
outputs/
├── fnol_001_result.json
├── fnol_002_result.json
├── fnol_003_result.json
├── fnol_004_result.json
└── fnol_005_result.json

---

## 📊 Test Results

| File | Route | Notes |
|------|-------|-------|
| fnol_001.txt | ⚡ Fast-track | All fields present, damage below ₹25,000 |
| fnol_002.txt | 🏥 Specialist Queue | Injury claim detected |
| fnol_003.txt | 🚩 Investigation Flag | Suspicious keywords found in description |
| fnol_004.txt | 📋 Manual Review | 3 mandatory fields missing |
| fnol_005.txt | ⚡ Fast-track | All fields present, damage below ₹25,000 |

---

## 📈 Impact

| Without Agent | With Agent |
|---------------|------------|
| 10–15 mins per FNOL | Seconds per FNOL |
| Human errors in extraction | Consistent AI extraction |
| Inconsistent routing decisions | Rule-based, auditable routing |
| No explanation for decisions | Clear reasoning in every output |

---

## ➕ Adding Your Own FNOL Files

1. Drop any `.txt` FNOL document into the `sample_fnols/` folder
2. Run `python agent.py` again
3. The agent automatically picks up and processes all files

---

## 👤 Author

Built for the **Insurance Claims Processing Agent Assessment**.
