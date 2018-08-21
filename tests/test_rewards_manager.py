import pytest
from brownie import reverts, ZERO_ADDRESS, chain
import web3
from conftest import gift_index
from utils.config import ldo_token_address


def test_owner_is_deployer(rewards_manager, ape):
    assert rewards_manager.owner() == ape


def test_stranger_cannot_transfer_ownership(rewards_manager, stranger):
    with reverts("not permitted"):
        rewards_manager.transfer_ownership(stranger, {"from": stranger})


def test_ownership_can_be_transferred(rewards_manager, ape, stranger):
    rewards_manager.transfer_ownership(stranger, {"from": ape})
    assert rewards_manager.owner() == stranger


def test_ownership_can_be_transferred_to_zero_address(rewards_manager, ape):
    rewards_manager.transfer_ownership(ZERO_ADDRESS, {"from": ape})
    assert rewards_manager.owner() == ZERO_ADDRESS


@pytest.mark.usefixtures("set_rewards_contract")
def test_stranger_cannot_set_rewards_contract(rewards_manager, stranger):
    assert rewards_manager.rewards_contract != ZERO_ADDRESS
    with reverts("not permitted"):
        rewards_manager.set_rewards_contract(ZERO_ADDRESS, {"from": stranger})


@pytest.mark.usefixtures("set_rewards_contract")
def test_owner_can_set_rewards_contract(rewards_manager, ape):
    assert rewards_manager.rewards_contract != ZERO_ADDRESS
    rewards_manager.set_rewards_contract(ZERO_ADDRESS, {"from": ape})
    assert rewards_manager.rewards_contract() == ZERO_ADDRESS


@pytest.mark.usefixtures("set_rewards_contract")
def test_owner_can_set_rewards_contract_to_zero_address(rewards_manager, ape):
    assert rewards_manager.rewards_contract != ZERO_ADDRESS
    rewards_manager.set_rewards_contract(ZERO_ADDRESS, {"from": ape})
    assert rewards_manager.rewards_contract() == ZERO_ADDRESS


def test_stranger_cannot_set_gift_index(rewards_manager, stranger):
    assert rewards_manager.gift_index != 0
    with reverts("not permitted"):
        rewards_manager.set_gift_index(0, {"from": stranger})


def test_owner_can_set_gift_index(rewards_manager, ape):
    assert rewards_manager.gift_index != 0
    rewards_manager.set_gift_index(0, {"from": ape})
    assert rewards_manager.gift_index() == 0


@pytest.mark.usefixtures("set_rewards_contract")
def test_is_rewards_period_finished(rewards_manager, farming_rewards):
    reward = farming_rewards.tokenRewards(gift_index)
    assert (chain[-1].timestamp >= reward[4]) == rewards_manager.is_rewards_period_finished()


@pytest.mark.usefixtures("set_rewards_contract")
def test_out_of_funding_date(rewards_manager, farming_rewards):
    reward = farming_rewards.tokenRewards(gift_index)
    assert reward[4] == rewards_manager.out_of_funding_date()


def test_start_next_rewards_period_with_zero_address_and_gift_index(rewards_manager, ape):
    with reverts("manager: rewards disabled"):
        rewards_manager.start_next_rewards_period({"from": ape})


# @pytest.mark.usefixtures("set_rewards_contract")
# @pytest.mark.require_network("development")
# def test_start_next_rewards_period_non_zero_balance_dev(rewards_manager, rewards_token, ape, stranger):
#     rewards_token.transfer(rewards_manager.address, 100, {"from": ape})
#     assert rewards_token.balanceOf(rewards_manager.address) > 0



