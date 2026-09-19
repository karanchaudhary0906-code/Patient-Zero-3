from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SourceProvenance(BaseModel):
    document_id: str
    document_name: str
    date: str
    page_number: int = 1
    verbatim_quote: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    certainty_level: str = "High"  # High, Moderate, Uncertain
    uncertainty_rationale: Optional[str] = None

class TimelineEvent(BaseModel):
    id: str
    date: str
    category: str  # Consultation, Prescription, Laboratory, Imaging, Hospitalization, Procedure
    title: str
    summary: str
    details: Dict[str, Any] = {}
    clinician: Optional[str] = None
    facility: Optional[str] = None
    status: str = "Normal"  # Normal, Abnormal, Warning, Critical, Resolved
    tags: List[str] = []
    provenance: SourceProvenance

class LabDataPoint(BaseModel):
    date: str
    value: float
    unit: str
    flag: str = "Normal"  # Normal, High, Low, Critical
    reference_range: str
    doc_id: str
    provenance: SourceProvenance

class LabMetricSeries(BaseModel):
    test_name: str
    category: str  # Glycemic, Renal, Lipid, Hematology, Cardiovascular
    unit: str
    normal_min: float
    normal_max: float
    points: List[LabDataPoint]
    trend_interpretation: str

class MedicationRecord(BaseModel):
    id: str
    name: str
    dosage: str
    frequency: str
    route: str = "Oral"
    start_date: str
    end_date: Optional[str] = None
    status: str = "Active"  # Active, Discontinued, Adjusted, Tapered
    indication: str
    change_reason: Optional[str] = None
    provenance: SourceProvenance

class DiscrepancyItem(BaseModel):
    id: str
    type: str  # Dosage Conflict, Allergy Warning, Missing Follow-up, Contradictory Note, Duplicate Therapy
    severity: str  # Critical, Warning, Informational
    title: str
    description: str
    involved_documents: List[str]
    evidence_quotes: List[str]
    clinical_recommendation: str

class RelationshipLink(BaseModel):
    id: str
    source_id: str
    source_label: str
    target_id: str
    target_label: str
    relation_type: str  # Triggered By, Treated With, Followed Up By, Contradicts, Adverse Reaction To
    description: str
    evidence_doc_id: str

class MedicalDocument(BaseModel):
    id: str
    title: str
    doc_type: str  # Prescription, Lab Report, Discharge Summary, Clinical Note, Imaging Scan
    date: str
    author: str
    facility: str
    file_name: str
    raw_text: str
    file_url: Optional[str] = None
    is_image: bool = False

class PatientProfile(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    mrn: str
    blood_type: str
    summary: str
    chronic_conditions: List[str]
    allergies: List[str]
    documents: List[MedicalDocument]
    timeline: List[TimelineEvent]
    labs: List[LabMetricSeries]
    medications: List[MedicationRecord]
    discrepancies: List[DiscrepancyItem]
    relationships: List[RelationshipLink]

class QueryRequest(BaseModel):
    patient_id: str
    query: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[SourceProvenance]
    related_events: List[str]

class CreatePatientRequest(BaseModel):
    name: str
    age: int = 35
    gender: str = "Unspecified"
    mrn: Optional[str] = None
    blood_type: str = "Unknown"
    summary: Optional[str] = None
    chronic_conditions: List[str] = []
    allergies: List[str] = []
