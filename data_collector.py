import datetime
import requests
import os
import json


def get_options_data(symbol, date, apiKey):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{date}/{date}?apiKey={apiKey}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    symbols = companies = []
    start_date = "2024-01-01"  # Start date for the date range
    end_date = "2024-03-14"    # End date for the date range
    apiKey = "OdewjQFS6xokp5qb0Bom2hjttVW_o3xo"    # Your Polygon.io API key

    for symbol in symbols:
        print(f"Fetching data for {symbol}...")
        symbol_data = {}
        date = start_date
        while date <= end_date:
            options_data = get_options_data(symbol, date, apiKey)
            if options_data:
                symbol_data[date] = options_data 
            else:
                print(f"Failed to retrieve options data for {symbol} on {date}.")
            # Move to the next date
            date = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        folder_path = "data"
        filename = os.path.join(folder_path, f"{symbol}.json")
        save_to_json(symbol_data, filename)
        print(f"Data saved to {filename}")