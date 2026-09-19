from app.models import (
    PatientProfile, MedicalDocument, TimelineEvent,
    LabMetricSeries, LabDataPoint, MedicationRecord,
    DiscrepancyItem, RelationshipLink, SourceProvenance
)

def get_p2() -> PatientProfile:
    docs = [
        MedicalDocument(
            id="doc-p2-01",
            title="Pre-Operative Assessment & Baseline Labs",
            doc_type="Lab Report",
            date="2023-11-10",
            author="Dr. Samuel Green, MD",
            facility="St. Jude Surgical Pavilion",
            file_name="2023-11-10_PreOp_Assessment.pdf",
            raw_text="ST. JUDE SURGICAL PAVILION - PRE-OP CLEARANCE\nDate: November 10, 2023\nPatient: Marcus Chen | Age: 54 | MRN: SJ-55210\nPROCEDURE SCHEDULED: Right Knee Arthroscopic Partial Meniscectomy.\n\nPRE-OP LABORATORY PANEL:\n- White Blood Cell Count (WBC): 6.8 k/uL [Normal] (Reference: 4.5 - 11.0 k/uL)\n- C-Reactive Protein (CRP): 3.2 mg/L [Normal] (Reference: < 8.0 mg/L)\n- Hemoglobin: 14.8 g/dL [Normal]\n- Platelets: 245 k/uL [Normal]\nALLERGIES: No Known Drug Allergies (NKDA).\nCLEARANCE: Patient cleared for elective surgery under general anesthesia."
        ),
        MedicalDocument(
            id="doc-p2-02",
            title="Operative Procedure Summary - Right Knee Arthroscopy",
            doc_type="Discharge Summary",
            date="2023-11-24",
            author="Dr. Patricia Vance, MD",
            facility="St. Jude Surgical Pavilion",
            file_name="2023-11-24_OpNote_Meniscectomy.pdf",
            raw_text="OPERATIVE REPORT\nDate of Surgery: November 24, 2023\nSurgeon: Dr. Patricia Vance, MD\nPre/Post-Op Diagnosis: Right knee complex medial meniscus tear.\nProcedure: Right knee arthroscopy, partial medial meniscectomy.\nProphylaxis: Cefazolin 2g IV administered 30 min prior to incision.\nCOMPLICATIONS: None. Blood loss minimal. Discharged home same day."
        ),
        MedicalDocument(
            id="doc-p2-03",
            title="Emergency Department Encounter - Post-Op Joint Infection",
            doc_type="Clinical Note",
            date="2023-12-06",
            author="Dr. Jason Miller, MD",
            facility="City General Hospital Emergency Dept",
            file_name="2023-12-06_ED_Infection.pdf",
            raw_text="CITY GENERAL HOSPITAL - EMERGENCY ENCOUNTER\nDate: December 06, 2023 (Post-op Day 12)\nPatient: Marcus Chen\n\nPRESENTING SYMPTOMS: Acute right knee pain, warm erythematous swelling, body temp 38.6 C (101.5 F).\nDIAGNOSTICS:\n- Arthrocentesis: 25cc purulent synovial fluid aspirated.\n- Gram stain: Gram-positive cocci in clusters. Presumed MSSA joint infection.\n- Serum WBC: 14.2 k/uL [H] (Elevated).\n- Serum CRP: 84.0 mg/L [H] (Severe inflammatory spike).\nTREATMENT & PRESCRIPTION:\n- Prescribed: Cephalexin 500 mg PO four times daily (QID) for 14 days."
        ),
        MedicalDocument(
            id="doc-p2-04",
            title="Orthopedic Urgent Clinic Note - Conflicting Antibiotic",
            doc_type="Clinical Note",
            date="2023-12-10",
            author="Dr. Alan Ward, MD",
            facility="St. Jude Orthopedic Clinic",
            file_name="2023-12-10_Ortho_Ward.pdf",
            raw_text="ST. JUDE ORTHOPEDIC CLINIC NOTE\nDate: December 10, 2023\nPatient: Marcus Chen\n\nREASON FOR VISIT: Swollen right knee following meniscectomy.\nNOTE: Clinician notes wound erythema. ED records from City General were not in the local St. Jude EHR at time of encounter.\nASSESSMENT: Post-op superficial wound infection.\nPLAN:\n- Prescribed: Ciprofloxacin 500 mg PO twice daily (BID) x 10 days.\n- Advised knee elevation and cold compress."
        ),
        MedicalDocument(
            id="doc-p2-05",
            title="Infectious Disease Consult - Medication Reconciliation",
            doc_type="Clinical Note",
            date="2023-12-18",
            author="Dr. Rebecca Moss, MD",
            facility="City General Infectious Disease Outpatient Clinic",
            file_name="2023-12-18_ID_Reconciliation.pdf",
            raw_text="INFECTIOUS DISEASE CONSULTATION & MED RECONCILIATION\nDate: December 18, 2023\nPatient: Marcus Chen\n\nMEDICATION SAFETY ALERT REVIEW:\nSynovial fluid culture finalized as Methicillin-Susceptible Staphylococcus aureus (MSSA).\nCRITICAL SAFETY CONFLICT DETECTED:\nPatient was found taking BOTH Cephalexin 500mg QID (from ED) AND Ciprofloxacin 500mg BID (from Ortho).\nCiprofloxacin provides inferior coverage for MSSA and poses unnecessary fluoroquinolone toxicity risks.\nCORRECTIVE ACTION:\n1. STOP Ciprofloxacin immediately.\n2. CONTINUE and finish full 14-day course of Cephalexin 500mg QID.\n3. Repeat inflammatory markers (WBC, CRP) in 6-8 weeks."
        ),
        MedicalDocument(
            id="doc-p2-06",
            title="Outpatient Follow-up & Inflammatory Resolution Panel",
            doc_type="Lab Report",
            date="2024-03-02",
            author="Metro Diagnostic Central",
            facility="City General Laboratory",
            file_name="2024-03-02_Resolution_Lab.pdf",
            raw_text="CITY GENERAL LAB - INFECTION RESOLUTION PANEL\nDate: March 02, 2024\nPatient: Marcus Chen\n\nRESULTS:\n- White Blood Cell Count (WBC): 6.2 k/uL [Normal] (Baseline 6.8, Peak 14.2)\n- C-Reactive Protein (CRP): 4.1 mg/L [Normal] (Baseline 3.2, Peak 84.0)\n- Right Knee Status: No effusion, full range of motion restored, pain free.\nASSESSMENT: Complete microbiological and clinical cure of post-arthroscopy surgical site infection."
        )
    ]

    timeline = [
        TimelineEvent(
            id="ev-p2-01",
            date="2023-11-10",
            category="Laboratory",
            title="Pre-Op Baseline Clearance: Normal Biomarkers",
            summary="Pre-operative screening confirms normal WBC (6.8 k/uL) and CRP (3.2 mg/L) prior to elective knee meniscectomy.",
            details={"wbc": 6.8, "crp": 3.2, "status": "Cleared for surgery"},
            clinician="Dr. Samuel Green, MD",
            facility="St. Jude Surgical Pavilion",
            status="Normal",
            tags=["Pre-Op", "Baseline Labs", "Surgery Clearance"],
            provenance=SourceProvenance(
                document_id="doc-p2-01",
                document_name="2023-11-10_PreOp_Assessment.pdf",
                date="2023-11-10",
                page_number=1,
                verbatim_quote="White Blood Cell Count (WBC): 6.8 k/uL [Normal]... CRP: 3.2 mg/L [Normal].",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p2-02",
            date="2023-11-24",
            category="Procedure",
            title="Elective Right Knee Arthroscopy",
            summary="Partial medial meniscectomy performed with perioperative Cefazolin 2g IV. Uncomplicated procedure.",
            details={"procedure": "Right knee arthroscopy", "antibiotic_prophylaxis": "Cefazolin 2g IV"},
            clinician="Dr. Patricia Vance, MD",
            facility="St. Jude Surgical Pavilion",
            status="Normal",
            tags=["Surgery", "Orthopedics", "Meniscectomy"],
            provenance=SourceProvenance(
                document_id="doc-p2-02",
                document_name="2023-11-24_OpNote_Meniscectomy.pdf",
                date="2023-11-24",
                page_number=1,
                verbatim_quote="Procedure: Right knee arthroscopy, partial medial meniscectomy... Cefazolin 2g IV administered.",
                confidence_score=0.98,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p2-03",
            date="2023-12-06",
            category="Hospitalization",
            title="Post-Op Joint Infection & Cephalexin Prescribed",
            summary="Emergency visit on Day 12 with acute knee erythema, fever 38.6 C, WBC 14.2, CRP 84. Arthrocentesis showed MSSA. Started on Cephalexin 500mg QID.",
            details={"temp": "38.6 C", "wbc": 14.2, "crp": 84.0, "pathogen": "MSSA", "rx": "Cephalexin 500mg QID"},
            clinician="Dr. Jason Miller, MD",
            facility="City General Hospital ED",
            status="Critical",
            tags=["Surgical Site Infection", "Wound Infection", "MSSA", "Antibiotic Start"],
            provenance=SourceProvenance(
                document_id="doc-p2-03",
                document_name="2023-12-06_ED_Infection.pdf",
                date="2023-12-06",
                page_number=1,
                verbatim_quote="Serum WBC: 14.2 k/uL [H]... Serum CRP: 84.0 mg/L [H]... Prescribed: Cephalexin 500 mg PO four times daily (QID).",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p2-04",
            date="2023-12-10",
            category="Prescription",
            title="Duplicate Antibiotic Conflict: Ciprofloxacin Added",
            summary="Orthopedic fellow, unaware of the patient's existing Cephalexin regimen and culture results, prescribed Ciprofloxacin 500mg BID creating duplicate therapy risk.",
            details={"duplicate_rx": "Ciprofloxacin 500mg BID", "risk": "Dual broad-spectrum antibiotic conflict"},
            clinician="Dr. Alan Ward, MD",
            facility="St. Jude Orthopedic Clinic",
            status="Critical",
            tags=["Medication Discrepancy", "Duplicate Antibiotics", "EHR Gap"],
            provenance=SourceProvenance(
                document_id="doc-p2-04",
                document_name="2023-12-10_Ortho_Ward.pdf",
                date="2023-12-10",
                page_number=1,
                verbatim_quote="Prescribed: Ciprofloxacin 500 mg PO twice daily (BID) x 10 days.",
                confidence_score=0.97,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p2-05",
            date="2023-12-18",
            category="Consultation",
            title="Infectious Disease Reconciliation: Ciprofloxacin Halted",
            summary="ID specialist caught the dangerous concurrent antibiotic conflict. Stopped Ciprofloxacin immediately and reinforced Cephalexin targeted for MSSA.",
            details={"action": "Ciprofloxacin stopped", "continued": "Cephalexin 500mg QID"},
            clinician="Dr. Rebecca Moss, MD",
            facility="City General Infectious Disease",
            status="Warning",
            tags=["Med Reconciliation", "Patient Safety", "Infectious Disease"],
            provenance=SourceProvenance(
                document_id="doc-p2-05",
                document_name="2023-12-18_ID_Reconciliation.pdf",
                date="2023-12-18",
                page_number=1,
                verbatim_quote="STOP Ciprofloxacin immediately. CONTINUE and finish full 14-day course of Cephalexin 500mg QID.",
                confidence_score=0.98,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p2-06",
            date="2024-03-02",
            category="Laboratory",
            title="Infection Clearance Confirmed: WBC & CRP Normalized",
            summary="Post-treatment lab tests confirm complete recovery with WBC 6.2 k/uL and CRP 4.1 mg/L. Full joint function restored.",
            details={"wbc": 6.2, "crp": 4.1, "joint": "Effusion resolved"},
            clinician="City General Laboratory",
            facility="City General Hospital",
            status="Resolved",
            tags=["Infection Cure", "Inflammatory Normalization", "Recovery"],
            provenance=SourceProvenance(
                document_id="doc-p2-06",
                document_name="2024-03-02_Resolution_Lab.pdf",
                date="2024-03-02",
                page_number=1,
                verbatim_quote="WBC: 6.2 k/uL [Normal]... CRP: 4.1 mg/L [Normal]... Complete microbiological and clinical cure.",
                confidence_score=0.99,
                certainty_level="High"
            )
        )
    ]

    labs = [
        LabMetricSeries(
            test_name="C-Reactive Protein (CRP)",
            category="Hematology",
            unit="mg/L",
            normal_min=0.0,
            normal_max=8.0,
            trend_interpretation="Massive post-operative spike to 84.0 mg/L indicating acute surgical site infection, followed by total normalization to 4.1 mg/L post antibiotic therapy.",
            points=[
                LabDataPoint(
                    date="2023-11-10",
                    value=3.2,
                    unit="mg/L",
                    flag="Normal",
                    reference_range="< 8.0 mg/L",
                    doc_id="doc-p2-01",
                    provenance=SourceProvenance(
                        document_id="doc-p2-01",
                        document_name="2023-11-10_PreOp_Assessment.pdf",
                        date="2023-11-10",
                        page_number=1,
                        verbatim_quote="CRP: 3.2 mg/L [Normal]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2023-12-06",
                    value=84.0,
                    unit="mg/L",
                    flag="Critical",
                    reference_range="< 8.0 mg/L",
                    doc_id="doc-p2-03",
                    provenance=SourceProvenance(
                        document_id="doc-p2-03",
                        document_name="2023-12-06_ED_Infection.pdf",
                        date="2023-12-06",
                        page_number=1,
                        verbatim_quote="Serum CRP: 84.0 mg/L [H] (Severe inflammatory spike)",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2024-03-02",
                    value=4.1,
                    unit="mg/L",
                    flag="Normal",
                    reference_range="< 8.0 mg/L",
                    doc_id="doc-p2-06",
                    provenance=SourceProvenance(
                        document_id="doc-p2-06",
                        document_name="2024-03-02_Resolution_Lab.pdf",
                        date="2024-03-02",
                        page_number=1,
                        verbatim_quote="CRP: 4.1 mg/L [Normal]",
                        confidence_score=0.99
                    )
                )
            ]
        ),
        LabMetricSeries(
            test_name="White Blood Cell Count (WBC)",
            category="Hematology",
            unit="k/uL",
            normal_min=4.5,
            normal_max=11.0,
            trend_interpretation="Leukocytosis at 14.2 k/uL during acute MSSA joint infection, normalizing back to baseline (6.2 k/uL).",
            points=[
                LabDataPoint(
                    date="2023-11-10",
                    value=6.8,
                    unit="k/uL",
                    flag="Normal",
                    reference_range="4.5 - 11.0 k/uL",
                    doc_id="doc-p2-01",
                    provenance=SourceProvenance(
                        document_id="doc-p2-01",
                        document_name="2023-11-10_PreOp_Assessment.pdf",
                        date="2023-11-10",
                        page_number=1,
                        verbatim_quote="White Blood Cell Count (WBC): 6.8 k/uL [Normal]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2023-12-06",
                    value=14.2,
                    unit="k/uL",
                    flag="High",
                    reference_range="4.5 - 11.0 k/uL",
                    doc_id="doc-p2-03",
                    provenance=SourceProvenance(
                        document_id="doc-p2-03",
                        document_name="2023-12-06_ED_Infection.pdf",
                        date="2023-12-06",
                        page_number=1,
                        verbatim_quote="Serum WBC: 14.2 k/uL [H]",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2024-03-02",
                    value=6.2,
                    unit="k/uL",
                    flag="Normal",
                    reference_range="4.5 - 11.0 k/uL",
                    doc_id="doc-p2-06",
                    provenance=SourceProvenance(
                        document_id="doc-p2-06",
                        document_name="2024-03-02_Resolution_Lab.pdf",
                        date="2024-03-02",
                        page_number=1,
                        verbatim_quote="White Blood Cell Count (WBC): 6.2 k/uL [Normal]",
                        confidence_score=0.99
                    )
                )
            ]
        ),
        LabMetricSeries(
            test_name="Body Temperature",
            category="Cardiovascular",
            unit="deg C",
            normal_min=36.1,
            normal_max=37.2,
            trend_interpretation="Fever spike to 38.6 C (101.5 F) on presentation with post-op infection.",
            points=[
                LabDataPoint(
                    date="2023-11-10",
                    value=36.8,
                    unit="deg C",
                    flag="Normal",
                    reference_range="36.1 - 37.2 deg C",
                    doc_id="doc-p2-01",
                    provenance=SourceProvenance(
                        document_id="doc-p2-01",
                        document_name="2023-11-10_PreOp_Assessment.pdf",
                        date="2023-11-10",
                        page_number=1,
                        verbatim_quote="Patient afebrile at 36.8 C.",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2023-12-06",
                    value=38.6,
                    unit="deg C",
                    flag="High",
                    reference_range="36.1 - 37.2 deg C",
                    doc_id="doc-p2-03",
                    provenance=SourceProvenance(
                        document_id="doc-p2-03",
                        document_name="2023-12-06_ED_Infection.pdf",
                        date="2023-12-06",
                        page_number=1,
                        verbatim_quote="body temp 38.6 C (101.5 F)",
                        confidence_score=0.99
                    )
                ),
                LabDataPoint(
                    date="2024-03-02",
                    value=36.7,
                    unit="deg C",
                    flag="Normal",
                    reference_range="36.1 - 37.2 deg C",
                    doc_id="doc-p2-06",
                    provenance=SourceProvenance(
                        document_id="doc-p2-06",
                        document_name="2024-03-02_Resolution_Lab.pdf",
                        date="2024-03-02",
                        page_number=1,
                        verbatim_quote="Temp 36.7 C afebrile",
                        confidence_score=0.99
                    )
                )
            ]
        )
    ]

    meds = [
        MedicationRecord(
            id="med-p2-01",
            name="Cephalexin",
            dosage="500 mg",
            frequency="Four times daily (QID)",
            route="Oral",
            start_date="2023-12-06",
            end_date="2023-12-20",
            status="Discontinued",
            indication="MSSA Right Knee Surgical Site Infection",
            change_reason="Completed full 14-day therapeutic regimen with documented infection cure.",
            provenance=SourceProvenance(
                document_id="doc-p2-03",
                document_name="2023-12-06_ED_Infection.pdf",
                date="2023-12-06",
                page_number=1,
                verbatim_quote="Prescribed: Cephalexin 500 mg PO four times daily (QID) for 14 days.",
                confidence_score=0.99
            )
        ),
        MedicationRecord(
            id="med-p2-02",
            name="Ciprofloxacin",
            dosage="500 mg",
            frequency="Twice daily (BID)",
            route="Oral",
            start_date="2023-12-10",
            end_date="2023-12-18",
            status="Discontinued",
            indication="Wound infection (duplicate/redundant)",
            change_reason="Discontinued by Infectious Disease due to duplicate therapy conflict and suboptimal coverage for MSSA.",
            provenance=SourceProvenance(
                document_id="doc-p2-05",
                document_name="2023-12-18_ID_Reconciliation.pdf",
                date="2023-12-18",
                page_number=1,
                verbatim_quote="STOP Ciprofloxacin immediately. Patient was found taking BOTH Cephalexin and Ciprofloxacin.",
                confidence_score=0.98
            )
        )
    ]

    discrepancies = [
        DiscrepancyItem(
            id="disc-p2-01",
            type="Duplicate Therapy",
            severity="Critical",
            title="Dangerous Concurrent Antibiotic Duplication",
            description="Patient was concurrently taking two broad-spectrum antibiotics (Cephalexin 500mg QID + Ciprofloxacin 500mg BID) prescribed by different clinics 4 days apart without cross-facility medication reconciliation.",
            involved_documents=["2023-12-06_ED_Infection.pdf", "2023-12-10_Ortho_Ward.pdf", "2023-12-18_ID_Reconciliation.pdf"],
            evidence_quotes=[
                "Prescribed: Cephalexin 500 mg PO four times daily (QID)",
                "Prescribed: Ciprofloxacin 500 mg PO twice daily (BID) x 10 days",
                "Patient was found taking BOTH Cephalexin 500mg QID and Ciprofloxacin 500mg BID."
            ],
            clinical_recommendation="Implement real-time cross-facility health information exchange (HIE) to prevent uncoordinated antibiotic co-prescriptions."
        )
    ]

    relationships = [
        RelationshipLink(
            id="rel-p2-01",
            source_id="ev-p2-02",
            source_label="Procedure: Knee Meniscectomy (Nov 24, 2023)",
            target_id="ev-p2-03",
            target_label="Hospitalization: Surgical Site Infection (Dec 06, 2023)",
            relation_type="Complicated By",
            description="Patient developed acute MSSA infection in the operated knee 12 days following arthroscopy.",
            evidence_doc_id="doc-p2-03"
        ),
        RelationshipLink(
            id="rel-p2-02",
            source_id="ev-p2-03",
            source_label="Rx: Cephalexin Prescribed in ED",
            target_id="ev-p2-04",
            target_label="Rx: Ciprofloxacin Prescribed in Ortho",
            relation_type="Contradicts",
            description="Uncoordinated outpatient prescriptions generated a high-risk duplicate antibiotic conflict.",
            evidence_doc_id="doc-p2-04"
        ),
        RelationshipLink(
            id="rel-p2-03",
            source_id="ev-p2-04",
            source_label="Conflict: Duplicate Antibiotics",
            target_id="ev-p2-05",
            target_label="Consult: ID Medication Reconciliation",
            relation_type="Followed Up By",
            description="Infectious disease consultation resolved the dangerous interaction and verified targeted MSSA therapy.",
            evidence_doc_id="doc-p2-05"
        )
    ]

    return PatientProfile(
        id="p2",
        name="Marcus Chen",
        age=54,
        gender="Male",
        mrn="SJ-55210",
        blood_type="O+",
        summary="54-year-old male post-elective knee arthroscopy complicated by MSSA surgical site infection. Highlights acute EHR fragmentation leading to simultaneous duplicate antibiotic prescriptions (Cephalexin + Ciprofloxacin) caught and reconciled by Infectious Disease.",
        chronic_conditions=["Osteoarthritis Right Knee", "Post-Surgical Joint Infection (Resolved)"],
        allergies=["No Known Drug Allergies"],
        documents=docs,
        timeline=timeline,
        labs=labs,
        medications=meds,
        discrepancies=discrepancies,
        relationships=relationships
    )
