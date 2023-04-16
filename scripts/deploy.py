from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpfulScripts import *
from web3 import Web3
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)


def deployFundMe():
    account = getAccount()
    print("Account : ", account)
    ## To deploy, we need to give it the arguments needed in the constructor
    # If we are in persistent network like sepolia, use associated network
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print("Price feed address : ", price_feed_address)
    else:
        ## Using mock. We will deploy our own price feed contract
        deployMocks()
        mock_aggregator = MockV3Aggregator[-1]
        price_feed_address = mock_aggregator.address

    fundMe = FundMe.deploy(
        price_feed_address,
        {"from": account, "gas_price": gas_strategy},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed at : ", fundMe.address)
    return fundMe


def main():
    deployFundMe()
