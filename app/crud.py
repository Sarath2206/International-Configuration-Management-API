from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .models import Configuration
from .schemas import ConfigurationCreate, ConfigurationUpdate

async def create_configuration(db: AsyncSession, config: ConfigurationCreate):
    db_config = Configuration(country_code=config.country_code, requirements=config.requirements)
    db.add(db_config)
    try:
        await db.commit()
        await db.refresh(db_config)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Configuration for this country already exists")
    return db_config

async def get_configuration(db: AsyncSession, country_code: str):
    result = await db.execute(select(Configuration).filter(Configuration.country_code == country_code))
    config = result.scalars().first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

async def update_configuration(db: AsyncSession, config: ConfigurationUpdate):
    result = await db.execute(select(Configuration).filter(Configuration.country_code == config.country_code))
    db_config = result.scalars().first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    db_config.requirements = config.requirements
    await db.commit()
    await db.refresh(db_config)
    return db_config

async def delete_configuration(db: AsyncSession, country_code: str):
    result = await db.execute(select(Configuration).filter(Configuration.country_code == country_code))
    db_config = result.scalars().first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    await db.delete(db_config)
    await db.commit()
    return {"detail": "Configuration deleted"}
