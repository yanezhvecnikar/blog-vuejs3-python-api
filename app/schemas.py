from pydantic import BaseModel, HttpUrl

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ProjectCreate(BaseModel):
    title: str
    description: str
    github_url: HttpUrl
    image_url: HttpUrl

class ProjectOut(ProjectCreate):
    id: int

    class Config:
        from_attributes = True