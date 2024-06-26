from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from ..utils.database_connection import Base




class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
   
    

    scenes = relationship("Scene", secondary="scene_user", back_populates="users")
