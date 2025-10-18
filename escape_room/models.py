from os import stat, environ
from typing import ClassVar, Dict
from pyodmongo import DbEngine, DbModel, Id, Field

db_user = environ.get("DB_USER", 'admin')
db_pass = environ.get("DB_PASS", 'admin')
db_address = environ.get("DB_ADDRESS", 'localhost')
db_port = environ.get("DB_PORT", "27017")
")
engine = DbEngine(mongo_uri=f"mongodb://{db_user}:{db_pass}@{db_address}:{db_port}", db_name='escape_room')

class User(DbModel):
    username: str = Field(index = True, unique = True, default="")
    password: str = ''
    inventory: Dict["Item| Id", int] = Field(default_factory=dict)
    location: 'Room | Id'
    _collection: ClassVar = "users"

    @staticmethod
    def get_user_by_id(id:str):
        pass

class Room(DbModel):
    name:str = Field(index=True, unique=True)
    description:str
    inventory: Dict['Item', int] | None = Field(default_factory=dict)
    _collection: ClassVar = "rooms"

class Item(DbModel, unsafe_hash=True):
    name:str = Field(index=True, unique=True)
    bulky:bool = False
    _collection: ClassVar = "items"
