from typing import ClassVar, Dict
from pyodmongo import DbEngine, DbModel, Id, Field

engine = DbEngine(mongo_uri="mongodb://root:root@localhost:27017", db_name='escape_room')

class User(DbModel):
    username: str = Field(index = True, unique = True, default="")
    password: str = ''
    inventory: Dict["Item| Id", int] = Field(default_factory=dict)
    location: 'Room | Id'
    _collection: ClassVar = "users"

class Room(DbModel):
    name:str = Field(index=True, unique=True)
    description:str
    inventory: Dict['Item', int] | None = Field(default_factory=dict)
    _collection: ClassVar = "rooms"

class Item(DbModel, unsafe_hash=True):
    name:str = Field(index=True, unique=True)
    bulky:bool = False
    _collection: ClassVar = "items"
