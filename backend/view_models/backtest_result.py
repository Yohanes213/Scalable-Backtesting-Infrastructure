from typing import List, Optional
from pydantic import BaseModel




class BackTestResult(BaseModel):
    final_portfolio_value : float
    total_trades : float
    winning_trades : float
    losing_trades : float
    max_drawdown : float
    max_moneydown : float
    sharpe_ratio : float

   

   

class Config:
    orm_mode = True


