"""
FNOL Claims Processing Agent
==============================
Uses FREE Groq API to extract fields, detect missing data,
classify claims, and route them to the correct workflow.
"""

import os
import json
import re
from pathlib import Path
from groq import Groq

# ── Groq client (FREE) ────────────────────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

# ── Routing keywords ──────────────────────────────────────────────────────────
FRAUD_KEYWORDS = ["fraud", "inconsistent", "staged", "suspicious", "fabricated"]
FAST_TRACK_LIMIT = 25000


# ── Step 1: Read FNOL document ────────────────────────────────────────────────
def read_fnol(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ── Step 2: Extract fields via Groq ──────────────────────────────────────────
def extract_fields(raw_text: str) -> dict:
    prompt = f"""
You are an insurance claims extraction assistant.
Extract the following fields from the FNOL document below.
Return ONLY a valid JSON object — no explanation, no markdown, no code fences.

Fields to extract:
- policy_number
- policyholder_name
- policy_effective_date
- policy_expiry_date
- incident_date
- incident_time
- incident_location
- incident_description
- claimant_name
- third_party
- contact_details
- asset_type
- asset_id
- estimated_damage (number only, no currency symbol)
- claim_type
- attachments
- initial_estimate (number only, no currency symbol)

If a field is missing or blank, set its value to null.

FNOL Document:
\"\"\"
{raw_text}
\"\"\"
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if present
    raw = re.sub(r"^```(?:json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()
    return json.loads(raw)


# ── Step 3: Identify missing fields ───────────────────────────────────────────
MANDATORY_FIELDS = [
    "policy_number", "policyholder_name", "policy_effective_date",
    "incident_date", "incident_time", "incident_location",
    "incident_description", "claimant_name", "contact_details",
    "asset_type", "estimated_damage", "claim_type", "initial_estimate",
]

def find_missing(fields: dict) -> list:
    return [f for f in MANDATORY_FIELDS if not fields.get(f)]


# ── Step 4: Route the claim ───────────────────────────────────────────────────
def route_claim(fields: dict, missing: list) -> tuple:
    description = (fields.get("incident_description") or "").lower()
    claim_type  = (fields.get("claim_type") or "").lower()

    try:
        damage = float(fields.get("estimated_damage") or 0)
    except (ValueError, TypeError):
        damage = 0

    # Priority 1 – fraud / investigation flag
    if any(kw in description for kw in FRAUD_KEYWORDS):
        return (
            "Investigation Flag",
            f"Description contains suspicious keyword(s): "
            f"{[kw for kw in FRAUD_KEYWORDS if kw in description]}. "
            "Routed for investigation.",
        )

    # Priority 2 – injury specialist
    if claim_type == "injury":
        return (
            "Specialist Queue",
            "Claim type is 'Injury'. Requires specialist medical assessment team.",
        )

    # Priority 3 – missing mandatory fields
    if missing:
        return (
            "Manual Review",
            f"The following mandatory fields are missing or blank: {missing}. "
            "A human agent must complete the record before processing.",
        )

    # Priority 4 – fast track (damage < threshold)
    if damage < FAST_TRACK_LIMIT:
        return (
            "Fast-track",
            f"Estimated damage ({damage:,.0f}) is below the {FAST_TRACK_LIMIT:,} "
            "threshold and all mandatory fields are present. Eligible for fast-track.",
        )

    # Default – standard queue
    return (
        "Standard Queue",
        f"Estimated damage ({damage:,.0f}) exceeds {FAST_TRACK_LIMIT:,} "
        "threshold. Routed to standard processing queue.",
    )


# ── Step 5: Build output JSON ─────────────────────────────────────────────────
def build_output(fields: dict, missing: list, route: str, reasoning: str) -> dict:
    return {
        "extractedFields": fields,
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": reasoning,
    }


# ── Main orchestrator ─────────────────────────────────────────────────────────
def process_fnol(file_path: str, output_dir: str = "outputs") -> dict:
    print(f"\n{'='*55}")
    print(f"  Processing: {Path(file_path).name}")
    print(f"{'='*55}")

    raw_text = read_fnol(file_path)

    print("  [1/4] Extracting fields via Groq (free)...")
    fields = extract_fields(raw_text)

    print("  [2/4] Checking for missing fields...")
    missing = find_missing(fields)
    if missing:
        print(f"         Missing: {missing}")
    else:
        print("         All mandatory fields present.")

    print("  [3/4] Routing claim...")
    route, reasoning = route_claim(fields, missing)
    print(f"         Route -> {route}")

    print("  [4/4] Building output...")
    result = build_output(fields, missing, route, reasoning)

    # Save output JSON
    Path(output_dir).mkdir(exist_ok=True)
    stem = Path(file_path).stem
    out_path = Path(output_dir) / f"{stem}_result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"  Saved -> {out_path}")

    return result


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fnol_dir = Path("sample_fnols")
    fnol_files = sorted(fnol_dir.glob("*.txt")) + sorted(fnol_dir.glob("*.pdf"))

    if not fnol_files:
        print("No FNOL files found in sample_fnols/")
        exit(1)

    summary = []
    for fp in fnol_files:
        result = process_fnol(str(fp))
        summary.append({
            "file": fp.name,
            "route": result["recommendedRoute"],
            "missingFields": result["missingFields"],
        })

    print("\n" + "="*55)
    print("  PROCESSING SUMMARY")
    print("="*55)
    for s in summary:
        print(f"  {s['file']:<20} -> {s['route']}")
        if s["missingFields"]:
            print(f"    Missing: {s['missingFields']}")
    print("="*55)
    print(f"\nAll results saved in: outputs/")