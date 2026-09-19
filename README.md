# 🩺 Patient Zero: The Missing Context

> **"Upload scattered medical documents → automatically organize them into one understandable patient timeline, while always showing where every piece of information came from."**

---

## 🌟 Overview

**Patient Zero** is an informational medical record reconstitution and longitudinal context engine. Healthcare records today are deeply fragmented across clinics, laboratories, hospitals, and pharmacies. When a patient sees a new physician, crucial context is frequently dropped: medication adjustments, repeated tests, and incidental findings go unnoticed.

Patient Zero solves this by ingesting scattered PDFs, lab reports, doctor notes, and prescriptions, extracting structured clinical entities, and mapping them into an interactive chronological timeline with verifiable source provenance.

> ⚠️ **Important Safety Disclaimer**: Patient Zero is an informational record-organization tool, not an autonomous diagnostic system. Every insight is 100% sourced and backed by original documentation excerpts.

---

## 🚀 Key Features

1. **Multi-Format Document Upload**:
   - Ingest PDFs, scanned images (JPEG, PNG), and raw clinical narrative notes.
   - Built-in visual document viewer with native image previews.

2. **Automated Clinical Entity Extraction**:
   - Deterministic regex parsing + optional **Gemini 2.5 Flash Vision** multimodal OCR.
   - Identifies encounter dates, diagnostic tests, numerical values, units, reference ranges, and medication orders.

3. **Color-Coded Longitudinal Timeline**:
   - 🔵 **Laboratory Test**
   - 🟢 **Prescription / Medication Order**
   - 🟣 **Doctor Consultation**
   - 🟠 **Imaging / Scan**
   - 🔴 **Hospitalization**

4. **Biomarker Trends Tracking**:
   - Interactive progression curves (Hemoglobin, Fasting Blood Glucose, Serum Creatinine, etc.) with standard reference intervals.

5. **Verifiable Source Provenance**:
   - Every single datum links directly to its source document, page number, confidence percentage, and verbatim quote with visual `<mark>` highlighting.

6. **✨ Killer Feature: "What Changed?" Engine**:
   - Automatically compares serial laboratory tests (e.g. Hemoglobin 11.8 → 14.1 g/dL).
   - Tracks medication lifecycles (*First documented* vs. *Last documented mention*).
   - Flags dropped follow-ups, medication conflicts, and drug allergy clashes.

7. **🎬 3-Minute Hackathon Demo Simulator**:
   - Guided 1-click pitch workflow that uploads scattered reports, builds the timeline, inspects provenance, and delivers the closing hackathon thesis.

---

## 🛠️ Quickstart Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.12, 3.13, 3.14)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/patient-zero.git
cd patient-zero
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python run.py
```
Open your browser at **http://127.0.0.1:8000** (or **http://localhost:8000**).

---

## 📱 How to View on Mobile & Share with Others

### Option A: View on Mobile (Same Wi-Fi)
Run the server on `0.0.0.0`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Find your laptop IP (`ipconfig` on Windows or `ifconfig` on Mac) and open `http://<YOUR_LAPTOP_IP>:8000` on your phone!

### Option B: Free Cloud Hosting (Render / Railway / Koyeb)
1. Push this repository to GitHub.
2. Go to [Render.com](https://render.com/) → **New Web Service** → Connect your GitHub repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **Deploy** to receive a public HTTPS URL (e.g., `https://patient-zero.onrender.com`) shareable with judges and friends!

---

## 🧪 Testing

Run the automated test suite:
```bash
python -m unittest tests/test_api.py
```

---

## 📜 Closing Statement
> *"Patient Zero doesn't diagnose the patient. It gives patients and clinicians something healthcare records often fail to provide: **context**."*
