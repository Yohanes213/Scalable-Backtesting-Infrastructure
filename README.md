**Crypto Trading Engineering: Scalable Backtesting Infrastructure**
===========================================================

**Overview**
--------

This project aims to design and build a reliable, large-scale trading data pipeline for a startup called Mela, which wants to make it simple for everyone to enter the world of cryptocurrencies. The pipeline will enable investors to run backtests that simulate current and past particular situations as well as their trend over time.

**Business Need**
-------------

The startup wants to provide a reliable source of investment while lowering the risk associated with trading cryptocurrencies. To achieve this, a robust data pipeline is needed to run various backtests and store useful artifacts in a robust data warehouse system.

**Data**
-----

The project will use candlestick data from Yahoo Finance and Binance. Candlestick data is a type of financial data that represents the price action of a security over time.

**Expected Outcomes**
------------------

* A robust data pipeline that can run various backtests
* Storage of useful artifacts in a robust data warehouse system
* Skills in technical analysis, backtesting, trading, and data engineering
* Knowledge of financial prediction, movement prediction, and enterprise-grade data engineering

## Installation
To get started with this project, clone the repository and install the required dependencies.

```bash
git clone https://github.com/group1Goldreich/Scalable-Backtesting-Infrastructure.git
cd Scalable-Backtesting-Infrastructure
pip install -r requirements.txt
```
Ensure you have the necessary environment setup, including Python 3.8+ and any other dependencies specified in the requirements.txt file.

## Usage

1. Build and run the Docker containers:
```bash
docker-compose build
docker-compose up -d
```

2. Execute the backtest:
```bash
python3 backtest/main.py
```

3. Start the backend:
Then run the backend
```bash
fastapi run backend/main.py
```

4. Launch the frontend:
Then The forntend
```bash
npm install
nvm start
```

**Contributors**
------

- [Yohanes Teshome Kebede](https://github.com/Yohanes213)
- [Eyerusalem Admassu](https://github.com/jadmassu)
- [Getachew Abebe](https://github.com/GetachewAbebe)
- [Mistir Nigusse](https://github.com/mistir-nigusse)
- [Abdelrhman Yasir](https://github.com/AB-y1)
