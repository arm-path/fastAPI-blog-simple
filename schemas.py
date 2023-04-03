from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List


class CategoryEnum(Enum):
    technologies = 'technologies'
    sociology = 'sociology'
    policy = 'policy'


class ArticleSchema(BaseModel):
    id: int
    category: CategoryEnum
    title: str = Field(max_length=31)
    raiting: int = Field(ge=0, le=5)
    description: Optional[str] = ""


class ResponseArticleListSchema(BaseModel):
    status: int
    data: List[ArticleSchema]


class ResponseArticleDetail(BaseModel):
    status: int
    data: ArticleSchema
