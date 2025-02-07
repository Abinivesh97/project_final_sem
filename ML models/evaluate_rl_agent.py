import gymnasium as gym
from stable_baselines3 import DQN
from oracle_rl_env import BlockchainOracleEnv

CONTRACT_ADDRESS = "0x4d6780D1ed1F7b7F1079d5163C360964533E6c0c"
ABI_PATH = "D:\\final year project\\project folder\\Final-year-full-sem\\blockchain-oracle\\build\\contracts\\SimpleOracle.json"
RPC_URL = "http://127.0.0.1:7545"

env = BlockchainOracleEnv(contract_address=CONTRACT_ADDRESS, abi_path=ABI_PATH, rpc_url=RPC_URL)
model = DQN.load("dqn_oracle_agent")

obs, _ = env.reset()
done = False

while not done:
    action, _states = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)
    print(f"Action: {action}, Reward: {reward}")
