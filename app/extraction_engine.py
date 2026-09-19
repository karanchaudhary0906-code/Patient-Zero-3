import re
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from app.models import (
    PatientProfile, MedicalDocument, TimelineEvent,
    LabMetricSeries, LabDataPoint, MedicationRecord,
    DiscrepancyItem, RelationshipLink, SourceProvenance
)

class MedicalExtractionEngine:
    def __init__(self):
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")

    def process_uploaded_document(self, text: str, filename: str, patient: PatientProfile) -> Tuple[MedicalDocument, List[TimelineEvent], List[DiscrepancyItem]]:
        doc_id = f"doc-up-{uuid.uuid4().hex[:6]}"
        today_str = datetime.now().strftime("%Y-%m-%d")

        # Date extraction heuristic
        date_matches = re.findall(r'(?:Date|Collected|Dated|Encounter):\s*([A-Za-z]+ \d{1,2}, \d{4}|\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
        doc_date = date_matches[0] if date_matches else today_str
        try:
            parsed_date = datetime.strptime(doc_date, "%B %d, %Y").strftime("%Y-%m-%d")
        except Exception:
            parsed_date = doc_date if re.match(r'^\d{4}-\d{2}-\d{2}$', doc_date) else today_str

        # Document type heuristic
        doc_type = "Clinical Note"
        if any(w in text.lower() for w in ["lab report", "specimen", "pathology", "hemoglobin", "test results", "cbc"]):
            doc_type = "Lab Report"
        elif any(w in text.lower() for w in ["discharge summary", "operative report", "admission"]):
            doc_type = "Discharge Summary"
        elif any(w in text.lower() for w in ["prescription", "rx:", "dispense"]):
            doc_type = "Prescription"
        elif any(w in text.lower() for w in ["ct scan", "mri", "x-ray", "ultrasound", "nodule"]):
            doc_type = "Imaging Scan"

        doc = MedicalDocument(
            id=doc_id,
            title=f"{doc_type} - {filename}",
            doc_type=doc_type,
            date=parsed_date,
            author="Extracted Clinical Provider",
            facility="Clinical Ingestion Portal",
            file_name=filename,
            raw_text=text
        )

        extracted_events = []
        new_discrepancies = []

        # Extract lab values if present
        lab_patterns = [
            (r'Hemoglobin(?:\s*\(Hb\))?:?\s*([\d\.]+)\s*(?:g/dL)?', "Hemoglobin", "g/dL"),
            (r'Hemoglobin A1c:?\s*([\d\.]+)\s*%?', "Hemoglobin A1c", "%"),
            (r'Glucose:?\s*([\d\.]+)\s*mg/dL', "Fasting Blood Glucose", "mg/dL"),
            (r'Creatinine:?\s*([\d\.]+)\s*mg/dL', "Serum Creatinine", "mg/dL"),
            (r'WBC:?\s*([\d\.,]+)\s*(?:k/uL|/uL)?', "White Blood Cell Count", "/uL"),
            (r'CRP:?\s*([\d\.]+)\s*mg/L', "C-Reactive Protein", "mg/L"),
            (r'BP:?\s*(\d{2,3}/\d{2,3})\s*mmHg', "Blood Pressure", "mmHg"),
        ]

        found_labs = []
        for pat, test_name, unit in lab_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                val_str = m.group(1)
                found_labs.append(f"{test_name}: {val_str} {unit}")

        if found_labs:
            event = TimelineEvent(
                id=f"ev-up-{uuid.uuid4().hex[:6]}",
                date=parsed_date,
                category="Laboratory",
                title=f"Extracted Diagnostic Panel ({len(found_labs)} tests)",
                summary=", ".join(found_labs),
                details={"tests": found_labs},
                clinician="Automated Extraction Engine",
                facility="Diagnostic Services",
                status="Warning" if any("A1c" in x or "CRP" in x or "Low" in text for x in found_labs) else "Normal",
                tags=["Extracted Labs", "Uploaded Record"],
                provenance=SourceProvenance(
                    document_id=doc_id,
                    document_name=filename,
                    date=parsed_date,
                    page_number=1,
                    verbatim_quote=found_labs[0] if found_labs else text[:100],
                    confidence_score=0.94,
                    certainty_level="High"
                )
            )
            extracted_events.append(event)

        # Update patient.labs for numeric lab points
        for pat, test_name, unit, norm_min, norm_max, cat in [
            (r'Hemoglobin(?:\s*\(Hb\))?:?\s*([\d\.]+)', "Hemoglobin", "g/dL", 12.0, 17.5, "Hematology"),
            (r'Hemoglobin A1c:?\s*([\d\.]+)', "Hemoglobin A1c", "%", 4.0, 5.6, "Glycemic"),
            (r'Glucose:?\s*([\d\.]+)', "Fasting Blood Glucose", "mg/dL", 70.0, 99.0, "Glycemic"),
            (r'Creatinine:?\s*([\d\.]+)', "Serum Creatinine", "mg/dL", 0.6, 1.2, "Renal"),
            (r'WBC:?\s*([\d\.,]+)', "White Blood Cell Count", "/uL", 4000.0, 11000.0, "Hematology"),
            (r'CRP:?\s*([\d\.]+)', "C-Reactive Protein", "mg/L", 0.0, 3.0, "Inflammatory"),
            (r'Ferritin:?\s*([\d\.]+)', "Serum Ferritin", "ng/mL", 15.0, 200.0, "Hematology"),
        ]:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                try:
                    num_val = float(m.group(1).replace(",", ""))
                    pt_flag = "Normal"
                    if num_val < norm_min:
                        pt_flag = "Low"
                    elif num_val > norm_max:
                        pt_flag = "High"
                    
                    lab_pt = LabDataPoint(
                        date=parsed_date,
                        value=num_val,
                        unit=unit,
                        flag=pt_flag,
                        reference_range=f"{norm_min}-{norm_max} {unit}",
                        doc_id=doc_id,
                        provenance=SourceProvenance(
                            document_id=doc_id,
                            document_name=filename,
                            date=parsed_date,
                            page_number=1,
                            verbatim_quote=m.group(0),
                            confidence_score=0.96,
                            certainty_level="High"
                        )
                    )
                    series = next((s for s in patient.labs if s.test_name.lower() == test_name.lower()), None)
                    if not series:
                        series = LabMetricSeries(
                            test_name=test_name,
                            category=cat,
                            unit=unit,
                            normal_min=norm_min,
                            normal_max=norm_max,
                            points=[lab_pt],
                            trend_interpretation=f"Baseline documented: {num_val} {unit} ({pt_flag})"
                        )
                        patient.labs.append(series)
                    else:
                        series.points.append(lab_pt)
                        series.points.sort(key=lambda x: x.date)
                        delta = series.points[-1].value - series.points[0].value
                        trend_dir = "increased" if delta > 0 else "decreased"
                        series.trend_interpretation = f"{test_name} {trend_dir} from {series.points[0].value} to {series.points[-1].value} {unit}"
                except ValueError:
                    pass

        # Extract Prescriptions / Medications
        med_matches = re.findall(r'(?:Initiate|Prescribed|Rx|Start|Take)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)\s+(\d+\s*(?:mg|g|mcg|ml))\s+([A-Za-z0-9\s]+?)(?:\.|\n|$)', text, re.IGNORECASE)
        for drug, dose, freq in med_matches:
            clean_drug = drug.strip()
            clean_dose = dose.strip()
            clean_freq = freq.strip()
            med_ev = TimelineEvent(
                id=f"ev-up-{uuid.uuid4().hex[:6]}",
                date=parsed_date,
                category="Prescription",
                title=f"Medication Prescription: {clean_drug} {clean_dose}",
                summary=f"{clean_drug} {clean_dose} {clean_freq}",
                details={"drug": clean_drug, "dose": clean_dose, "frequency": clean_freq},
                clinician="Clinical Provider",
                facility="Care Facility",
                status="Normal",
                tags=["Prescription", "Medication Order"],
                provenance=SourceProvenance(
                    document_id=doc_id,
                    document_name=filename,
                    date=parsed_date,
                    page_number=1,
                    verbatim_quote=f"{clean_drug} {clean_dose} {clean_freq}",
                    confidence_score=0.89,
                    certainty_level="High"
                )
            )
            extracted_events.append(med_ev)

            # Update patient.medications list if not duplicate
            if not any(m.name.lower() == clean_drug.lower() and m.dosage.lower() == clean_dose.lower() for m in patient.medications):
                med_rec = MedicationRecord(
                    id=f"med-up-{uuid.uuid4().hex[:6]}",
                    name=clean_drug,
                    dosage=clean_dose,
                    frequency=clean_freq,
                    route="Oral",
                    start_date=parsed_date,
                    status="Active",
                    indication="Documented in uploaded medical record",
                    provenance=SourceProvenance(
                        document_id=doc_id,
                        document_name=filename,
                        date=parsed_date,
                        page_number=1,
                        verbatim_quote=f"{clean_drug} {clean_dose} {clean_freq}",
                        confidence_score=0.92,
                        certainty_level="High"
                    )
                )
                patient.medications.append(med_rec)

            # Check allergy contraindication against patient allergies
            for allergy in patient.allergies:
                allergy_core = allergy.lower().split('(')[0].strip()
                if allergy_core in clean_drug.lower() or (allergy_core == 'penicillin' and any(x in clean_drug.lower() for x in ['amoxicillin', 'ampicillin', 'augmentin', 'penicillin'])):
                    disc = DiscrepancyItem(
                        id=f"disc-up-{uuid.uuid4().hex[:6]}",
                        type="Allergy Warning",
                        severity="Critical",
                        title=f"Prescription Violates Allergy Profile: {clean_drug}",
                        description=f"Uploaded document contains order for {clean_drug} {clean_dose}, which directly violates known documented allergy: '{allergy}'.",
                        involved_documents=[filename],
                        evidence_quotes=[f"{clean_drug} {clean_dose} {clean_freq}"],
                        clinical_recommendation=f"Hard-stop warning: Withhold {clean_drug} pending clinician allergy confirmation."
                    )
                    new_discrepancies.append(disc)

        # Fallback clinical encounter event if no specific labs or meds parsed
        if not extracted_events:
            event = TimelineEvent(
                id=f"ev-up-{uuid.uuid4().hex[:6]}",
                date=parsed_date,
                category=doc_type if doc_type in ["Consultation", "Imaging", "Hospitalization", "Procedure"] else "Consultation",
                title=f"Medical Document Ingestion: {doc_type}",
                summary=text[:160] + ("..." if len(text) > 160 else ""),
                details={"char_count": len(text)},
                clinician="Ingestion Engine",
                facility="Clinical Records",
                status="Normal",
                tags=["Clinical Document", "Ingested"],
                provenance=SourceProvenance(
                    document_id=doc_id,
                    document_name=filename,
                    date=parsed_date,
                    page_number=1,
                    verbatim_quote=text[:120],
                    confidence_score=0.85,
                    certainty_level="Moderate",
                    uncertainty_rationale="Automated narrative parsing without discrete numeric markers"
                )
            )
            extracted_events.append(event)

        return doc, extracted_events, new_discrepancies

    def generate_what_changed(self, patient: PatientProfile) -> Dict[str, Any]:
        """
        Killer Hackathon Feature: Synthesizes 'What Changed?' across:
        1. Blood Tests (trend changes with initial -> latest deltas)
        2. Medications (first seen -> last documented mention -> transitions)
        3. Missing Information & Inconsistencies
        4. Repeated Tests Frequency
        """
        test_changes = []
        for lab in patient.labs:
            if len(lab.points) >= 2:
                initial = lab.points[0]
                latest = lab.points[-1]
                delta = round(latest.value - initial.value, 2)
                direction = "increased" if delta > 0 else "decreased"
                test_changes.append({
                    "test_name": lab.test_name,
                    "initial": f"{initial.value} {lab.unit} ({initial.date})",
                    "latest": f"{latest.value} {lab.unit} ({latest.date})",
                    "summary": f"{lab.test_name} {direction} from {initial.value} -> {latest.value} {lab.unit}",
                    "delta": f"{'+' if delta > 0 else ''}{delta} {lab.unit}",
                    "interpretation": lab.trend_interpretation,
                    "times_tested": len(lab.points),
                    "provenance": latest.provenance
                })
            elif len(lab.points) == 1:
                pt = lab.points[0]
                test_changes.append({
                    "test_name": lab.test_name,
                    "initial": f"{pt.value} {lab.unit}",
                    "latest": f"{pt.value} {lab.unit} ({pt.date})",
                    "summary": f"{lab.test_name} measured once at {pt.value} {lab.unit}",
                    "delta": "Baseline",
                    "interpretation": lab.trend_interpretation,
                    "times_tested": 1,
                    "provenance": pt.provenance
                })

        med_changes = []
        for m in patient.medications:
            end_info = f"Last documented mention: {m.end_date}" if m.end_date else "Currently active / ongoing"
            summary_txt = f"{m.name} ({m.dosage}): First documented on {m.start_date}. {end_info}."
            if m.change_reason:
                summary_txt += f" Rationale: {m.change_reason}"
            med_changes.append({
                "name": m.name,
                "dosage": m.dosage,
                "status": m.status,
                "first_seen": m.start_date,
                "last_seen": m.end_date or "Present",
                "summary": summary_txt,
                "provenance": m.provenance
            })

        missing_info = []
        for d in patient.discrepancies:
            missing_info.append({
                "id": d.id,
                "title": d.title,
                "severity": d.severity,
                "description": d.description,
                "evidence": d.evidence_quotes,
                "recommendation": d.clinical_recommendation
            })

        repeated_tests = []
        for lab in patient.labs:
            repeated_tests.append({
                "test_name": lab.test_name,
                "count": len(lab.points),
                "frequency_summary": f"{lab.test_name} performed {len(lab.points)} times across {patient.timeline[0].date} to {patient.timeline[-1].date}"
            })

        return {
            "patient_name": patient.name,
            "date_range": f"{patient.timeline[0].date} to {patient.timeline[-1].date}" if patient.timeline else "",
            "blood_tests": test_changes,
            "medications": med_changes,
            "missing_information": missing_info,
            "repeated_tests": repeated_tests
        }

    def answer_longitudinal_query(self, patient: PatientProfile, query: str) -> Dict[str, Any]:
        q_lower = query.lower()
        answer = ""
        citations = []
        related_event_ids = []

        if any(w in q_lower for w in ["what changed", "changes", "difference", "evolution"]):
            changes = self.generate_what_changed(patient)
            lines = [f"**Longitudinal Changes Detected for {patient.name}:**\n"]
            lines.append("### 🩸 Blood Tests & Biomarkers")
            for t in changes["blood_tests"]:
                lines.append(f"• **{t['summary']}** ({t['delta']}) — *{t['interpretation']}*")
                citations.append(t["provenance"])
            lines.append("\n### 💊 Medication History")
            for m in changes["medications"]:
                lines.append(f"• {m['summary']}")
                citations.append(m["provenance"])
            if changes["missing_information"]:
                lines.append("\n### ⚠️ Missing Information & Alerts")
                for mi in changes["missing_information"]:
                    lines.append(f"• **{mi['title']}** ({mi['severity']}): {mi['description']}")
            lines.append("\n### 🔁 Repeated Testing")
            for r in changes["repeated_tests"]:
                lines.append(f"• {r['frequency_summary']}")
            answer = "\n".join(lines)

        elif any(w in q_lower for w in ["discrepancy", "conflict", "allergy", "error", "duplicate", "missing", "gap"]):
            if patient.discrepancies:
                disc_summaries = []
                for d in patient.discrepancies:
                    disc_summaries.append(f"- **{d.title}** ({d.severity}): {d.description}\n  *Evidence Quote:* \"{d.evidence_quotes[0] if d.evidence_quotes else 'N/A'}\"\n  *Recommendation:* {d.clinical_recommendation}")
                    for ev in patient.timeline:
                        if any(doc in ev.provenance.document_name for doc in d.involved_documents):
                            citations.append(ev.provenance)
                            related_event_ids.append(ev.id)
                answer = f"**Identified Clinical Discrepancies & Missing Context for {patient.name}:**\n\n" + "\n\n".join(disc_summaries)
            else:
                answer = f"No critical discrepancies currently flagged for {patient.name}."

        elif any(w in q_lower for w in ["medication", "drug", "dose", "iron", "ferrous", "metformin", "lisinopril", "losartan", "cephalexin", "ciprofloxacin", "antibiotic", "cough", "b12"]):
            med_details = []
            for m in patient.medications:
                status_txt = f"[Active since {m.start_date}]" if m.status == 'Active' else f"[Last documented: {m.end_date} - {m.change_reason or 'Completed'}]"
                med_details.append(f"- **{m.name} {m.dosage}** ({m.frequency}): {status_txt}\n  *Indication:* {m.indication}\n  *Source Quote:* \"{m.provenance.verbatim_quote}\"")
                citations.append(m.provenance)
            answer = f"**Medication History for {patient.name}:**\n\n" + "\n\n".join(med_details)

        elif any(w in q_lower for w in ["lab", "test", "hemoglobin", "hba1c", "a1c", "glucose", "creatinine", "wbc", "crp", "trend", "blood pressure", "bp"]):
            lab_details = []
            for l in patient.labs:
                pts_str = " -> ".join([f"{p.date}: {p.value} {p.unit} ({p.flag})" for p in l.points])
                lab_details.append(f"- **{l.test_name}** ({l.category}): {pts_str}\n  *Clinical Interpretation:* {l.trend_interpretation}")
                for p in l.points:
                    citations.append(p.provenance)
            answer = f"**Longitudinal Diagnostic Lab Trends for {patient.name}:**\n\n" + "\n\n".join(lab_details)

        else:
            matching_events = []
            for ev in patient.timeline:
                if any(term in ev.title.lower() or term in ev.summary.lower() or term in ' '.join(ev.tags).lower() for term in q_lower.split()):
                    matching_events.append(ev)
                    citations.append(ev.provenance)
                    related_event_ids.append(ev.id)

            if matching_events:
                ev_str = []
                for ev in matching_events:
                    ev_str.append(f"- **{ev.date}** [{ev.category}] **{ev.title}**: {ev.summary} *(Source: {ev.provenance.document_name}, Page {ev.provenance.page_number})*")
                answer = f"**Relevant Timeline Events for '{query}':**\n\n" + "\n".join(ev_str)
            else:
                answer = f"**Patient Journey Summary for {patient.name}**:\n- Total Longitudinal Records: {len(patient.documents)} documents across {patient.timeline[0].date} to {patient.timeline[-1].date}.\n- Diagnoses: {', '.join(patient.chronic_conditions)}.\n- Allergies: {', '.join(patient.allergies)}.\n- Flagged Discrepancies: {len(patient.discrepancies)} safety alert(s) detected.\n- Monitored Lab Series: {len(patient.labs)} physiological biomarkers tracked."
                if patient.timeline:
                    citations.append(patient.timeline[0].provenance)
                    related_event_ids.append(patient.timeline[0].id)

        unique_citations = []
        seen = set()
        for c in citations:
            key = (c.document_id, c.page_number, c.verbatim_quote)
            if key not in seen:
                seen.add(key)
                unique_citations.append(c)

        return {
            "answer": answer,
            "citations": unique_citations[:4],
            "related_events": list(set(related_event_ids))
        }

engine = MedicalExtractionEngine()
