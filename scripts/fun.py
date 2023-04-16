from brownie import FundMe, network, config
from scripts.helpfulScripts import *

def deployFundMe():
    account = getAccount()
    fundMe = FundMe[-1]
    print(fundMe.getVersion())
    print(fundMe.getEthAmountToUSD(1))


def main():
    deployFundMe()