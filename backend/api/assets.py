from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from backend.core.database import get_db, neo4j_driver
from backend.models.asset import Asset

router = APIRouter(prefix="/assets", tags=["Assets"])

class AssetCreate(BaseModel):
    asset_id: str
    type: str
    location: str

class AssetResponse(AssetCreate):
    health_score: float
    status: str

    class Config:
        orm_mode = True

@router.post("/", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = Asset(asset_id=asset.asset_id, type=asset.type, location=asset.location)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    
    # Sync with Neo4j Knowledge Graph
    if neo4j_driver:
        with neo4j_driver.session() as session:
            session.run("MERGE (a:Asset {asset_id: $id, type: $type, location: $loc})",
                        id=asset.asset_id, type=asset.type, loc=asset.location)
    
    return db_asset

@router.get("/", response_model=List[AssetResponse])
def get_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    assets = db.query(Asset).offset(skip).limit(limit).all()
    return assets
