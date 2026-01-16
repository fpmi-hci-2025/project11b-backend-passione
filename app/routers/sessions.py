from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.database import db
from app.models import Session, SessionCreate

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


@router.post("", response_model=Session, status_code=201)
async def create_session(session_data: SessionCreate):
    """Создать сессию посетителя при сканировании QR-кода."""
    session = db.create_session(
        table_id=session_data.table_id,
        device_id=session_data.device_id,
        language=session_data.language
    )
    if not session:
        raise HTTPException(status_code=404, detail="Table not found")
    return session


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: UUID):
    """Получить сессию по ID."""
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
