from pydantic import BaseModel, Field


class ArticleCreate(BaseModel):
    title: str
    conten: str
    user_id: int

    class Config:
        orm_mode = True