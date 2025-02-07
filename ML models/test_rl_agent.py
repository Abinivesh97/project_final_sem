import gymnasium as gym
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from oracle_rl_env import BlockchainOracleEnv

CONTRACT_ADDRESS = "0x4d6780D1ed1F7b7F1079d5163C360964533E6c0c"  
ABI_PATH = "D:\\final year project\\project folder\\Final-year-full-sem\\blockchain-oracle\\build\\contracts\\SimpleOracle.json"
RPC_URL = "http://127.0.0.1:7545"

env = BlockchainOracleEnv(contract_address=CONTRACT_ADDRESS, abi_path=ABI_PATH, rpc_url=RPC_URL)
env = make_vec_env(lambda: env, n_envs=1)


model = DQN.load("dqn_oracle_agent")


obs = env.reset()  

for step in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info  = env.step(action) 

    print(f"Step {step + 1}: Action={action}, Reward={reward}, New Obs={obs}, info={info}")

    if done:
        print("Episode finished. Resetting environment.")
        obs, _ = env.reset()
