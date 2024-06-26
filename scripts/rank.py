import pandas as pd

# Define the paths to the CSV files
files = {
    'Ethereum': 'data/ETH-USD.csv',
    'Binance Coin': 'data/BNB-USD.csv',
    'Solana': 'data/SOL-USD.csv',
    'Dogecoin': 'data/DOGE-USD.csv',
    'Cardano': 'data/ADA-USD.csv',
    'Gnosis': 'data/GNO-USD.csv',
    'Bitcoin': 'data/BTC-USD.csv',
}

# Initialize a list to store rows of the new DataFrame
rows = []

# Read each file and extract the latest row
for key, file in files.items():
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure the 'Date' column is in datetime format
    latest_row = df.sort_values(by='Date').iloc[-1]  # Get the latest row
    latest_row['Ticker'] = key  # Add a column for the ticker symbol
    rows.append(latest_row)

# Convert the list of rows to a DataFrame
result_df = pd.DataFrame(rows)

# Reset the index
result_df.reset_index(drop=True, inplace=True)

# Print the resulting DataFrame
print(result_df.sort_values(by='Volume'))
