#!/usr/bin/python3
import brownie


def test_potato_sender_balance_decreases(accounts, potato):
    sender_balance = potato.balanceOf(accounts[0])
    amount = sender_balance // 4

    potato.transfer(accounts[1], amount, {'from': accounts[0]})

    assert potato.balanceOf(accounts[0]) == sender_balance - amount


def test_potato_receiver_balance_increases(accounts, potato):
    receiver_balance = potato.balanceOf(accounts[1])
    amount = potato.balanceOf(accounts[0]) // 4

    potato.transfer(accounts[1], amount, {'from': accounts[0]})

    assert potato.balanceOf(accounts[1]) == receiver_balance + amount


def test_potato_total_supply_not_affected(accounts, potato):
    total_supply = potato.totalSupply()
    amount = potato.balanceOf(accounts[0])

    potato.transfer(accounts[1], amount, {'from': accounts[0]})

    assert potato.totalSupply() == total_supply


def test_potato_returns_true(accounts, potato):
    amount = potato.balanceOf(accounts[0])
    tx = potato.transfer(accounts[1], amount, {'from': accounts[0]})

    assert tx.return_value is True


def test_potato_transfer_full_balance(accounts, potato):
    amount = potato.balanceOf(accounts[0])
    receiver_balance = potato.balanceOf(accounts[1])

    potato.transfer(accounts[1], amount, {'from': accounts[0]})

    assert potato.balanceOf(accounts[0]) == 0
    assert potato.balanceOf(accounts[1]) == receiver_balance + amount


def test_potato_transfer_zero_potatos(accounts, potato):
    sender_balance = potato.balanceOf(accounts[0])
    receiver_balance = potato.balanceOf(accounts[1])

    potato.transfer(accounts[1], 0, {'from': accounts[0]})

    assert potato.balanceOf(accounts[0]) == sender_balance
    assert potato.balanceOf(accounts[1]) == receiver_balance


def test_potato_transfer_to_self(accounts, potato):
    sender_balance = potato.balanceOf(accounts[0])
    amount = sender_balance // 4

    potato.transfer(accounts[0], amount, {'from': accounts[0]})

    assert potato.balanceOf(accounts[0]) == sender_balance


def test_potato_insufficient_balance(accounts, potato):
    balance = potato.balanceOf(accounts[0])

    with brownie.reverts():
        potato.transfer(accounts[1], balance + 1, {'from': accounts[0]})


def test_potato_transfer_event_fires(accounts, potato):
    amount = potato.balanceOf(accounts[0])
    tx = potato.transfer(accounts[1], amount, {'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]
