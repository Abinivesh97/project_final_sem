import gymnasium as gym  
from gymnasium import spaces
from web3 import Web3
import json
from btc_price_fetcher import BTCPriceFetcher

btc_fetcher = BTCPriceFetcher()

class BlockchainOracleEnv(gym.Env):
    def __init__(self, contract_address, abi_path, rpc_url):
        super().__init__()

        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        assert self.web3.is_connected(), "Failed to connect to blockchain"

        # Load contract ABI
        with open(abi_path, "r") as f:
            contract_json = json.load(f)
            contract_abi = contract_json["abi"]

        # Get contract instance
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        
        self.action_space = spaces.Discrete(2)
    
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=np.float32)

    def step(self, action):
    
        current_value = self.contract.functions.getValue().call()
        print(f"[DEBUG] Step: Fetched Oracle Value from Blockchain: {current_value}")

        # Fetch latest BTC price (cached, updates every 60s)
        btc_price = btc_fetcher.fetch_price()
        print(f"[INFO] Current BTC Price: ${btc_price}")

        # Normalize values
        oracle_norm = min(current_value / 100000.0, 1.0)  
        btc_norm = btc_price / 100000  

        obs = np.array([oracle_norm, btc_norm], dtype=np.float32)

        reward = -1  

        if action == 1:  
            new_value = int(btc_price)  
            print(f"[DEBUG] Step: Updating Oracle Value to: {new_value}")

            tx_hash = self.contract.functions.updateValue(new_value).transact({"from": self.web3.eth.accounts[0]})
            self.web3.eth.wait_for_transaction_receipt(tx_hash)

            
            if abs(new_value - current_value) > 100:
                reward = 10  
            else:
                reward = -15  
        else:
            reward = 5  

        done = False  
        truncated = False  

        return obs, reward, done, truncated, {} 

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  

        # Fetch latest oracle value
        current_value = self.contract.functions.getValue().call()
        print(f"[DEBUG] Reset: Initial Oracle Value: {current_value}")

        btc_price = btc_fetcher.fetch_price()
        print(f"[INFO] Initial BTC Price: ${btc_price}")

        oracle_norm = min(current_value / 100000.0, 1.0)
        btc_norm = btc_price / 100000

        obs = np.array([oracle_norm, btc_norm], dtype=np.float32)

        return obs, {}  

    def render(self, mode='human'):
        print(f"Oracle Value: {self.contract.functions.getValue().call()}")
