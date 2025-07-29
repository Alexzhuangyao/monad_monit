# Monad 代币监控工具

这是一个基于Python的 **Monad区块链** 代币余额监控工具，使用 `web3.py` 库连接Monad测试网RPC接口，实时监测自定义ERC20代币和MON原生币余额变化。支持多地址批量监控，并输出余额变化提示。

示例：
<img width="1954" height="1414" alt="ffbf9aac-b913-4208-95b0-103cea22a0bf" src="https://github.com/user-attachments/assets/80d845ef-a8ba-4e83-a789-aff8f3a6bcca" />


## 功能

- 连接Monad测试网 RPC 节点。
- 读取指定ERC20代币和MON代币余额。
- 支持多个地址持续轮询监控余额。
- 提示MON代币及指定代币的余额变化（增减或无变化）。
- 显示余额信息及对应区块浏览器链接。

## 环境依赖

- Python 3.6+
- `web3` Python库

安装方式：

```bash
pip install web3
```

## 配置说明

在脚本中修改以下变量：

- `RPC_URL`：Monad测试网RPC接口地址（默认 `https://testnet-rpc.monad.xyz`）。
- `EXPLORER_URL`：Monad测试网区块浏览器地址（默认 `https://testnet.monadexplorer.com`）。
- `TOKEN_CONTRACT`：需要监控的ERC20代币合约地址。
- `addresses` 字典：待监控地址列表及对应备注名称。

## 使用方法

运行脚本：

```bash
python monitor.py
```

脚本每隔1小时（3600秒）自动刷新一次余额信息，输出当前时间戳、地址余额及余额变化情况。

## 代码简介

- `TokenMonitor` 类负责通过 `web3.py` 连接RPC节点，调用合约 `balanceOf`、`symbol`、`decimals` 接口读取代币余额。
- 通过 `w3.eth.get_balance()` 获取MON原生代币余额。
- 维护前一次余额状态，计算并提示余额变化。
- 支持多地址批量监控，循环定时调用监控函数。

## 注意事项

- 请确保网络连通RPC接口。
- 合约ABI只包含必要的ERC20接口，其他功能未实现。
- 监控间隔和地址列表可根据需求自定义。
- 运行前请替换`addresses`字典中的地址为实际监控地址。

此工具适合需要定时监控Monad链上ERC20代币及MON主币余额的开发者或用户，帮助及时掌握资金变化动态。

如需进一步扩展功能，例如监听转账事件、发送交易等，可基于 `web3.py` 继续开发。




