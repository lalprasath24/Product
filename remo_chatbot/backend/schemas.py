# schemas.py
from pydantic import BaseModel
from enum import Enum

class DBType(str, Enum):
    postgres = "postgres"
    mysql = "mysql"

# Model for the database configuration
class DBConfig(BaseModel):
    db_type: DBType  # <-- NEW FIELD
    host: str
    port: int
    user: str
    password: str
    dbname: str

class Item(BaseModel):  
    name:str
    age:int

class ChatRequest(BaseModel):
    question: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How many users are in the database?"
            }
        }


class AppState:
    db_config: DBConfig = None

app_state = AppState()