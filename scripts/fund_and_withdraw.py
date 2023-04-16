from brownie import FundMe
from scripts.helpfulScripts import *
import time

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)


def fund():
    fundMe = FundMe[-1]
    account = getAccount()
    entrance_fee = fundMe.getEntranceFee()
    print(entrance_fee)
    print("funding : ")
    print("Sending : ", entrance_fee)
    fundMe.fund({"from": account, "value": Web3.toWei(1, "ether")})


def withdraw():
    fundMe = FundMe[-1]
    print("Contract balance : ", fundMe.balance())
    account = getAccount()
    print("msg.sender :     ", account)
    print("Contract owner : ", fundMe.owner())

    print("withdraw...")
    fundMe.withdraw({"from": account})
    print("Withdraw successful")


def main():
    fund()
    # time.sleep(10)
    withdraw()
