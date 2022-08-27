from tokenize import String
from pydantic import BaseModel
from typing import Optional

class userSchema(BaseModel):
    id: Optional[str]
    name: str 
    username: str 
    user_password: str
    
    
class dataUser(BaseModel):
    username: str 
    user_password: str