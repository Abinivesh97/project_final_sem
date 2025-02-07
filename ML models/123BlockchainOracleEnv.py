import gym
import numpy as np
import requests
from gym import spaces
from web3 import Web3
import json

class BlockchainOracleEnv(gym.Env):
    def __init__(self, contract_address, abi_path, rpc_url):
        super(BlockchainOracleEnv, self).__init__()

        # Connect to Ganache
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        assert self.web3.is_connected(), "Failed to connect to blockchain"

        # Load contract ABI
        with open(abi_path, "r") as f:
            contract_json = json.load(f)
            contract_abi = contract_json["abi"]

        # Get contract instance
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)

        # Action space: 0 (do nothing) or 1 (update value)
        self.action_space = spaces.Discrete(2)

        # Observation space: Current oracle value (normalized)
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)

    def get_btc_price(self):
        """Fetch real-time BTC price from CoinGecko API"""
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        try:
            response = requests.get(url).json()
            return response["bitcoin"]["usd"]
        except Exception as e:
            print(f"Error fetching BTC price: {e}")
            return None

    def step(self, action):
        btc_price = self.get_btc_price()
        if btc_price is None:
            btc_price = 50000  # Default fallback value
        
        current_value = self.contract.functions.getValue().call()
        obs = np.array([current_value / 100000.0], dtype=np.float32)

        reward = 10
        if action == 1:  # If agent chooses to update value
            new_value = int(btc_price)  # Use real BTC price as new oracle value
            tx_hash = self.contract.functions.updateValue(new_value).transact({"from": self.web3.eth.accounts[0]})
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            reward = -abs(new_value - current_value) / 100  # More reward if value changes correctly
        else:
            reward = -abs(current_value - btc_price) / 500  # Small negative reward if value is far from BTC price

        done = False
        truncated = False  # Add truncated flag (needed for Gymnasium)

        return obs, reward, done, truncated, {} # Return 5 values as required

    def reset(self, seed=None, options=None):
        """ Ensure compatibility with Gymnasium """
        super().reset(seed=seed)

        current_value = self.contract.functions.getValue().call()
        obs = np.array([current_value / 100000.0], dtype=np.float32)
        return obs, {}
    
    def seed(self, seed=None):
        """Set the seed for reproducibility (optional)."""
        np.random.seed(seed)

    def render(self, mode='human'):
        print(f"Oracle Value: {self.contract.functions.getValue().call()}")
