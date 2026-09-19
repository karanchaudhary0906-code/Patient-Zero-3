from app.models import (
    PatientProfile, MedicalDocument, TimelineEvent,
    LabMetricSeries, LabDataPoint, MedicationRecord,
    DiscrepancyItem, RelationshipLink, SourceProvenance
)

def get_p1() -> PatientProfile:
    docs = [
        MedicalDocument(
            id="doc-p1-01",
            title="Primary Care Initial Assessment & Management Plan",
            doc_type="Clinical Note",
            date="2022-10-12",
            author="Dr. Robert Hayes, MD",
            facility="MetroHealth Family Clinic",
            file_name="2022-10-12_Encounter_Hayes.pdf",
            raw_text="METROHEALTH FAMILY CLINIC - ENCOUNTER NOTE\nDate: October 12, 2022\nPatient: Eleanor Vance | DOB: 1958-03-14 | MRN: MH-88492\nAttending: Dr. Robert Hayes, MD\n\nCHIEF COMPLAINT: Routine health maintenance and fatigue.\nASSESSMENT:\n1. Type 2 Diabetes Mellitus, newly uncontrolled. Random fingerstick 210 mg/dL.\n2. Essential Hypertension, Stage 1. BP today 152/92 mmHg.\nPLAN:\n- Initiate Metformin 500 mg PO once daily with dinner. Titrate to BID after 2 weeks if tolerated.\n- Initiate Lisinopril 10 mg PO once daily in morning for hypertension & renal protection.\n- Ordered baseline Comprehensive Metabolic Panel and HbA1c in 3 months.\n- Follow up in 3-4 months with lab results."
        ),
        MedicalDocument(
            id="doc-p1-02",
            title="Comprehensive Laboratory Report - Glycemic & Renal Panel",
            doc_type="Lab Report",
            date="2023-01-18",
            author="Quest Diagnostics Clinical Laboratory",
            facility="Quest Diagnostics Central",
            file_name="2023-01-18_Quest_Panel.pdf",
            raw_text="QUEST DIAGNOSTICS - CLINICAL REPORT\nSpecimen ID: QD-99201-B | Collected: 2023-01-18 07:45 AM\nPatient: Eleanor Vance | Ordering: Dr. Robert Hayes, MD\n\nTEST RESULTS:\n- Hemoglobin A1c: 8.4 % [H] (Reference: < 5.7 %, Target in DM < 7.0 %)\n- Fasting Glucose: 168 mg/dL [H] (Reference: 70 - 99 mg/dL)\n- Serum Creatinine: 0.92 mg/dL [Normal] (Reference: 0.50 - 1.10 mg/dL)\n- eGFR: > 90 mL/min/1.73m2 [Normal]\n- Blood Urea Nitrogen (BUN): 16 mg/dL [Normal]\n- Total Cholesterol: 215 mg/dL [H]\n- LDL Cholesterol: 134 mg/dL [H]\nCOMMENT: Glycemic targets not achieved on current initial monotherapy."
        ),
        MedicalDocument(
            id="doc-p1-03",
            title="Endocrinology Consultation & Medication Adjustment",
            doc_type="Clinical Note",
            date="2023-02-02",
            author="Dr. Angela Thorne, MD",
            facility="University Endocrine Center",
            file_name="2023-02-02_Endo_Thorne.pdf",
            raw_text="UNIVERSITY ENDOCRINE CENTER - SPECIALIST CONSULT\nDate: February 02, 2023\nPatient: Eleanor Vance\n\nREVIEW OF LABS (Quest 2023-01-18):\nHbA1c 8.4% demonstrates suboptimal control on Metformin 500mg QD. Renal function intact (Creatinine 0.92).\nACTION PLAN:\n1. Intensify Metformin to 1000 mg PO twice daily (BID) with meals.\n2. Continue Lisinopril 10 mg QD.\n3. Recommend dietary carbohydrate moderation.\n4. ORDERED: Urine Albumin-to-Creatinine Ratio (UACR) to evaluate for diabetic microalbuminuria.\n5. Recheck HbA1c in 6 months."
        ),
        MedicalDocument(
            id="doc-p1-04",
            title="Urgent Care Visit - Persistent Cough & ACE-Inhibitor Reaction",
            doc_type="Clinical Note",
            date="2023-08-14",
            author="Dr. Karen Liu, MD",
            facility="Midtown Urgent Care Center",
            file_name="2023-08-14_UrgentCare_Liu.pdf",
            raw_text="MIDTOWN URGENT CARE CLINICAL SUMMARY\nDate: August 14, 2023\nPatient: Eleanor Vance | Age: 65\n\nCHIEF COMPLAINT: Dry hacking cough for past 6 weeks, non-productive, worse at night.\nEXAM: Lungs clear bilaterally. Afebrile.\nMEDICATION REVIEW: Lisinopril 10mg started approx 10 months ago.\nASSESSMENT: Suspected ACE inhibitor-induced dry cough.\nPLAN:\n- Discontinue Lisinopril 10 mg immediately.\n- Switch to ARB class: Prescribed Losartan potassium 50 mg PO once daily.\n- Follow up if cough persists beyond 2-3 weeks."
        ),
        MedicalDocument(
            id="doc-p1-05",
            title="Laboratory Evaluation - Follow-up Glycemic & Metabolic Panel",
            doc_type="Lab Report",
            date="2023-09-05",
            author="MetroHealth Pathology Lab",
            facility="MetroHealth Diagnostic Services",
            file_name="2023-09-05_Lab_Followup.pdf",
            raw_text="METROHEALTH PATHOLOGY REPORT\nDate: September 05, 2023\nPatient: Eleanor Vance\n\nRESULTS:\n- Hemoglobin A1c: 7.1 % [Moderate Improvement] (Baseline 8.4%)\n- Fasting Glucose: 132 mg/dL [H] (Baseline 168 mg/dL)\n- Serum Creatinine: 1.02 mg/dL [Normal] (Reference: 0.50 - 1.10 mg/dL)\n- Potassium: 4.4 mmol/L [Normal]\n- Blood Pressure: 138/84 mmHg\nCLINICAL NOTE: Significant glycemic improvement following Metformin titration."
        ),
        MedicalDocument(
            id="doc-p1-06",
            title="Cardiology / Internal Medicine Annual Review",
            doc_type="Clinical Note",
            date="2024-05-20",
            author="Dr. Robert Hayes, MD",
            facility="MetroHealth Family Clinic",
            file_name="2024-05-20_Annual_Hayes.pdf",
            raw_text="METROHEALTH CLINICAL PROGRESS NOTE\nDate: May 20, 2024\nPatient: Eleanor Vance\n\nHISTORY & REVIEW:\n- ACE-induced cough resolved completely after switching to Losartan 50mg.\n- Blood pressure well managed at 124/78 mmHg on Losartan.\n- Latest in-office HbA1c: 6.8% [Target Achieved < 7.0%].\n- Serum Creatinine noted at 1.35 mg/dL [Mild Elevation - baseline was 0.92-1.02].\n- Patient reports adherence to Metformin 1000mg BID and Losartan 50mg QD.\nPLAN:\n- Monitor renal panel closely; repeat Creatinine & eGFR in 3 months.\n- Re-check urine microalbumin (noted missing from records)."
        )
    ]

    timeline = [
        TimelineEvent(
            id="ev-p1-01",
            date="2022-10-12",
            category="Consultation",
            title="Initial T2D & Hypertension Diagnosis",
            summary="Diagnosed with Type 2 Diabetes and Stage 1 Hypertension. Started on Metformin 500mg QD and Lisinopril 10mg QD.",
            details={"bp": "152/92 mmHg", "random_glucose": "210 mg/dL", "action": "Initiated dual therapy"},
            clinician="Dr. Robert Hayes, MD",
            facility="MetroHealth Family Clinic",
            status="Warning",
            tags=["Diabetes", "Hypertension", "Medication Start"],
            provenance=SourceProvenance(
                document_id="doc-p1-01",
                document_name="2022-10-12_Encounter_Hayes.pdf",
                date="2022-10-12",
                page_number=1,
                verbatim_quote="Initiate Metformin 500 mg PO once daily with dinner... Initiate Lisinopril 10 mg PO once daily in morning.",
                confidence_score=0.98,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p1-02",
            date="2023-01-18",
            category="Laboratory",
            title="Baseline Quest Panel: Elevated HbA1c (8.4%)",
            summary="Lab panel reveals uncontrolled glycemic markers with HbA1c at 8.4% and fasting glucose 168 mg/dL. Renal indices normal.",
            details={"hba1c": 8.4, "glucose": 168, "creatinine": 0.92, "ldl": 134},
            clinician="Quest Diagnostics",
            facility="Quest Diagnostics Central",
            status="Critical",
            tags=["Lab Panel", "HbA1c Spike", "Dyslipidemia"],
            provenance=SourceProvenance(
                document_id="doc-p1-02",
                document_name="2023-01-18_Quest_Panel.pdf",
                date="2023-01-18",
                page_number=1,
                verbatim_quote="Hemoglobin A1c: 8.4 % [H] (Reference: < 5.7 %)... Fasting Glucose: 168 mg/dL [H].",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p1-03",
            date="2023-02-02",
            category="Prescription",
            title="Metformin Titration to 1000mg BID & Missing UACR",
            summary="Endocrinologist increased Metformin to 1000mg BID due to HbA1c 8.4%. Ordered Urine Albumin/Creatinine Ratio (not subsequently fulfilled).",
            details={"metformin_change": "500mg QD -> 1000mg BID", "order": "Urine Microalbumin"},
            clinician="Dr. Angela Thorne, MD",
            facility="University Endocrine Center",
            status="Normal",
            tags=["Titration", "Endocrinology", "Orders Pending"],
            provenance=SourceProvenance(
                document_id="doc-p1-03",
                document_name="2023-02-02_Endo_Thorne.pdf",
                date="2023-02-02",
                page_number=1,
                verbatim_quote="Intensify Metformin to 1000 mg PO twice daily (BID)... ORDERED: Urine Albumin-to-Creatinine Ratio (UACR).",
                confidence_score=0.96,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p1-04",
            date="2023-08-14",
            category="Prescription",
            title="Adverse Drug Reaction: ACE-Inhibitor Cough & Losartan Switch",
            summary="Urgent care assessment identified chronic cough as adverse reaction to Lisinopril. Discontinued Lisinopril and substituted Losartan 50mg QD.",
            details={"discontinued": "Lisinopril 10mg", "started": "Losartan 50mg QD", "reaction": "Dry intractable cough"},
            clinician="Dr. Karen Liu, MD",
            facility="Midtown Urgent Care Center",
            status="Warning",
            tags=["Adverse Reaction", "Medication Switch", "Urgent Care"],
            provenance=SourceProvenance(
                document_id="doc-p1-04",
                document_name="2023-08-14_UrgentCare_Liu.pdf",
                date="2023-08-14",
                page_number=1,
                verbatim_quote="Discontinue Lisinopril 10 mg immediately. Switch to ARB class: Prescribed Losartan potassium 50 mg PO once daily.",
                confidence_score=0.94,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p1-05",
            date="2023-09-05",
            category="Laboratory",
            title="Follow-up Glycemic Panel: HbA1c Drops to 7.1%",
            summary="Demonstrated significant metabolic response to Metformin titration: HbA1c reduced from 8.4% to 7.1%. Normal potassium and renal function.",
            details={"hba1c": 7.1, "glucose": 132, "creatinine": 1.02, "potassium": 4.4},
            clinician="MetroHealth Diagnostics",
            facility="MetroHealth Pathology Lab",
            status="Resolved",
            tags=["Lab Panel", "HbA1c Improvement", "Glycemic Control"],
            provenance=SourceProvenance(
                document_id="doc-p1-05",
                document_name="2023-09-05_Lab_Followup.pdf",
                date="2023-09-05",
                page_number=1,
                verbatim_quote="Hemoglobin A1c: 7.1 % [Moderate Improvement] (Baseline 8.4%)... Fasting Glucose: 132 mg/dL.",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p1-06",
            date="2024-05-20",
            category="Consultation",
            title="Annual Review: Target HbA1c (6.8%) with Mild Creatinine Elevation",
            summary="Patient reached glycemic target HbA1c 6.8% and BP 124/78 mmHg. However, Creatinine rose to 1.35 mg/dL requiring renal monitoring.",
            details={"hba1c": 6.8, "creatinine": 1.35, "bp": "124/78 mmHg"},
            clinician="Dr. Robert Hayes, MD",
            facility="MetroHealth Family Clinic",
            status="Warning",
            tags=["Annual Review", "Renal Alert", "Goal Reached"],
            provenance=SourceProvenance(
                document_id="doc-p1-06",
                document_name="2024-05-20_Annual_Hayes.pdf",
                date="2024-05-20",
                page_number=1,
                verbatim_quote="Latest in-office HbA1c: 6.8% [Target Achieved < 7.0%]... Serum Creatinine noted at 1.35 mg/dL [Mild Elevation].",
                confidence_score=0.97,
                certainty_level="High"
            )
        )
    ]

    labs = [
        LabMetricSeries(
            test_name="Hemoglobin A1c",
            category="Glycemic",
            unit="%",
            normal_min=4.0,
            normal_max=5.7,
            trend_interpretation="Marked improvement from uncontrolled baseline (8.4%) to goal (6.8%) following Metformin dosage titration.",
            points=[
                LabDataPoint(
                    date="2023-01-18",
                    value=8.4,
                    unit="%",
                    flag="High",
                    reference_range="< 5.7 %",
                    doc_id="doc-p1-02",
                    provenance=SourceProvenance(
                        document_id="doc-p1-02",
                        document_name="2023-01-18_Quest_Panel.pdf",
                        date="2023-01-18",
                        page_number=1,
                        verbatim_quote="Hemoglobin A1c: 8.4 % [H]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2023-09-05",
                    value=7.1,
                    unit="%",
                    flag="High",
                    reference_range="< 5.7 %",
                    doc_id="doc-p1-05",
                    provenance=SourceProvenance(
                        document_id="doc-p1-05",
                        document_name="2023-09-05_Lab_Followup.pdf",
                        date="2023-09-05",
                        page_number=1,
                        verbatim_quote="Hemoglobin A1c: 7.1 % [Moderate Improvement]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2024-05-20",
                    value=6.8,
                    unit="%",
                    flag="Normal",
                    reference_range="< 5.7 %",
                    doc_id="doc-p1-06",
                    provenance=SourceProvenance(
                        document_id="doc-p1-06",
                        document_name="2024-05-20_Annual_Hayes.pdf",
                        date="2024-05-20",
                        page_number=1,
                        verbatim_quote="Latest in-office HbA1c: 6.8% [Target Achieved]",
                        confidence_score=0.97
                    )
                )
            ]
        ),
        LabMetricSeries(
            test_name="Serum Creatinine",
            category="Renal",
            unit="mg/dL",
            normal_min=0.50,
            normal_max=1.10,
            trend_interpretation="Gradual upward drift from normal baseline (0.92 mg/dL) to mildly elevated (1.35 mg/dL) at 19 months.",
            points=[
                LabDataPoint(
                    date="2023-01-18",
                    value=0.92,
                    unit="mg/dL",
                    flag="Normal",
                    reference_range="0.50 - 1.10 mg/dL",
                    doc_id="doc-p1-02",
                    provenance=SourceProvenance(
                        document_id="doc-p1-02",
                        document_name="2023-01-18_Quest_Panel.pdf",
                        date="2023-01-18",
                        page_number=1,
                        verbatim_quote="Serum Creatinine: 0.92 mg/dL [Normal]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2023-09-05",
                    value=1.02,
                    unit="mg/dL",
                    flag="Normal",
                    reference_range="0.50 - 1.10 mg/dL",
                    doc_id="doc-p1-05",
                    provenance=SourceProvenance(
                        document_id="doc-p1-05",
                        document_name="2023-09-05_Lab_Followup.pdf",
                        date="2023-09-05",
                        page_number=1,
                        verbatim_quote="Serum Creatinine: 1.02 mg/dL [Normal]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2024-05-20",
                    value=1.35,
                    unit="mg/dL",
                    flag="High",
                    reference_range="0.50 - 1.10 mg/dL",
                    doc_id="doc-p1-06",
                    provenance=SourceProvenance(
                        document_id="doc-p1-06",
                        document_name="2024-05-20_Annual_Hayes.pdf",
                        date="2024-05-20",
                        page_number=1,
                        verbatim_quote="Serum Creatinine noted at 1.35 mg/dL [Mild Elevation]",
                        confidence_score=0.97
                    )
                )
            ]
        ),
        LabMetricSeries(
            test_name="Fasting Blood Glucose",
            category="Glycemic",
            unit="mg/dL",
            normal_min=70.0,
            normal_max=99.0,
            trend_interpretation="Steady reduction from 168 mg/dL to 118 mg/dL.",
            points=[
                LabDataPoint(
                    date="2023-01-18",
                    value=168.0,
                    unit="mg/dL",
                    flag="High",
                    reference_range="70 - 99 mg/dL",
                    doc_id="doc-p1-02",
                    provenance=SourceProvenance(
                        document_id="doc-p1-02",
                        document_name="2023-01-18_Quest_Panel.pdf",
                        date="2023-01-18",
                        page_number=1,
                        verbatim_quote="Fasting Glucose: 168 mg/dL [H]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2023-09-05",
                    value=132.0,
                    unit="mg/dL",
                    flag="High",
                    reference_range="70 - 99 mg/dL",
                    doc_id="doc-p1-05",
                    provenance=SourceProvenance(
                        document_id="doc-p1-05",
                        document_name="2023-09-05_Lab_Followup.pdf",
                        date="2023-09-05",
                        page_number=1,
                        verbatim_quote="Fasting Glucose: 132 mg/dL",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2024-05-20",
                    value=118.0,
                    unit="mg/dL",
                    flag="High",
                    reference_range="70 - 99 mg/dL",
                    doc_id="doc-p1-06",
                    provenance=SourceProvenance(
                        document_id="doc-p1-06",
                        document_name="2024-05-20_Annual_Hayes.pdf",
                        date="2024-05-20",
                        page_number=1,
                        verbatim_quote="In-office glucose 118 mg/dL fasting",
                        confidence_score=0.95
                    )
                )
            ]
        ),
        LabMetricSeries(
            test_name="Systolic Blood Pressure",
            category="Cardiovascular",
            unit="mmHg",
            normal_min=90.0,
            normal_max=120.0,
            trend_interpretation="Controlled from Stage 1 HTN (152 mmHg) to normotensive (124 mmHg) after transitioning to Losartan.",
            points=[
                LabDataPoint(
                    date="2022-10-12",
                    value=152.0,
                    unit="mmHg",
                    flag="High",
                    reference_range="90 - 120 mmHg",
                    doc_id="doc-p1-01",
                    provenance=SourceProvenance(
                        document_id="doc-p1-01",
                        document_name="2022-10-12_Encounter_Hayes.pdf",
                        date="2022-10-12",
                        page_number=1,
                        verbatim_quote="BP today 152/92 mmHg.",
                        confidence_score=0.98
                    )
                ),
                LabDataPoint(
                    date="2023-09-05",
                    value=138.0,
                    unit="mmHg",
                    flag="High",
                    reference_range="90 - 120 mmHg",
                    doc_id="doc-p1-05",
                    provenance=SourceProvenance(
                        document_id="doc-p1-05",
                        document_name="2023-09-05_Lab_Followup.pdf",
                        date="2023-09-05",
                        page_number=1,
                        verbatim_quote="Blood Pressure: 138/84 mmHg",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2024-05-20",
                    value=124.0,
                    unit="mmHg",
                    flag="Normal",
                    reference_range="90 - 120 mmHg",
                    doc_id="doc-p1-06",
                    provenance=SourceProvenance(
                        document_id="doc-p1-06",
                        document_name="2024-05-20_Annual_Hayes.pdf",
                        date="2024-05-20",
                        page_number=1,
                        verbatim_quote="Blood pressure well managed at 124/78 mmHg",
                        confidence_score=0.97
                    )
                )
            ]
        )
    ]

    meds = [
        MedicationRecord(
            id="med-p1-01",
            name="Metformin HCl",
            dosage="500 mg",
            frequency="Once daily",
            route="Oral",
            start_date="2022-10-12",
            end_date="2023-02-02",
            status="Adjusted",
            indication="Type 2 Diabetes Mellitus",
            change_reason="Titrated up to 1000mg BID due to uncontrolled HbA1c 8.4%",
            provenance=SourceProvenance(
                document_id="doc-p1-01",
                document_name="2022-10-12_Encounter_Hayes.pdf",
                date="2022-10-12",
                page_number=1,
                verbatim_quote="Initiate Metformin 500 mg PO once daily with dinner.",
                confidence_score=0.98
            )
        ),
        MedicationRecord(
            id="med-p1-02",
            name="Metformin HCl Extended Release",
            dosage="1000 mg",
            frequency="Twice daily (BID)",
            route="Oral",
            start_date="2023-02-02",
            end_date=None,
            status="Active",
            indication="Type 2 Diabetes Mellitus",
            change_reason="Dose intensification by Endocrinology",
            provenance=SourceProvenance(
                document_id="doc-p1-03",
                document_name="2023-02-02_Endo_Thorne.pdf",
                date="2023-02-02",
                page_number=1,
                verbatim_quote="Intensify Metformin to 1000 mg PO twice daily (BID) with meals.",
                confidence_score=0.96
            )
        ),
        MedicationRecord(
            id="med-p1-03",
            name="Lisinopril",
            dosage="10 mg",
            frequency="Once daily",
            route="Oral",
            start_date="2022-10-12",
            end_date="2023-08-14",
            status="Discontinued",
            indication="Hypertension & Renal Preservation",
            change_reason="Adverse Drug Reaction: Persistent intractable cough (ACEi-mediated).",
            provenance=SourceProvenance(
                document_id="doc-p1-04",
                document_name="2023-08-14_UrgentCare_Liu.pdf",
                date="2023-08-14",
                page_number=1,
                verbatim_quote="Discontinue Lisinopril 10 mg immediately... Suspected ACE inhibitor-induced dry cough.",
                confidence_score=0.94
            )
        ),
        MedicationRecord(
            id="med-p1-04",
            name="Losartan Potassium",
            dosage="50 mg",
            frequency="Once daily",
            route="Oral",
            start_date="2023-08-14",
            end_date=None,
            status="Active",
            indication="Hypertension (ARB substitute)",
            change_reason="Substituted for Lisinopril to resolve cough while preserving blood pressure control.",
            provenance=SourceProvenance(
                document_id="doc-p1-04",
                document_name="2023-08-14_UrgentCare_Liu.pdf",
                date="2023-08-14",
                page_number=1,
                verbatim_quote="Switch to ARB class: Prescribed Losartan potassium 50 mg PO once daily.",
                confidence_score=0.94
            )
        )
    ]

    discrepancies = [
        DiscrepancyItem(
            id="disc-p1-01",
            type="Missing Follow-up",
            severity="Warning",
            title="Unfulfilled Diabetic Microalbuminuria Screening",
            description="Endocrinology consult on Feb 02, 2023 ordered a Urine Albumin-to-Creatinine Ratio (UACR) to evaluate for diabetic nephropathy. Over 15 months and 3 subsequent encounters, no record of this test being completed exists.",
            involved_documents=["2023-02-02_Endo_Thorne.pdf", "2024-05-20_Annual_Hayes.pdf"],
            evidence_quotes=[
                "ORDERED: Urine Albumin-to-Creatinine Ratio (UACR) to evaluate for diabetic microalbuminuria.",
                "Re-check urine microalbumin (noted missing from records)."
            ],
            clinical_recommendation="Schedule urine microalbumin check promptly to assess early nephropathy in light of rising serum creatinine (1.35 mg/dL)."
        ),
        DiscrepancyItem(
            id="disc-p1-02",
            type="Dosage Conflict",
            severity="Informational",
            title="Handwritten Refill vs Electronic Titration Order",
            description="Doc 3 specified Metformin 1000mg BID, but an outpatient pharmacy dispensation record noted a 30-day supply dispensed as 500mg tablets with unclear label instructions ('Take 1 tab twice daily').",
            involved_documents=["2023-02-02_Endo_Thorne.pdf"],
            evidence_quotes=[
                "Intensify Metformin to 1000 mg PO twice daily (BID) with meals."
            ],
            clinical_recommendation="Verify pill count and patient understanding: ensure patient is taking two 500mg tablets BID (or one 1000mg tablet BID) rather than underdosing at 500mg BID."
        )
    ]

    relationships = [
        RelationshipLink(
            id="rel-p1-01",
            source_id="ev-p1-02",
            source_label="Lab: HbA1c 8.4% (Jan 18, 2023)",
            target_id="ev-p1-03",
            target_label="Rx: Metformin 1000mg BID Titration (Feb 02, 2023)",
            relation_type="Triggered By",
            description="Endocrinologist increased Metformin dosage directly responding to uncontrolled HbA1c spike in Quest panel.",
            evidence_doc_id="doc-p1-03"
        ),
        RelationshipLink(
            id="rel-p1-02",
            source_id="ev-p1-01",
            source_label="Rx: Lisinopril 10mg Initiated (Oct 12, 2022)",
            target_id="ev-p1-04",
            target_label="Consult: Lisinopril Cough & Urgent Care (Aug 14, 2023)",
            relation_type="Adverse Reaction To",
            description="Patient developed chronic cough 10 months after starting Lisinopril, diagnosed as ACEi-related reaction.",
            evidence_doc_id="doc-p1-04"
        ),
        RelationshipLink(
            id="rel-p1-03",
            source_id="ev-p1-04",
            source_label="Rx: Discontinue Lisinopril -> Start Losartan 50mg",
            target_id="ev-p1-06",
            target_label="Consult: BP Controlled & Cough Resolved (May 20, 2024)",
            relation_type="Followed Up By",
            description="Transition from ACEi to ARB resolved the cough completely while preserving blood pressure control at 124/78 mmHg.",
            evidence_doc_id="doc-p1-06"
        ),
        RelationshipLink(
            id="rel-p1-04",
            source_id="ev-p1-03",
            source_label="Order: Urine Albumin Ratio Ordered (Feb 02, 2023)",
            target_id="disc-p1-01",
            target_label="Discrepancy: Missing Follow-up Microalbumin",
            relation_type="Contradicts",
            description="Diagnostic test ordered across care continuum but missing from all subsequent clinical datasets.",
            evidence_doc_id="doc-p1-06"
        )
    ]

    return PatientProfile(
        id="p1",
        name="Eleanor Vance",
        age=66,
        gender="Female",
        mrn="MH-88492",
        blood_type="A+",
        summary="66-year-old female with longitudinal cardiometabolic care tracking over 19 months. Shows successful glycemic response to Metformin titration, Lisinopril adverse reaction leading to ARB switch, with rising creatinine and an unfulfilled microalbumin order.",
        chronic_conditions=["Type 2 Diabetes Mellitus", "Essential Hypertension", "Hyperlipidemia"],
        allergies=["ACE Inhibitors (Lisinopril - intractable cough)"],
        documents=docs,
        timeline=timeline,
        labs=labs,
        medications=meds,
        discrepancies=discrepancies,
        relationships=relationships
    )
