from pydantic import BaseModel, Field


class ArticleCreate(BaseModel):
    title: str
    conten: str

    class Config:
        orm_mode = True
