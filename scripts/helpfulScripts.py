from brownie import FundMe, network, config, MockV3Aggregator, accounts
from web3 import Web3
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

FORKED = ["mainnet-fork"]
DECIMALS = 18
STARTINGPRICE = 2000

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]


def getAccount():
    print("Network : ",network.show_active())
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED:
        return accounts[0]
    elif network.show_active() == "sepolia":
        return accounts.add(config["wallets"]['sepolia']["from_key"])
    else:
        pass


def deployMocks():
    print(f"The active network is {network.show_active()}")
    if len(MockV3Aggregator) <= 0:
        print("Deploying mocks...")
        MockV3Aggregator.deploy(
            DECIMALS,
            Web3.toWei(STARTINGPRICE, "ether"),
            {"from": getAccount(), "gas_price": gas_strategy},
        )
        print("Mocks deployed")
