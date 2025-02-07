from web3 import Web3
import json
import requests


ganache_url = "http://127.0.0.1:7545"  
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("[INFO] Connected to Ganache")
else:
    print("[ERROR] Failed to connect to Ganache")
    exit()

#  Load Contract ABI & Address
with open("D:\\final year project\\project folder\\Final-year-full-sem\\blockchain-oracle\\build\\contracts\\SimpleOracle.json") as f:
    contract_data = json.load(f)

contract_abi = contract_data["abi"]
contract_address = "0x4d6780D1ed1F7b7F1079d5163C360964533E6c0c"  

# Get contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
print(f"[INFO] Connected to contract at: {contract_address}")

CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

try:
    response = requests.get(CRYPTO_API_URL)
    if response.status_code == 200:
        crypto_data = response.json()
        btc_price = crypto_data["bitcoin"]["usd"]
        print(f"[INFO] Current BTC Price: ${btc_price}")

        new_value = int(btc_price)

        sender_account = web3.eth.accounts[0]  
        tx = contract.functions.updateValue(new_value).transact({'from': sender_account})
        web3.eth.wait_for_transaction_receipt(tx)

        print(f"[SUCCESS] Updated Oracle Value to {new_value}")

    else:
        print("[ERROR] Failed to fetch crypto data")

except Exception as e:
    print(f"[ERROR] Exception: {e}")

try:
    latest_value = contract.functions.getValue().call()
    print(f"[INFO] Stored Oracle Value in Smart Contract: {latest_value}")
except Exception as e:
    print(f"[ERROR] Error reading data: {e}")
