from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from crud import dss as crud_dss
from schemas import dss as schema_dss

router = APIRouter(
    prefix="/api/dss",
    tags=["DSS Algorithm"]
)

@router.get("/scenario-inputs", response_model=schema_dss.ScenarioInputResponse)
def get_scenario_inputs(db: Session = Depends(get_db)):
    data = crud_dss.get_dss_inputs(db)
    return {
        "scenario_name": "Kịch bản khởi tạo (Mặc định)",
        "total_classes": len(data),
        "data": data
    }