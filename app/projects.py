from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import database, schemas, models
from app.auth import get_current_user
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=schemas.ProjectOut)
def add_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_project(db, project)

@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)
