from scripts.helpfulScripts import *
from scripts.deploy import deployFundMe
import pytest
from brownie import exceptions

def test_can_fund_and_withdraw():
    print("Test")
    account = getAccount()
    fund_me = deployFundMe()
    print("We try getting the entrance fee")
    entrance_fee = fund_me.getEntranceFee() +100
    print("We got the entrance fee")
    print("Fund")
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    print("Fund done")
    print("Entrance fee :", entrance_fee)
    print("User balance : ", fund_me.getUserBalance())
    assert fund_me.getUserBalance() == entrance_fee
    print("Withdraw")
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    print("We've withdraw")
    assert fund_me.getUserBalance() == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fundMe = deployFundMe()
    bad_actor = accounts[3]
    with pytest.raises(exceptions.VirtualMachineError):
        fundMe.withdraw({"from": bad_actor})

