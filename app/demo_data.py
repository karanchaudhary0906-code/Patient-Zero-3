from typing import Dict
from app.models import PatientProfile
from app.cases.p0 import get_p0
from app.cases.p1 import get_p1
from app.cases.p2 import get_p2
from app.cases.p3 import get_p3

def get_demo_patients() -> Dict[str, PatientProfile]:
    return {
        "p0": get_p0(),
        "p1": get_p1(),
        "p2": get_p2(),
        "p3": get_p3()
    }
