from app.models import (
    PatientProfile, MedicalDocument, TimelineEvent,
    LabMetricSeries, LabDataPoint, MedicationRecord,
    DiscrepancyItem, RelationshipLink, SourceProvenance
)

def get_p0() -> PatientProfile:
    docs = [
        MedicalDocument(
            id="doc-p0-01",
            title="Comprehensive Complete Blood Count (CBC)",
            doc_type="Lab Report",
            date="2026-01-12",
            author="Apollo Diagnostics Clinical Laboratory",
            facility="Apollo Hospital Central Lab",
            file_name="blood_report_jan.pdf",
            raw_text="""APOLLO HOSPITALS - CLINICAL LABORATORY REPORT
Date: January 12, 2026 | Specimen ID: AP-88319
Patient: Rahul Sharma | Age: 29 | Gender: Male | MRN: AP-10294
Ordering Physician: Dr. Sunita Rao, MD

COMPLETE BLOOD COUNT (CBC):
- Hemoglobin (Hb): 11.8 g/dL [Low] (Reference Range: 13.5 - 17.5 g/dL)
- RBC Count: 4.1 million/uL [Low] (Reference: 4.5 - 5.9)
- Packed Cell Volume (PCV): 35.2 % [Low] (Reference: 40 - 50)
- MCV: 76.4 fL [Low] (Reference: 80 - 100 fL) - Microcytic
- MCH: 24.1 pg [Low] (Reference: 27 - 33 pg) - Hypochromic
- White Blood Cell Count (WBC): 6,400 /uL [Normal] (Reference: 4,000 - 11,000)
- Platelet Count: 245,000 /uL [Normal] (Reference: 150,000 - 450,000)
- Serum Ferritin: 11 ng/mL [Low] (Reference: 30 - 400 ng/mL)

IMPRESSION: Microcytic hypochromic anemia consistent with iron deficiency. Recommend clinical correlation and iron supplementation."""
        ),
        MedicalDocument(
            id="doc-p0-02",
            title="General Medicine Outpatient Consultation & Prescription",
            doc_type="Prescription",
            date="2026-01-18",
            author="Dr. Sunita Rao, MD (Internal Medicine)",
            facility="Apollo Medical Centre",
            file_name="prescription_18jan.jpg",
            raw_text="""APOLLO MEDICAL CENTRE - PRESCRIPTION
Date: 18/01/2026
Patient: Rahul Sharma | Age: 29

CHIEF COMPLAINT: Generalized fatigue, lethargy, exertional dyspnea for 3 weeks.
REVIEW OF LABS: CBC from 12/01/2026 demonstrates microcytic anemia with Hb 11.8 g/dL and low ferritin (11 ng/mL).
DIAGNOSIS: Iron Deficiency Anemia.

PRESCRIPTION:
1. Ferrous Ascorbate + Folic Acid (Iron supplement) 100 mg elemental iron PO once daily after dinner x 3 months.
2. Methylcobalamin (Vitamin B12) 1500 mcg PO once daily morning x 1 month.
3. Dietary advice: Increase dietary leafy greens, legumes, and citrus fruits.
4. PLAN: Recheck CBC in 2 months (March 2026)."""
        ),
        MedicalDocument(
            id="doc-p0-03",
            title="Follow-up Complete Blood Count (CBC)",
            doc_type="Lab Report",
            date="2026-03-20",
            author="Apollo Diagnostics Clinical Laboratory",
            facility="Apollo Hospital Central Lab",
            file_name="blood_report_mar.pdf",
            raw_text="""APOLLO HOSPITALS - CLINICAL LABORATORY REPORT
Date: March 20, 2026
Patient: Rahul Sharma | Ordering: Dr. Sunita Rao, MD

COMPLETE BLOOD COUNT (CBC):
- Hemoglobin (Hb): 12.9 g/dL [Mild Improvement] (Reference Range: 13.5 - 17.5 g/dL)
- RBC Count: 4.5 million/uL [Normal]
- Packed Cell Volume (PCV): 38.6 % [Borderline]
- MCV: 82.1 fL [Normal]
- Serum Ferritin: 28 ng/mL [Improving]

COMMENT: Positive hematological response to oral iron therapy. Hemoglobin increased from 11.8 to 12.9 g/dL (+1.1 g/dL). Continue therapy."""
        ),
        MedicalDocument(
            id="doc-p0-04",
            title="Progress Evaluation & Refill Prescription",
            doc_type="Prescription",
            date="2026-05-15",
            author="Dr. Sunita Rao, MD",
            facility="Apollo Medical Centre",
            file_name="prescription_may.pdf",
            raw_text="""APOLLO MEDICAL CENTRE - CLINICAL PROGRESS NOTE
Date: May 15, 2026
Patient: Rahul Sharma

ASSESSMENT: Patient reports significant improvement in stamina and energy.
MEDICATION REVIEW:
- Ferrous Ascorbate (Iron supplement) 100 mg daily - Refill authorized for 30 days.
- Vitamin B12 course completed in February.
INSTRUCTION: Continue iron until end of June. Repeat CBC in June."""
        ),
        MedicalDocument(
            id="doc-p0-05",
            title="Diagnostic Hematology Evaluation - Mid-Year CBC",
            doc_type="Lab Report",
            date="2026-06-14",
            author="Metropolis Healthcare Pathology",
            facility="Metropolis Diagnostic Laboratory",
            file_name="CBC_June.pdf",
            raw_text="""METROPOLIS HEALTHCARE - PATHOLOGY REPORT
Date: 14/06/2026
Patient: Rahul Sharma | Age: 29 | Gender: Male
Client ID: MET-49021

HEMATOLOGY PROFILE:
- Hemoglobin: 13.7 g/dL [Normal] (Reference Range: 13.0 - 17.0 g/dL)
- Total WBC Count: 7,200 /uL [Normal] (Reference: 4,000 - 10,000)
- Platelets: 240,000 /uL [Normal] (Reference: 150,000 - 410,000)
- Packed Cell Volume (PCV): 41.2 % [Normal] (Reference: 40 - 50)
- MCV: 85.4 fL [Normal]
- MCH: 28.6 pg [Normal]

INTERPRETATION: Complete normalization of red cell indices and hemoglobin. Anemia resolved."""
        ),
        MedicalDocument(
            id="doc-p0-06",
            title="General Health Check & Annual CBC",
            doc_type="Lab Report",
            date="2026-08-12",
            author="Apollo Hospital Diagnostic Centre",
            facility="Apollo Hospital Central Lab",
            file_name="CBC_Aug.pdf",
            raw_text="""APOLLO HOSPITALS - ANNUAL HEALTH CHECK
Date: August 12, 2026
Patient: Rahul Sharma

LABORATORY FINDINGS:
- Hemoglobin: 14.1 g/dL [Normal / Robust] (Reference: 13.5 - 17.5 g/dL)
- Fasting Glucose: 92 mg/dL [Normal] (Reference: 70 - 100 mg/dL)
- Serum Creatinine: 0.95 mg/dL [Normal] (Reference: 0.70 - 1.20 mg/dL)
- Blood Pressure: 118/76 mmHg [Optimal]

NOTE: Patient has discontinued iron supplement as planned following normalization. No current medications documented."""
        )
    ]

    timeline = [
        TimelineEvent(
            id="ev-p0-01",
            date="2026-01-12",
            category="Laboratory",
            title="Blood Test: Hemoglobin 11.8 g/dL (Low)",
            summary="Initial CBC revealed microcytic hypochromic anemia with Hemoglobin at 11.8 g/dL and low ferritin (11 ng/mL).",
            details={"hb": 11.8, "ferritin": 11, "mcv": 76.4, "status": "Anemia detected"},
            clinician="Apollo Diagnostics",
            facility="Apollo Hospital Central Lab",
            status="Warning",
            tags=["Blood Test", "Hemoglobin", "Anemia", "CBC"],
            provenance=SourceProvenance(
                document_id="doc-p0-01",
                document_name="blood_report_jan.pdf",
                date="2026-01-12",
                page_number=1,
                verbatim_quote="Hemoglobin (Hb): 11.8 g/dL [Low] (Reference Range: 13.5 - 17.5 g/dL)... Serum Ferritin: 11 ng/mL [Low]",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p0-02",
            date="2026-01-18",
            category="Prescription",
            title="Doctor Visit: Started Iron Supplement & Vitamin B12",
            summary="Dr. Sunita Rao diagnosed Iron Deficiency Anemia. Initiated Ferrous Ascorbate 100mg daily and Vitamin B12 1500mcg daily.",
            details={"started": ["Ferrous Ascorbate 100mg PO daily", "Vitamin B12 1500mcg daily"], "reason": "Fatigue and low ferritin"},
            clinician="Dr. Sunita Rao, MD",
            facility="Apollo Medical Centre",
            status="Normal",
            tags=["Doctor Visit", "Prescription", "Iron Supplement", "Vitamin B12"],
            provenance=SourceProvenance(
                document_id="doc-p0-02",
                document_name="prescription_18jan.jpg",
                date="2026-01-18",
                page_number=1,
                verbatim_quote="Ferrous Ascorbate + Folic Acid 100 mg elemental iron PO once daily... Methylcobalamin (Vitamin B12) 1500 mcg PO once daily",
                confidence_score=0.97,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p0-03",
            date="2026-03-20",
            category="Laboratory",
            title="Blood Test: Hemoglobin 12.9 g/dL (Improving)",
            summary="CBC demonstrated positive therapeutic response: Hemoglobin increased by +1.1 g/dL to 12.9 g/dL. Ferritin recovering.",
            details={"hb": 12.9, "delta": "+1.1 g/dL", "ferritin": 28},
            clinician="Apollo Diagnostics",
            facility="Apollo Hospital Central Lab",
            status="Normal",
            tags=["Blood Test", "Hemoglobin Rise", "CBC"],
            provenance=SourceProvenance(
                document_id="doc-p0-03",
                document_name="blood_report_mar.pdf",
                date="2026-03-20",
                page_number=1,
                verbatim_quote="Hemoglobin (Hb): 12.9 g/dL [Mild Improvement]... Hemoglobin increased from 11.8 to 12.9 g/dL",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p0-04",
            date="2026-05-15",
            category="Prescription",
            title="Doctor Visit: Iron Refill Authorized; Vitamin B12 Completed",
            summary="Follow-up note authorized final 30-day supply of iron supplement. Vitamin B12 marked as completed. Advised repeat CBC in June.",
            details={"iron_status": "Refill authorized x30 days", "b12_status": "Completed in Feb"},
            clinician="Dr. Sunita Rao, MD",
            facility="Apollo Medical Centre",
            status="Normal",
            tags=["Doctor Visit", "Refill", "Medication Review"],
            provenance=SourceProvenance(
                document_id="doc-p0-04",
                document_name="prescription_may.pdf",
                date="2026-05-15",
                page_number=1,
                verbatim_quote="Ferrous Ascorbate 100 mg daily - Refill authorized for 30 days. Vitamin B12 course completed.",
                confidence_score=0.96,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p0-05",
            date="2026-06-14",
            category="Laboratory",
            title="Blood Test: Hemoglobin 13.7 g/dL (Target Reached)",
            summary="Mid-year pathology panel confirmed complete resolution of anemia with Hemoglobin at 13.7 g/dL, normal WBC (7,200), and normal platelets (240k).",
            details={"hb": 13.7, "wbc": 7200, "platelets": 240000, "status": "Resolved"},
            clinician="Metropolis Healthcare",
            facility="Metropolis Diagnostic Laboratory",
            status="Resolved",
            tags=["Blood Test", "Hemoglobin Normal", "Anemia Resolved", "CBC"],
            provenance=SourceProvenance(
                document_id="doc-p0-05",
                document_name="CBC_June.pdf",
                date="2026-06-14",
                page_number=1,
                verbatim_quote="Hemoglobin: 13.7 g/dL [Normal] (Reference Range: 13.0 - 17.0 g/dL)... Complete normalization of red cell indices.",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p0-06",
            date="2026-08-12",
            category="Laboratory",
            title="Annual Check: Hemoglobin 14.1 g/dL (Optimal)",
            summary="Annual screening verified sustained remission with Hemoglobin reaching 14.1 g/dL, normal fasting glucose (92 mg/dL) and normal creatinine (0.95 mg/dL).",
            details={"hb": 14.1, "glucose": 92, "creatinine": 0.95, "medications": "None ongoing"},
            clinician="Apollo Hospital Central Lab",
            facility="Apollo Hospital",
            status="Resolved",
            tags=["Annual Check", "Hemoglobin Peak", "CBC", "Optimal Health"],
            provenance=SourceProvenance(
                document_id="doc-p0-06",
                document_name="CBC_Aug.pdf",
                date="2026-08-12",
                page_number=1,
                verbatim_quote="Hemoglobin: 14.1 g/dL [Normal / Robust]... Patient has discontinued iron supplement as planned following normalization.",
                confidence_score=0.99,
                certainty_level="High"
            )
        )
    ]

    labs = [
        LabMetricSeries(
            test_name="Hemoglobin",
            category="Hematology",
            unit="g/dL",
            normal_min=13.0,
            normal_max=17.5,
            trend_interpretation="Marked longitudinal rise from 11.8 g/dL (Jan) to 14.1 g/dL (Aug) following 4-month iron supplementation course. Complete hematological resolution.",
            points=[
                LabDataPoint(
                    date="2026-01-12",
                    value=11.8,
                    unit="g/dL",
                    flag="Low",
                    reference_range="13.5 - 17.5 g/dL",
                    doc_id="doc-p0-01",
                    provenance=SourceProvenance(
                        document_id="doc-p0-01",
                        document_name="blood_report_jan.pdf",
                        date="2026-01-12",
                        page_number=1,
                        verbatim_quote="Hemoglobin (Hb): 11.8 g/dL [Low]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2026-03-20",
                    value=12.9,
                    unit="g/dL",
                    flag="Low",
                    reference_range="13.5 - 17.5 g/dL",
                    doc_id="doc-p0-03",
                    provenance=SourceProvenance(
                        document_id="doc-p0-03",
                        document_name="blood_report_mar.pdf",
                        date="2026-03-20",
                        page_number=1,
                        verbatim_quote="Hemoglobin (Hb): 12.9 g/dL [Mild Improvement]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2026-06-14",
                    value=13.7,
                    unit="g/dL",
                    flag="Normal",
                    reference_range="13.0 - 17.0 g/dL",
                    doc_id="doc-p0-05",
                    provenance=SourceProvenance(
                        document_id="doc-p0-05",
                        document_name="CBC_June.pdf",
                        date="2026-06-14",
                        page_number=1,
                        verbatim_quote="Hemoglobin: 13.7 g/dL [Normal]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2026-08-12",
                    value=14.1,
                    unit="g/dL",
                    flag="Normal",
                    reference_range="13.5 - 17.5 g/dL",
                    doc_id="doc-p0-06",
                    provenance=SourceProvenance(
                        document_id="doc-p0-06",
                        document_name="CBC_Aug.pdf",
                        date="2026-08-12",
                        page_number=1,
                        verbatim_quote="Hemoglobin: 14.1 g/dL [Normal / Robust]",
                        confidence_score=0.99
                    )
                )
            ]
        ),
        LabMetricSeries(
            test_name="Serum Ferritin",
            category="Hematology",
            unit="ng/mL",
            normal_min=30.0,
            normal_max=400.0,
            trend_interpretation="Iron stores replenished from depleted baseline of 11 ng/mL to 28 ng/mL.",
            points=[
                LabDataPoint(
                    date="2026-01-12",
                    value=11.0,
                    unit="ng/mL",
                    flag="Low",
                    reference_range="30 - 400 ng/mL",
                    doc_id="doc-p0-01",
                    provenance=SourceProvenance(
                        document_id="doc-p0-01",
                        document_name="blood_report_jan.pdf",
                        date="2026-01-12",
                        page_number=1,
                        verbatim_quote="Serum Ferritin: 11 ng/mL [Low]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2026-03-20",
                    value=28.0,
                    unit="ng/mL",
                    flag="Low",
                    reference_range="30 - 400 ng/mL",
                    doc_id="doc-p0-03",
                    provenance=SourceProvenance(
                        document_id="doc-p0-03",
                        document_name="blood_report_mar.pdf",
                        date="2026-03-20",
                        page_number=1,
                        verbatim_quote="Serum Ferritin: 28 ng/mL [Improving]",
                        confidence_score=0.99
                    )
                )
            ]
        ),
        LabMetricSeries(
            test_name="White Blood Cell Count (WBC)",
            category="Hematology",
            unit="/uL",
            normal_min=4000.0,
            normal_max=11000.0,
            trend_interpretation="Stable normal leukocyte counts across all 4 evaluations (6,400 to 7,200 /uL).",
            points=[
                LabDataPoint(
                    date="2026-01-12",
                    value=6400.0,
                    unit="/uL",
                    flag="Normal",
                    reference_range="4,000 - 11,000",
                    doc_id="doc-p0-01",
                    provenance=SourceProvenance(
                        document_id="doc-p0-01",
                        document_name="blood_report_jan.pdf",
                        date="2026-01-12",
                        page_number=1,
                        verbatim_quote="White Blood Cell Count (WBC): 6,400 /uL",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2026-06-14",
                    value=7200.0,
                    unit="/uL",
                    flag="Normal",
                    reference_range="4,000 - 10,000",
                    doc_id="doc-p0-05",
                    provenance=SourceProvenance(
                        document_id="doc-p0-05",
                        document_name="CBC_June.pdf",
                        date="2026-06-14",
                        page_number=1,
                        verbatim_quote="Total WBC Count: 7,200 /uL [Normal]",
                        confidence_score=0.99
                    )
                )
            ]
        )
    ]

    meds = [
        MedicationRecord(
            id="med-p0-01",
            name="Ferrous Ascorbate (Iron Supplement)",
            dosage="100 mg elemental iron",
            frequency="Once daily (evening)",
            route="Oral",
            start_date="2026-01-18",
            end_date="2026-06-15",
            status="Discontinued",
            indication="Iron Deficiency Anemia",
            change_reason="First documented: Jan 18, 2026. Last documented mention: May 15, 2026. Discontinued in June upon documented resolution of anemia (Hb 13.7 g/dL).",
            provenance=SourceProvenance(
                document_id="doc-p0-02",
                document_name="prescription_18jan.jpg",
                date="2026-01-18",
                page_number=1,
                verbatim_quote="Ferrous Ascorbate + Folic Acid 100 mg elemental iron PO once daily",
                confidence_score=0.97
            )
        ),
        MedicationRecord(
            id="med-p0-02",
            name="Methylcobalamin (Vitamin B12)",
            dosage="1500 mcg",
            frequency="Once daily (morning)",
            route="Oral",
            start_date="2026-01-18",
            end_date="2026-02-18",
            status="Discontinued",
            indication="Nutritional Anemia Support",
            change_reason="Completed planned 30-day oral replenishment course in February 2026.",
            provenance=SourceProvenance(
                document_id="doc-p0-02",
                document_name="prescription_18jan.jpg",
                date="2026-01-18",
                page_number=1,
                verbatim_quote="Methylcobalamin (Vitamin B12) 1500 mcg PO once daily morning x 1 month",
                confidence_score=0.98
            )
        )
    ]

    discrepancies = [
        DiscrepancyItem(
            id="disc-p0-01",
            type="Missing Information",
            severity="Warning",
            title="Iron Supplement Discontinuation Gap",
            description="Iron supplement (Ferrous Ascorbate) was authorized for 30-day refill on May 15, 2026. No subsequent medication list or discontinuation note was found in records after May 2026 until August confirmation.",
            involved_documents=["prescription_may.pdf", "CBC_June.pdf"],
            evidence_quotes=[
                "Refill authorized for 30 days. Continue iron until end of June.",
                "Patient has discontinued iron supplement as planned following normalization."
            ],
            clinical_recommendation="Surfaced for review: Confirm exact date of iron cessation and ensure patient maintains adequate dietary iron intake."
        )
    ]

    relationships = [
        RelationshipLink(
            id="rel-p0-01",
            source_id="ev-p0-01",
            source_label="Lab: Hemoglobin 11.8 g/dL (Jan 12, 2026)",
            target_id="ev-p0-02",
            target_label="Rx: Iron & B12 Started (Jan 18, 2026)",
            relation_type="Triggered By",
            description="Physician initiated oral iron and Vitamin B12 directly in response to microcytic anemia documented on Jan 12 CBC.",
            evidence_doc_id="doc-p0-02"
        ),
        RelationshipLink(
            id="rel-p0-02",
            source_id="ev-p0-02",
            source_label="Rx: Iron Supplementation Active",
            target_id="ev-p0-05",
            target_label="Lab: Hemoglobin Normalized to 13.7 g/dL (June 14)",
            relation_type="Followed Up By",
            description="Hematological resolution achieved following 5-month iron therapy with steady rise from 11.8 to 13.7 g/dL.",
            evidence_doc_id="doc-p0-05"
        )
    ]

    return PatientProfile(
        id="p0",
        name="Rahul Sharma",
        age=29,
        gender="Male",
        mrn="AP-10294",
        blood_type="O+",
        summary="29-year-old male with documented recovery from Iron Deficiency Anemia over 8 months. Longitudinal records track steady Hemoglobin improvement (11.8 -> 14.1 g/dL) following Ferrous Ascorbate initiation, with successful planned cessation.",
        chronic_conditions=["Iron Deficiency Anemia (Resolved)", "Fatigue (Resolved)"],
        allergies=["No Known Drug Allergies"],
        documents=docs,
        timeline=timeline,
        labs=labs,
        medications=meds,
        discrepancies=discrepancies,
        relationships=relationships
    )
