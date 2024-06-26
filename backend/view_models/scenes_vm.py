from typing import List, Optional
from pydantic import BaseModel




class IndicatorParams(BaseModel):
    name: str
    value: int

class ScenesBaseVM(BaseModel):
    coin_name: str
    strategy_name : str  
    start_date : str 
    end_date : str 
    params :List[IndicatorParams]
    start_cash : float
    commission : float
   


   
class ScenesCreateVM(ScenesBaseVM):
    pass

class ScenesVM(ScenesBaseVM):
    id: int
   

class Config:
    orm_mode = True


