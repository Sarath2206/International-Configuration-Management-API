from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

async def handle_db_exceptions(exc: Exception):
    if isinstance(exc, IntegrityError):
        raise HTTPException(status_code=400, detail="Database integrity error")
    raise HTTPException(status_code=500, detail="Internal server error")
