from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, engine, Base
from .schemas import ConfigurationCreate, ConfigurationUpdate, Configuration
from .crud import create_configuration, get_configuration, update_configuration, delete_configuration

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/create_configuration", response_model=Configuration)
async def create_config(config: ConfigurationCreate, db: AsyncSession = Depends(get_db)):
    return await create_configuration(db, config)

@app.get("/get_configuration/{country_code}", response_model=Configuration)
async def read_config(country_code: str, db: AsyncSession = Depends(get_db)):
    return await get_configuration(db, country_code)

@app.post("/update_configuration", response_model=Configuration)
async def update_config(config: ConfigurationUpdate, db: AsyncSession = Depends(get_db)):
    return await update_configuration(db, config)

@app.delete("/delete_configuration/{country_code}")
async def delete_config(country_code: str, db: AsyncSession = Depends(get_db)):
    return await delete_configuration(db, country_code)
