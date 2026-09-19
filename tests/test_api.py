import sys
import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestPatientZeroAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_list_patients(self):
        res = self.client.get("/api/patients")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("patients", data)
        self.assertEqual(len(data["patients"]), 4)
        ids = [p["id"] for p in data["patients"]]
        self.assertIn("p0", ids)
        self.assertIn("p1", ids)
        self.assertIn("p2", ids)
        self.assertIn("p3", ids)

    def test_02_get_p0_rahul_sharma(self):
        res = self.client.get("/api/patients/p0")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["name"], "Rahul Sharma")
        self.assertEqual(len(data["documents"]), 6)
        self.assertEqual(len(data["timeline"]), 6)
        self.assertGreaterEqual(len(data["labs"]), 1)
        self.assertGreaterEqual(len(data["medications"]), 1)

        # Check provenance format on first event
        ev1 = data["timeline"][0]
        self.assertIn("provenance", ev1)
        self.assertIn("blood_report_jan.pdf", ev1["provenance"]["document_name"])
        self.assertIn("11.8", ev1["provenance"]["verbatim_quote"])
        self.assertGreaterEqual(ev1["provenance"]["confidence_score"], 0.9)

    def test_03_killer_feature_what_changed(self):
        res = self.client.get("/api/patients/p0/what-changed")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["patient_name"], "Rahul Sharma")
        self.assertIn("blood_tests", data)
        self.assertIn("medications", data)
        self.assertIn("missing_information", data)
        self.assertIn("repeated_tests", data)

        # Hemoglobin change check
        hb_changes = [t for t in data["blood_tests"] if "Hemoglobin" in t["test_name"]]
        self.assertTrue(len(hb_changes) > 0)
        self.assertIn("11.8", hb_changes[0]["initial"])
        self.assertIn("14.1", hb_changes[0]["latest"])

    def test_04_get_p2_and_p3_discrepancies(self):
        # Case 2: Marcus Chen (Duplicate Antibiotics)
        res2 = self.client.get("/api/patients/p2")
        self.assertEqual(res2.status_code, 200)
        p2_data = res2.json()
        disc_types_p2 = [d["type"] for d in p2_data["discrepancies"]]
        self.assertIn("Duplicate Therapy", disc_types_p2)

        # Case 3: Sarah Jenkins (Allergy & Missing CT)
        res3 = self.client.get("/api/patients/p3")
        self.assertEqual(res3.status_code, 200)
        p3_data = res3.json()
        disc_types_p3 = [d["type"] for d in p3_data["discrepancies"]]
        self.assertIn("Allergy Warning", disc_types_p3)
        self.assertIn("Missing Follow-up", disc_types_p3)

    def test_05_document_upload_and_extraction(self):
        sample_note = """APOLLO CLINIC FOLLOW-UP
Date: 2026-09-10
Patient: Rahul Sharma
ASSESSMENT: Patient reports excellent exercise tolerance.
RESULTS:
Hemoglobin: 14.3 g/dL
BP: 120/80 mmHg
PLAN:
Maintain healthy dietary iron intake. Follow up annually."""

        res = self.client.post(
            "/api/patients/p0/upload",
            data={
                "raw_text": sample_note,
                "doc_title": "Annual_Followup_Sept_2026"
            }
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(len(data["extracted_events"]), 1)

    def test_06_system_stats(self):
        res = self.client.get("/api/stats")
        self.assertEqual(res.status_code, 200)
        stats = res.json()
        self.assertGreaterEqual(stats["total_patients"], 4)
        self.assertGreaterEqual(stats["total_documents_indexed"], 18)
        self.assertIn("compliance", stats)

    def test_07_create_new_patient_and_incremental_timeline(self):
        # 1. Create a brand new real patient
        payload = {
            "name": "Jane Doe",
            "age": 38,
            "gender": "Female",
            "blood_type": "B+",
            "chronic_conditions": ["Iron Deficiency Anemia"],
            "allergies": ["Sulfa"],
            "summary": "38-year-old female tracking hemoglobin improvement."
        }
        create_res = self.client.post("/api/patients", json=payload)
        self.assertEqual(create_res.status_code, 200)
        patient_data = create_res.json()["patient"]
        patient_id = patient_data["id"]
        self.assertEqual(patient_data["name"], "Jane Doe")
        self.assertEqual(len(patient_data["timeline"]), 0)

        # 2. Upload first blood test
        up1 = self.client.post(
            f"/api/patients/{patient_id}/upload",
            data={
                "raw_text": "Date: 2026-02-01\nHemoglobin: 10.4 g/dL\nFerritin: 8.0 ng/mL\nImpression: Microcytic Anemia",
                "doc_title": "Initial_CBC_Lab"
            }
        )
        self.assertEqual(up1.status_code, 200)

        # 3. Upload prescription
        up2 = self.client.post(
            f"/api/patients/{patient_id}/upload",
            data={
                "raw_text": "Date: 2026-02-05\nRx Initiate Ferrous Ascorbate 100mg daily for 60 days.",
                "doc_title": "Oral_Iron_Prescription"
            }
        )
        self.assertEqual(up2.status_code, 200)

        # 4. Upload follow-up CBC
        up3 = self.client.post(
            f"/api/patients/{patient_id}/upload",
            data={
                "raw_text": "Date: 2026-04-15\nHemoglobin: 12.8 g/dL\nFerritin: 22.0 ng/mL\nImpression: Resolved Anemia",
                "doc_title": "Followup_CBC_Lab"
            }
        )
        self.assertEqual(up3.status_code, 200)

        # 5. Verify timeline and What Changed synthesis
        prof_res = self.client.get(f"/api/patients/{patient_id}")
        self.assertEqual(prof_res.status_code, 200)
        profile = prof_res.json()
        self.assertEqual(len(profile["documents"]), 3)
        self.assertGreaterEqual(len(profile["timeline"]), 3)
        self.assertGreaterEqual(len(profile["medications"]), 1)

        wc_res = self.client.get(f"/api/patients/{patient_id}/what-changed")
        self.assertEqual(wc_res.status_code, 200)
        wc = wc_res.json()
        self.assertGreaterEqual(len(wc["blood_tests"]), 1)
        hb_change = next(t for t in wc["blood_tests"] if "Hemoglobin" in t["test_name"])
        self.assertIn("10.4", hb_change["initial"])
        self.assertIn("12.8", hb_change["latest"])
        self.assertIn("+2.4", hb_change["delta"])

    def test_08_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["frontend"], "integrated")

    def test_09_frontend_root_and_spa(self):
        # Verify root index.html is served
        res_root = self.client.get("/")
        self.assertEqual(res_root.status_code, 200)
        self.assertIn("text/html", res_root.headers.get("content-type", ""))
        self.assertIn("Patient Zero", res_root.text)

        # Verify SPA fallback on client-side paths
        res_spa = self.client.get("/dashboard")
        self.assertEqual(res_spa.status_code, 200)
        self.assertIn("text/html", res_spa.headers.get("content-type", ""))
        self.assertIn("Patient Zero", res_spa.text)

if __name__ == "__main__":
    unittest.main()

