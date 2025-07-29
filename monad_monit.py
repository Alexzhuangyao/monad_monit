from web3 import Web3
import time
from datetime import datetime
import json

# 配置
RPC_URL = "https://testnet-rpc.monad.xyz"
EXPLORER_URL = "https://testnet.monadexplorer.com"
TOKEN_CONTRACT = "0x22a3d96424df6f04d02477cb5ba571bbf615f47e"

# 颜色代码
RED = "\033[91m"
RESET = "\033[0m"

# ERC20代币的ABI
ERC20_ABI = json.loads('''
[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]
''')

class TokenMonitor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
        self.token_contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(TOKEN_CONTRACT),
            abi=ERC20_ABI
        )
        self.previous_balances = {}
        self.previous_native_balances = {}
        
    def get_token_info(self):
        try:
            symbol = self.token_contract.functions.symbol().call()
            decimals = self.token_contract.functions.decimals().call()
            return symbol, decimals
        except Exception as e:
            print(f"❌ 获取代币信息时出错: {str(e)}")
            return "Unknown", 18
            
    def monitor_address(self, address, name):
        try:
            # 确保地址格式正确
            checksum_address = self.w3.to_checksum_address(address)
            
            # 获取MON原生代币余额
            native_balance = self.w3.eth.get_balance(checksum_address)
            native_balance_eth = self.w3.from_wei(native_balance, 'ether')
            
            # 获取代币余额
            token_balance = self.token_contract.functions.balanceOf(checksum_address).call()
            symbol, decimals = self.get_token_info()
            token_balance_decimal = token_balance / (10 ** decimals)
            
            # 打印信息
            print(f"\n📍 地址: {checksum_address} | {name}")
            print(f"💰 MON余额: {native_balance_eth:.6f} MON")
            print(f"💎 代币余额: {token_balance_decimal:.6f} {symbol}")
            print(f"🔍 区块浏览器: {EXPLORER_URL}/address/{checksum_address}?tab=Token")
            
            # 检查MON余额变化
            previous_native = self.previous_native_balances.get(checksum_address)
            if previous_native is not None:
                previous_native_eth = self.w3.from_wei(previous_native, 'ether')
                native_diff = native_balance_eth - previous_native_eth
                if native_diff > 0:
                    print(f"📈 MON较上次增加: +{native_diff:.6f} MON")
                elif native_diff < 0:
                    print(f"📉 MON较上次减少: {native_diff:.6f} MON")
                else:
                    print(f"{RED}📊 MON余额无变化{RESET}")
            
            # 检查代币余额变化
            previous_token = self.previous_balances.get(checksum_address)
            if previous_token is not None:
                previous_token_decimal = previous_token / (10 ** decimals)
                token_diff = token_balance_decimal - previous_token_decimal
                if token_diff > 0:
                    print(f"📈 {symbol}较上次增加: +{token_diff:.6f} {symbol}")
                elif token_diff < 0:
                    print(f"📉 {symbol}较上次减少: {token_diff:.6f} {symbol}")
                else:
                    print(f"📊 {symbol}余额无变化")
            
            # 更新上次余额
            self.previous_native_balances[checksum_address] = native_balance
            self.previous_balances[checksum_address] = token_balance
            
            return True
            
        except Exception as e:
            print(f"❌ 监控地址 {address} ({name}) 时出错: {str(e)}")
            return False

def main():
    print("🔄 Monad代币监控工具")
    
    monitor = TokenMonitor()
    
    # 检查连接
    if not monitor.w3.is_connected():
        print("❌ 无法连接到Monad网络")
        return
        
    print(f"✅ 已连接到Monad网络")
    
    # 要监控的地址列表
    addresses = {
        "your-monad-address": "m4_hedge",
        "your-monad-address": "m2-0",
        "your-monad-address": "m2-1",
        "your-monad-address": "m2-2",
        "your-monad-address": "m2-3",
        "your-monad-address": "m2-4",
        "your-monad-address": "m2-5",
        "your-monad-address": "m2-6",
        "your-monad-address": "m4_da"
    }
    
    while True:
        print("\n" + "="*50)
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for address, name in addresses.items():
            monitor.monitor_address(address, name)
                
        print("\n💤 3600秒后更新...")
        time.sleep(3600)

if __name__ == "__main__":
    main() 
