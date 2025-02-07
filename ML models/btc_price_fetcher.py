import requests
import time

class BTCPriceFetcher:
    """Fetch BTC prices from multiple sources and compute a trustworthiness score."""

    def __init__(self, update_interval=60):
        self.sources = {
            "coingecko": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            "binance": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
            "kraken": "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
        }
        self.trust_scores = {source: 1.0 for source in self.sources}
        self.last_update_time = 0
        self.cached_price = 50000
        self.update_interval = update_interval

    def fetch_price(self):
        """Fetch BTC prices from multiple sources and determine the most reliable one."""
        current_time = time.time()
        if current_time - self.last_update_time < self.update_interval:
            return self.cached_price  

        prices = {}
        for source, url in self.sources.items():
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()

                if source == "coingecko":
                    prices[source] = data["bitcoin"]["usd"]
                elif source == "binance":
                    prices[source] = float(data["price"])
                elif source == "kraken":
                    prices[source] = float(data["result"]["XXBTZUSD"]["c"][0])

            except requests.exceptions.RequestException as e:
                print(f"[ERROR] {source} API Failed: {e}")
                self.trust_scores[source] *= 0.9  

        if not prices:
            print("[WARNING] No sources available, using cached price.")
            return self.cached_price

        # Calculate weighted average using trustworthiness scores
        total_weight = sum(self.trust_scores[src] for src in prices.keys())
        weighted_price = sum(prices[src] * self.trust_scores[src] for src in prices.keys()) / total_weight

        self.cached_price = weighted_price
        self.last_update_time = current_time
        print(f"[INFO] Selected BTC Price: ${self.cached_price:.2f} (Weighted by trust scores)")

        return self.cached_price
