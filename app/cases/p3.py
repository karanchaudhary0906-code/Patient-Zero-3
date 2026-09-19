from app.models import (
    PatientProfile, MedicalDocument, TimelineEvent,
    LabMetricSeries, LabDataPoint, MedicationRecord,
    DiscrepancyItem, RelationshipLink, SourceProvenance
)

def get_p3() -> PatientProfile:
    docs = [
        MedicalDocument(
            id="doc-p3-01",
            title="Trauma Center Inpatient Summary & CT Scan",
            doc_type="Discharge Summary",
            date="2023-01-15",
            author="Dr. David Vance, MD",
            facility="Mercy Regional Trauma Center",
            file_name="2023-01-15_Trauma_Discharge.pdf",
            raw_text="MERCY REGIONAL TRAUMA CENTER - DISCHARGE SUMMARY\nDate of Admission: Jan 14, 2023 | Date of Discharge: Jan 15, 2023\nPatient: Sarah Jenkins | Age: 42 | MRN: MR-77140\n\nREASON FOR ADMISSION: Motor vehicle collision (restrained driver).\nALLERGY ALERT: PENICILLIN - SEVERE ANAPHYLAXIS (Laryngeal edema, ICU admission 2018).\n\nCHEST/ABDOMEN CT FINDINGS:\n1. No intra-abdominal injury or traumatic aortic disruption.\n2. INCIDENTAL FINDING: Well-circumscribed non-calcified 6mm solitary pulmonary nodule in right lower lobe (Lung-RADS Category 3).\nRECOMMENDATION: Repeat low-dose CT chest in 6 months to assess stability and rule out malignancy."
        ),
        MedicalDocument(
            id="doc-p3-02",
            title="Urgent Care Clinic Note - Acute Bacterial Sinusitis",
            doc_type="Clinical Note",
            date="2023-07-22",
            author="Dr. Thomas Reed, MD",
            facility="Express Care Clinic West",
            file_name="2023-07-22_ExpressCare_Reed.pdf",
            raw_text="EXPRESS CARE CLINIC WEST - ENCOUNTER NOTE\nDate: July 22, 2023\nPatient: Sarah Jenkins\n\nCHIEF COMPLAINT: Severe facial pressure, purulent nasal discharge, and dental aching for 10 days.\nASSESSMENT: Acute bacterial rhinosinusitis.\nALLERGY RECORD IN SYSTEM: 'No Known Allergies' (Default unverified field).\nTREATMENT PLAN:\n- Prescribed: Amoxicillin-Clavulanate (Augmentin) 875/125 mg PO twice daily x 7 days.\n- Decongestant nasal spray."
        ),
        MedicalDocument(
            id="doc-p3-03",
            title="Pulmonology Consultation - Incidental Nodule Review",
            doc_type="Clinical Note",
            date="2024-02-14",
            author="Dr. Helena Croft, MD",
            facility="Mercy Specialty Clinic",
            file_name="2024-02-14_Pulmonology_Croft.pdf",
            raw_text="MERCY SPECIALTY CLINIC - PULMONARY EVALUATION\nDate: February 14, 2024\nPatient: Sarah Jenkins\n\nREASON FOR CONSULTATION: Persistent mild dry cough and shortness of breath upon exertion.\nRETROSPECTIVE RECORD REVIEW:\nUpon reviewing trauma records from January 2023, clinician noted a 6mm right lower lobe pulmonary nodule explicitly flagged for 6-month CT follow-up.\nCRITICAL CARE GAP IDENTIFIED:\nThe recommended 6-month repeat CT chest (due July 2023) was NEVER performed. Patient was lost to follow-up on this finding for over 13 months.\nPLAN:\n- Stat Low-Dose CT Chest with IV contrast to evaluate nodule morphology and growth.\n- Documented severe Penicillin anaphylaxis verified with patient."
        )
    ]

    timeline = [
        TimelineEvent(
            id="ev-p3-01",
            date="2023-01-15",
            category="Imaging",
            title="CT Scan: Incidental 6mm Lung Nodule & Severe Penicillin Allergy",
            summary="Trauma CT identified an incidental 6mm right lower lobe pulmonary nodule (Lung-RADS 3) with mandatory 6-month follow-up. Documented severe Penicillin anaphylaxis.",
            details={"nodule": "6mm RLL", "lung_rads": 3, "allergy": "Penicillin (Anaphylaxis)", "recommendation": "Repeat CT in 6 months"},
            clinician="Dr. David Vance, MD",
            facility="Mercy Regional Trauma Center",
            status="Warning",
            tags=["CT Scan", "Incidental Finding", "Severe Allergy"],
            provenance=SourceProvenance(
                document_id="doc-p3-01",
                document_name="2023-01-15_Trauma_Discharge.pdf",
                date="2023-01-15",
                page_number=1,
                verbatim_quote="INCIDENTAL FINDING: Well-circumscribed non-calcified 6mm solitary pulmonary nodule... Recommend repeat low-dose CT chest in 6 months... ALLERGY ALERT: PENICILLIN - SEVERE ANAPHYLAXIS.",
                confidence_score=0.99,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p3-02",
            date="2023-07-22",
            category="Prescription",
            title="Dangerous Allergy Omission: Amoxicillin Prescribed",
            summary="Urgent Care clinic failed to pull trauma allergy records, defaulting to 'No Known Allergies', and prescribed Amoxicillin-Clavulanate for acute sinusitis.",
            details={"rx": "Amoxicillin-Clavulanate 875/125mg", "recorded_allergy": "NKDA (Incorrect)", "real_allergy": "Penicillin anaphylaxis"},
            clinician="Dr. Thomas Reed, MD",
            facility="Express Care Clinic West",
            status="Critical",
            tags=["Allergy Breach", "Near Miss", "Contraindicated Rx"],
            provenance=SourceProvenance(
                document_id="doc-p3-02",
                document_name="2023-07-22_ExpressCare_Reed.pdf",
                date="2023-07-22",
                page_number=1,
                verbatim_quote="Prescribed: Amoxicillin-Clavulanate 875/125 mg PO twice daily... ALLERGY RECORD: 'No Known Allergies'.",
                confidence_score=0.97,
                certainty_level="High"
            )
        ),
        TimelineEvent(
            id="ev-p3-03",
            date="2024-02-14",
            category="Consultation",
            title="Pulmonology Consult: 7-Month Overdue Incidental Nodule Flagged",
            summary="Pulmonologist discovered the Jan 2023 6mm nodule had never been restudied at 6 months (now 7 months overdue). Ordered immediate stat low-dose chest CT.",
            details={"gap": "7 months overdue for 6mm nodule follow-up", "action": "Stat low-dose chest CT ordered"},
            clinician="Dr. Helena Croft, MD",
            facility="Mercy Specialty Clinic",
            status="Critical",
            tags=["Care Gap", "Delayed Oncology Screening", "Overdue CT"],
            provenance=SourceProvenance(
                document_id="doc-p3-03",
                document_name="2024-02-14_Pulmonology_Croft.pdf",
                date="2024-02-14",
                page_number=1,
                verbatim_quote="The recommended 6-month repeat CT chest (due July 2023) was NEVER performed. Patient was lost to follow-up on this finding for over 13 months.",
                confidence_score=0.98,
                certainty_level="High"
            )
        )
    ]

    labs = [
        LabMetricSeries(
            test_name="Pulmonary Nodule Size",
            category="Imaging",
            unit="mm",
            normal_min=0.0,
            normal_max=4.0,
            trend_interpretation="Initial 6mm nodule detected Jan 2023. Overdue for surveillance.",
            points=[
                LabDataPoint(
                    date="2023-01-15",
                    value=6.0,
                    unit="mm",
                    flag="High",
                    reference_range="< 4.0 mm",
                    doc_id="doc-p3-01",
                    provenance=SourceProvenance(
                        document_id="doc-p3-01",
                        document_name="2023-01-15_Trauma_Discharge.pdf",
                        date="2023-01-15",
                        page_number=1,
                        verbatim_quote="6mm solitary pulmonary nodule in right lower lobe",
                        confidence_score=0.99
                    )
                )
            ]
        )
    ]

    meds = [
        MedicationRecord(
            id="med-p3-01",
            name="Amoxicillin-Clavulanate",
            dosage="875/125 mg",
            frequency="Twice daily",
            route="Oral",
            start_date="2023-07-22",
            end_date="2023-07-22",
            status="Discontinued",
            indication="Acute sinusitis (Contraindicated by anaphylaxis)",
            change_reason="Prescribed in error due to missing allergy synchronization across clinic systems.",
            provenance=SourceProvenance(
                document_id="doc-p3-02",
                document_name="2023-07-22_ExpressCare_Reed.pdf",
                date="2023-07-22",
                page_number=1,
                verbatim_quote="Prescribed: Amoxicillin-Clavulanate 875/125 mg PO twice daily",
                confidence_score=0.97
            )
        )
    ]

    discrepancies = [
        DiscrepancyItem(
            id="disc-p3-01",
            type="Allergy Warning",
            severity="Critical",
            title="Near-Fatal Allergy Information Omission",
            description="Severe Penicillin anaphylaxis with prior ICU admission was documented in Hospital Summary (Doc 1) but appeared as 'No Known Allergies' in Urgent Care Clinic (Doc 2), resulting in contraindicated Amoxicillin prescription.",
            involved_documents=["2023-01-15_Trauma_Discharge.pdf", "2023-07-22_ExpressCare_Reed.pdf"],
            evidence_quotes=[
                "ALLERGY ALERT: PENICILLIN - SEVERE ANAPHYLAXIS (Laryngeal edema, ICU admission 2018).",
                "ALLERGY RECORD IN SYSTEM: 'No Known Allergies' (Default unverified field)."
            ],
            clinical_recommendation="Immediately reconcile enterprise allergy master records and implement hard-stop contraindication warnings."
        ),
        DiscrepancyItem(
            id="disc-p3-02",
            type="Missing Follow-up",
            severity="Critical",
            title="Overdue Incidental Pulmonary Nodule CT Screening",
            description="A 6mm pulmonary nodule with Lung-RADS 3 classification required follow-up imaging in July 2023 (6 months). Was missed entirely until February 2024 (13 months later, 7 months overdue).",
            involved_documents=["2023-01-15_Trauma_Discharge.pdf", "2024-02-14_Pulmonology_Croft.pdf"],
            evidence_quotes=[
                "RECOMMENDATION: Repeat low-dose CT chest in 6 months to assess stability and rule out malignancy.",
                "The recommended 6-month repeat CT chest (due July 2023) was NEVER performed."
            ],
            clinical_recommendation="Urgent completion of low-dose chest CT and pulmonary oncology review to assess nodule volume doubling time."
        )
    ]

    relationships = [
        RelationshipLink(
            id="rel-p3-01",
            source_id="ev-p3-01",
            source_label="Allergy: Penicillin Anaphylaxis Documented",
            target_id="ev-p3-02",
            target_label="Rx: Amoxicillin Prescribed in Urgent Care",
            relation_type="Contradicts",
            description="Dangerous failure of allergy communication between hospital and urgent care systems.",
            evidence_doc_id="doc-p3-02"
        ),
        RelationshipLink(
            id="rel-p3-02",
            source_id="ev-p3-01",
            source_label="Imaging: 6mm Nodule 6-Month CT Recommendation",
            target_id="ev-p3-03",
            target_label="Consult: Pulmonologist Flags 7-Month Overdue Care Gap",
            relation_type="Followed Up By",
            description="Incidental finding lost in clinical transition until retrieved 13 months later.",
            evidence_doc_id="doc-p3-03"
        )
    ]

    return PatientProfile(
        id="p3",
        name="Sarah Jenkins",
        age=42,
        gender="Female",
        mrn="MR-77140",
        blood_type="B-",
        summary="42-year-old female victim of motor vehicle collision whose incidental findings and life-threatening allergies were dropped during health system handoffs. Highlights both a near-fatal Penicillin prescription and a 7-month overdue lung nodule cancer screening.",
        chronic_conditions=["Solitary Pulmonary Nodule (Surveillance Overdue)", "History of Trauma/MVC"],
        allergies=["Penicillin (Severe Anaphylaxis)"],
        documents=docs,
        timeline=timeline,
        labs=labs,
        medications=meds,
        discrepancies=discrepancies,
        relationships=relationships
    )
