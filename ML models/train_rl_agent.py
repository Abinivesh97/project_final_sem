import gymnasium as gym
import numpy as np
import requests  
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure
from oracle_rl_env import BlockchainOracleEnv


CONTRACT_ADDRESS = "0x4d6780D1ed1F7b7F1079d5163C360964533E6c0c"  
ABI_PATH = "D:\\final year project\\project folder\\Final-year-full-sem\\blockchain-oracle\\build\\contracts\\SimpleOracle.json"
RPC_URL = "http://127.0.0.1:7545"

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        return response["bitcoin"]["usd"]
    except Exception as e:
        print(f"Error fetching BTC price: {e}")
        return None 

env = BlockchainOracleEnv(contract_address=CONTRACT_ADDRESS, abi_path=ABI_PATH, rpc_url=RPC_URL)
check_env(env)
env = make_vec_env(lambda: env, n_envs=1)  


btc_price = get_btc_price()
if btc_price:
    print(f"[INFO] Current BTC Price: ${btc_price}")
else:
    print("[WARNING] BTC price unavailable. Using previous training data.")

log_dir = "D:/final year project/project folder/Final-year-full-sem/logs"
logger = configure(log_dir, ["stdout", "tensorboard"])

try:
    model = DQN.load("dqn_oracle_agent", env=env)
    print("Loaded existing model. Continuing training...")
except:
    print("No existing model found. Training from scratch...")
    model = DQN(
        "MlpPolicy", env, verbose=1, learning_rate=0.001, buffer_size=10000, batch_size=32, gamma=0.99,
        exploration_initial_eps=1.0, 
        exploration_final_eps=0.01,   
        exploration_fraction=0.3,
        tensorboard_log=log_dir  
    )

model.set_logger(logger)

print("Training Agent...")
model.learn(total_timesteps=5000, tb_log_name="DQN_Oracle")

model.save("dqn_oracle_agent")
print("Training complete. Model updated.")
