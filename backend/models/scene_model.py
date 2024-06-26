from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table,UniqueConstraint
from sqlalchemy.orm import relationship
from ..utils.database_connection import Base



class Scene(Base):
    __tablename__ = 'scenes'
    coin_name = Column(String)
    scene_id = Column(Integer, primary_key=True, index=True)
    start_cash = Column(Float)
    commission = Column(Float)
    start_date = Column(String)
    end_date = Column(String)
   
    users = relationship("User", secondary="scene_user", back_populates="scenes")
    backtests = relationship("BacktestResult", back_populates="scene")
    __table_args__ = (UniqueConstraint('scene_id', name='_scene_id_uc'),)

scene_user = Table(
    'scene_user', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('scene_id', Integer, ForeignKey('scenes.scene_id'), primary_key=True)
)