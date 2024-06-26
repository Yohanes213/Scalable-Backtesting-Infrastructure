
from sqlalchemy import Column, Integer,  ForeignKey, Float
from sqlalchemy.orm import relationship
from ..utils.database_connection import Base



class BacktestResult(Base):
    __tablename__ = 'backtest_results'
    
    backtest_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    scene_id = Column(Integer, ForeignKey('scenes.scene_id'))
    final_portfolio_value = Column(Float)
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    max_drawdown = Column(Float)
    max_moneydown = Column(Float)
    sharpe_ratio = Column(Float)

    user = relationship("User")
    # indicator = relationship("Indicator", back_populates="backtest_results")
    indicator_parameters = relationship("IndicatorParameter", back_populates="backtest_results")
    
    scene = relationship("Scene", back_populates="backtests")
    
    
    