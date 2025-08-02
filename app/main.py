from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import timedelta
from app import models, schemas, database, auth, projects

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(root_path="/api")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])