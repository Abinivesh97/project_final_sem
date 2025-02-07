import gym
import numpy as np
from gym import spaces
from web3 import Web3
import json

class BlockchainOracleEnv(gym.Env):
    def __init__(self, contract_address, abi_path, rpc_url):
        super(BlockchainOracleEnv, self).__init__()

        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        assert self.web3.is_connected(), "Failed to connect to blockchain"

        # Load contract ABI
        with open(abi_path, "r") as f:
            contract_json = json.load(f)
            contract_abi = contract_json["abi"]

        
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        
       
        self.action_space = spaces.Discrete(2)
        
        
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)

    def step(self, action):
        current_value = self.contract.functions.getValue().call()
        obs = np.array([min(current_value / 100000.0, 1.0)], dtype=np.float32)  


        reward = 10
        if action == 1:  
            print(current_value)
            new_value = np.random.randint(1, 1000)  
            tx_hash = self.contract.functions.updateValue(new_value).transact({"from": self.web3.eth.accounts[0]})
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            reward = -abs(new_value - current_value) / 100 
        
        else:  
            reward = -abs(current_value - 500) / 200  

        done = False
        truncated = False  

        return obs, reward, done, truncated, {} 

    def reset(self, seed=None, options=None):
        """ Ensure compatibility with Gymnasium """
        super().reset(seed=seed)

        current_value = self.contract.functions.getValue().call()
        obs = np.array([min(current_value / 100000.0, 1.0)], dtype=np.float32) 

        return obs, {}
    
    def seed(self, seed=None):
        """Set the seed for reproducibility (optional)."""
        np.random.seed(seed)

    def render(self, mode='human'):
        print(f"Oracle Value: {self.contract.functions.getValue().call()}")
