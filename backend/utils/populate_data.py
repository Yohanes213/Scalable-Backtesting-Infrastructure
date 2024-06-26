from typing import List, Type, Dict
from sqlalchemy.orm import Session
from .database_connection import Base
import json

def populate_initial_data(db: Session, model_cls: Type[Base], initial_data: List[Dict]):
    for data_entry in initial_data:
        db_entry = model_cls(**data_entry)
        print("------db",db_entry)
        
        print("------db",db)
        db.add(db_entry)
    db.commit()



def load_initial_data_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data