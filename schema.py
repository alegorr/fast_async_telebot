from pydantic import BaseModel

class UserSchema(BaseModel):
    is_bot: bool
    username: str
    service_id: int

    class Config:
        orm_mode = True

class ServiceSchema(BaseModel):
    name: str
    url: str

    class Config:
        orm_mode = True

class TransactionSchema(BaseModel):
    user_id: int
    service_id: int
    input: str
    output: str
    complete: bool
    error: str

    class Config:
        orm_mode = True
