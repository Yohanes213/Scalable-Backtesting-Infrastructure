import asyncio
import os
import sys
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import Null, alias, select
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

def backtest(db: Session, data: ScenesBaseVM) -> BacktestResult:
    try:
        params_dict = params_to_dict(data.params)
        existing_result = check_existing_result(db, data, params_dict)
        print("-----",existing_result)
        if existing_result:
            return existing_result
        
        send_request(data, params_dict)
        metrics = consume_backtest_results()

        if metrics:
            db_scene = save_scene(db, data)
            print("db_scene",db_scene)
            db_backtest_result = save_backtest_result(db,  db_scene, metrics)
            print("db_backtest_result", db_backtest_result)
            db_indicator = save_indicator(db, data.strategy_name)
            print("db_indicator",db_indicator)
            save_indicator_params(db, db_indicator.indicator_id,db_backtest_result, data.params)
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

def save_indicator_params(db, indicator_id,db_backtest_result, params):
    try:
        for param_data in params:
            db_param = IndicatorParameter(
                backtest_results_id =db_backtest_result.backtest_id,
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

def save_backtest_result(db,  db_scene, metrics):
    try:
        db_backtest_result = BacktestResult(
            user_id=1,
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


    
def check_existing_result(db, data, params_dict,):
    query = (
     db.query(BacktestResult)
    .join(BacktestResult.scene)
    .filter(
        Scene.coin_name == data.coin_name,
        Scene.start_cash == data.start_cash,
        Scene.start_date == data.start_date,
        Scene.commission == data.commission,
        Scene.end_date == data.end_date,
        Indicator.indicator_name == data.strategy_name
        # IndicatorParameter.parameter_name == parameter_name_filter,
        # IndicatorParameter.parameter_value == parameter_value_filter
        )
    )
    results = query.first()
    print(results)
    return results

