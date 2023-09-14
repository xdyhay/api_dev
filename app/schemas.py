from typing import Optional
from pydantic import BaseModel, EmailStr, Field, conint
from datetime import datetime
from uuid import UUID, uuid4

class UserBaseModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    email: EmailStr
    password: str

class UserCreateModel(UserBaseModel):
    pass

class UserOut(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True



class PostBaseModel(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateModel(PostBaseModel):
    pass
    
class PostUpdateModel(PostBaseModel):
    pass

class PostOut(PostBaseModel):
    id: int
    created_at: datetime
    user_uuid: UUID = Field(default_factory=uuid4)
    user: UserOut

    class Config:
        from_attributes = True



class LikeBaseModel(BaseModel):
    post_id: int

class LikeCreateModel(LikeBaseModel):
    """
    Like direction: dir 1 is like, 0 is unlike
    ge: The value must be greater than or equal to this.
    le: The value must be less than or equal to this.
    """
    dir: conint(ge=0, le=1)

class PostLikeOut(BaseModel):
    post: PostOut
    likes: int

    class Config:
        from_attributes = True



# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uuid: UUID = None



class QueryParams():
    def __init__(self, limit: int = None, skip: int = 0, search: str = None):
        self.limit = limit
        self.skip = skip
        self.search = search