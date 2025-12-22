from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.database import db
from app.models import Table

router = APIRouter(prefix="/api/tables", tags=["Tables"])


@router.get("/qr/{qr_code}", response_model=Table)
async def get_table_by_qr(qr_code: str):
    """Получить информацию о столике по QR-коду."""
    table = db.get_table_by_qr(qr_code)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router.get("/{table_id}", response_model=Table)
async def get_table(table_id: UUID):
    """Получить столик по ID."""
    table = db.get_table(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table
