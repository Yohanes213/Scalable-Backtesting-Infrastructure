import asyncio
import os
import sys
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import Null, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.models.indicator_parameter import IndicatorParameter
from backend.view_models.backtest_result import BackTestResult
from ..models.backtest_result_model import BacktestResult
from ..models.scene_model import Scene
from ..models.indicator_model import Indicator
from ..view_models.scenes_vm import IndicatorParams, ScenesBaseVM
# sys.path.append(os.path.abspath(os.path.join("../Scalable-Backtesting-Infrastructure/kafka_scripts")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from kafka_scripts.kafka_consumer import consume_backtest_results 
from kafka_scripts.kafka_producer import send_backend_request

# def backtest(db: Session, data: ScenesBaseVM) -> BackTestResult:
#     try:
            
#             if(data.params):
#                 dict = params_to_dict(data.params)
#             send_backend_request(
#                 data.coin_name, 
#                 data.start_date,
#                 data.end_date, 
#                 data.strategy_name,
#                 dict,
#                 data.start_cash, 
#                 data.commission
#                 )
            
#             metrics =  consume_backtest_results()
    
#             if(metrics):
#                 db_indicator = Indicator(
#                 indicator_name=data.strategy_name
#                 )
#                 # # Add Indicator to session
#                 db.add(db_indicator)
#                 db.flush()  # 
               
#                 print("db_indicator",db_indicator)
#                 # indicator = db.query(Indicator).filter(Indicator.indicator_name ==  data.strategy_name).first()
#                 if(db_indicator):
#                     indicatorId = db_indicator.indicator_id
#                     for param_data in data.params:
#                         db_param = IndicatorParameter(
#                             indicator_id=indicatorId,
#                             parameter_name =param_data.name, 
#                             parameter_value=param_data.value)
#                         db.add(db_param)
                
#                     db.flush()  # Ensure the indicator gets an ID before it's used in Scene
               
#                     print("db_indicator_param",)
                
#                     # # Create Scene record
#                     db_scene = Scene(
#                         coin_name = data.coin_name,
#                         start_cash=data.start_cash,
#                         commission=data.commission,
#                         start_date=data.start_date,
#                         end_date=data.end_date,
#                     )
                    

#                     # # Add Scene to session
#                     db.add(db_scene)
#                     db.flush()  # Ensure the scene gets an ID before it's used in BacktestResult
#                     print("db_scene",db_scene)
                    
                    
#                     db_backtest_result = BacktestResult(
#                             user_id = 1,
#                             indicator_id = db_indicator.indicator_id,
#                             # indicator_parameter = db_
#                             scene_id= db_scene.scene_id,
#                             final_portfolio_value = 0.0,
#                             total_trades  =  metrics['Number of trades'],
#                             winning_trades = 0.0,
#                             losing_trades = 0.0,
#                             max_drawdown =  metrics['Max drawdown'],
#                             max_moneydown = 0.0,
#                             sharpe_ratio = metrics['Sharpe ratio']
                            
#                         )
#                     # # Add BacktestResult to session
#                     db.add(db_backtest_result)
#                     db.commit()  # Commit all changes to the database
#                     print("db_backtest_result",db_backtest_result)
#                     return db_backtest_result
            
#             else:
#                 return Null 
#                 # return HTTPException(status_code=500, detail="Internal server error")

#     except SQLAlchemyError as e:
#         db.rollback()
#         print("Database error", e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred.")
#     except Exception as e :
#         print("ERROR", e)
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        


def backtest(db: Session, data: ScenesBaseVM) -> BacktestResult:
    try:
        params_dict = params_to_dict(data.params)
        send_request(data, params_dict)
        metrics = consume_backtest_results()

        if metrics:
            db_indicator = save_indicator(db, data.strategy_name)
            print("db_indicator",db_indicator)
            save_indicator_params(db, db_indicator.indicator_id, data.params)
            db_scene = save_scene(db, data)
            print("db_scene",db_scene)
            db_backtest_result = save_backtest_result(db, db_indicator, db_scene, metrics)
            print("db_backtest_result", db_backtest_result)
            return db_backtest_result
        else:
            raise HTTPException(status_code=500, detail="No metrics received from backtest")

    except SQLAlchemyError as e:
        print("Database error", e)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred.")
    except Exception as e:
        print("ERROR", e)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")




def send_request(data, params_dict):
    send_backend_request(
        data.coin_name, 
        data.start_date,
        data.end_date, 
        data.strategy_name,
        params_dict,
        data.start_cash, 
        data.commission
    )


def save_indicator(db, strategy_name):
    try:
        db_indicator = Indicator(
            indicator_name=strategy_name
        )
        db.add(db_indicator)
        db.flush()
        return db_indicator
    except Exception as e:
        db.rollback()
        print(f"An error occurred while saving the indicator: {e}")
        return None

def save_indicator_params(db, indicator_id, params):
    try:
        for param_data in params:
            db_param = IndicatorParameter(
                indicator_id=indicator_id,
                parameter_name=param_data.name, 
                parameter_value=param_data.value
            )
            db.add(db_param)
        db.flush()
    except Exception as e:
        db.rollback()
        print(f"An error occurred while saving the indicator parameters: {e}")

def save_scene(db, data):
    try:
        db_scene = Scene(
            coin_name=data.coin_name,
            start_cash=data.start_cash,
            commission=data.commission,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        db.add(db_scene)
        db.flush()
        return db_scene
    except Exception as e:
        db.rollback()
        print(f"An error occurred while saving the scene: {e}")
        return None

def save_backtest_result(db, db_indicator, db_scene, metrics):
    try:
        db_backtest_result = BacktestResult(
            user_id=1,
            indicator_id=db_indicator.indicator_id,
            scene_id=db_scene.scene_id,
            final_portfolio_value=0.0,
            total_trades=metrics['Number of trades'],
            winning_trades=0.0,
            losing_trades=0.0,
            max_drawdown=metrics['Max drawdown'],
            max_moneydown=0.0,
            sharpe_ratio=metrics['Sharpe ratio']
        )
        db.add(db_backtest_result)
        db.commit()
        return db_backtest_result
    except Exception as e:
        db.rollback()
        print(f"An error occurred while saving the backtest result: {e}")
        return None

def params_to_dict(params: List[IndicatorParams]) -> dict:
    return {param.name: param.value for param in params}


#     name = 'Bitcoin'    
#     strategy = 'macd'
#     start_date = '2023-06-24'
#     end_date ='2024-06-24'

#     params = {'fast_period':12, 'slow_period':26, 'signal_period':9, 'comm':0.0}
#     start_cash = 1000000
#     commission=0.001
 
            
    
#     send_backend_request(name, start_date, end_date, strategy, params, start_cash, commission)

#     metrics =  consume_backtest_results()
    
#     # print("METRICS--", metrics)
#     if(metrics):
#         print("METRICS--", metrics)
       
       
#         res = BackTestResult(
#             final_portfolio_value = 0.0,
#             total_trades  =  metrics['Number of trades'],
#             winning_trades = 0.0,
#             losing_trades = 0.0,
#             max_drawdown =  metrics['Max drawdown'],
#             max_moneydown = 0.0,
#             sharpe_ratio = metrics['Sharpe ratio']
            
#         )
#         return res
#     else:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str("Back test result not found"))

    



