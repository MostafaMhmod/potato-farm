#!/usr/bin/python3
import brownie


def test_usd_sender_balance_decreases(accounts, usd):
    sender_balance = usd.balanceOf(accounts[0])
    amount = sender_balance // 4

    usd.transfer(accounts[1], amount, {'from': accounts[0]})

    assert usd.balanceOf(accounts[0]) == sender_balance - amount


def test_usd_receiver_balance_increases(accounts, usd):
    receiver_balance = usd.balanceOf(accounts[1])
    amount = usd.balanceOf(accounts[0]) // 4

    usd.transfer(accounts[1], amount, {'from': accounts[0]})

    assert usd.balanceOf(accounts[1]) == receiver_balance + amount


def test_usd_total_supply_not_affected(accounts, usd):
    total_supply = usd.totalSupply()
    amount = usd.balanceOf(accounts[0])

    usd.transfer(accounts[1], amount, {'from': accounts[0]})

    assert usd.totalSupply() == total_supply


def test_usd_returns_true(accounts, usd):
    amount = usd.balanceOf(accounts[0])
    tx = usd.transfer(accounts[1], amount, {'from': accounts[0]})

    assert tx.return_value is True


def test_usd_transfer_full_balance(accounts, usd):
    amount = usd.balanceOf(accounts[0])
    receiver_balance = usd.balanceOf(accounts[1])

    usd.transfer(accounts[1], amount, {'from': accounts[0]})

    assert usd.balanceOf(accounts[0]) == 0
    assert usd.balanceOf(accounts[1]) == receiver_balance + amount


def test_usd_transfer_zero_usds(accounts, usd):
    sender_balance = usd.balanceOf(accounts[0])
    receiver_balance = usd.balanceOf(accounts[1])

    usd.transfer(accounts[1], 0, {'from': accounts[0]})

    assert usd.balanceOf(accounts[0]) == sender_balance
    assert usd.balanceOf(accounts[1]) == receiver_balance


def test_usd_transfer_to_self(accounts, usd):
    sender_balance = usd.balanceOf(accounts[0])
    amount = sender_balance // 4

    usd.transfer(accounts[0], amount, {'from': accounts[0]})

    assert usd.balanceOf(accounts[0]) == sender_balance


def test_usd_insufficient_balance(accounts, usd):
    balance = usd.balanceOf(accounts[0])

    with brownie.reverts():
        usd.transfer(accounts[1], balance + 1, {'from': accounts[0]})


def test_usd_transfer_event_fires(accounts, usd):
    amount = usd.balanceOf(accounts[0])
    tx = usd.transfer(accounts[1], amount, {'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]
