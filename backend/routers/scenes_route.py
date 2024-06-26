from fastapi import APIRouter, Depends,  HTTPException,  status

from ..view_models.backtest_result import BackTestResult
from ..utils.database_connection import get_db as session
from ..controllers  import backtest_controller
from sqlalchemy.ext.asyncio import AsyncSession

from ..view_models.scenes_vm import ScenesBaseVM


router = APIRouter(
    prefix="/scenes",
    tags=["scenes"],
    responses={404: {"description": "Not found"}},
)


    
@router.post("/backtest",response_model=BackTestResult)
async def create_data(data: ScenesBaseVM, db: AsyncSession =  Depends(session)):
    try:
               
        backtest_result =  backtest_controller.backtest(db, data=data)
        return backtest_result
    except Exception as e:
        print("ERRPR", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
