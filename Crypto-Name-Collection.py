import requests
import json

def get_data(url):
    try:
        print(f'Fetching cryptocurrencies from {url}...')
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f'Gathered {len(data)} cryptocurrencies.')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        data = []
    return data

def fetch_all_cryptocurrencies():
    # Coingecko (list)
    url_coingecko_list = "https://api.coingecko.com/api/v3/coins/list"
    data_coingecko_list = get_data(url_coingecko_list)
    names_coingecko_list = [d['name'] for d in data_coingecko_list if isinstance(d, dict) and 'name' in d]

    # Coingecko (search)
    url_coingecko_search = "https://api.coingecko.com/api/v3/search/trending"
    data_coingecko_search = get_data(url_coingecko_search)
    names_coingecko_search = [d['item']['name'] for d in data_coingecko_search.get('coins', []) if isinstance(d, dict) and 'item' in d and 'name' in d['item']]

    # CoinMarketCap
    url_coinmarketcap = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10000&sortBy=market_cap&sortType=desc&convert=USD"
    data_coinmarketcap = get_data(url_coinmarketcap)
    names_coinmarketcap = [d['name'] for d in data_coinmarketcap.get('data', {}).get('cryptoCurrencyList', []) if isinstance(d, dict) and 'name' in d]

    # CoinPaprika
    url_coinpaprika = "https://api.coinpaprika.com/v1/coins"
    data_coinpaprika = get_data(url_coinpaprika)
    names_coinpaprika = [d['name'] for d in data_coinpaprika if isinstance(d, dict) and 'name' in d]

    # CryptoCompare
    url_cryptocompare = "https://min-api.cryptocompare.com/data/all/coinlist"
    data_cryptocompare = get_data(url_cryptocompare)
    names_cryptocompare = [v['CoinName'] for k, v in data_cryptocompare.get('Data', {}).items() if isinstance(v, dict) and 'CoinName' in v]

    # CoinCap
    url_coincap = "https://api.coincap.io/v2/assets"
    data_coincap = get_data(url_coincap)
    names_coincap = [d['name'] for d in data_coincap.get('data', []) if isinstance(d, dict) and 'name' in d]

    # CoinLore
    url_coinlore = "https://api.coinlore.net/api/tickers/?start=0&limit=5000"
    data_coinlore = get_data(url_coinlore)
    names_coinlore = [d['name'] for d in data_coinlore.get('data', []) if isinstance(d, dict) and 'name' in d]

    # Coinranking
    url_coinranking = "https://api.coinranking.com/v2/coins"
    data_coinranking = get_data(url_coinranking)
    names_coinranking = [d['name'] for d in data_coinranking.get('data', {}).get('coins', []) if isinstance(d, dict) and 'name' in d]

    # Combine and remove duplicates
    return list(set(names_coingecko_list + names_coingecko_search + names_coinmarketcap + names_coinpaprika + names_cryptocompare + names_coincap + names_coinlore + names_coinranking))



# Read existing cryptocurrencies from file
try:
    with open("cryptocurrencies.json", "r") as file:
        existing_cryptocurrencies = json.load(file)
except FileNotFoundError:
    existing_cryptocurrencies = []

cryptocurrency_names = list(set(existing_cryptocurrencies + fetch_all_cryptocurrencies()))

with open("cryptocurrencies.json", "w") as file:
    json.dump(cryptocurrency_names, file)

print(f"There are {len(cryptocurrency_names)} unique cryptocurrencies in the file.")
