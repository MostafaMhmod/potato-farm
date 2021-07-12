#!/usr/bin/python3
import brownie


def test_usd_sender_balance_decreases(accounts, usd):
    sender_balance = usd.balanceOf(accounts[0])
    amount = sender_balance // 4

    usd.approve(accounts[1], amount, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert usd.balanceOf(accounts[0]) == sender_balance - amount


def test_usd_receiver_balance_increases(accounts, usd):
    receiver_balance = usd.balanceOf(accounts[2])
    amount = usd.balanceOf(accounts[0]) // 4

    usd.approve(accounts[1], amount, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert usd.balanceOf(accounts[2]) == receiver_balance + amount


def test_usd_caller_balance_not_affected(accounts, usd):
    caller_balance = usd.balanceOf(accounts[1])
    amount = usd.balanceOf(accounts[0])

    usd.approve(accounts[1], amount, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert usd.balanceOf(accounts[1]) == caller_balance


def test_usd_caller_approval_affected(accounts, usd):
    approval_amount = usd.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    usd.approve(accounts[1], approval_amount, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert usd.allowance(accounts[0], accounts[1]) == approval_amount - transfer_amount


def test_usd_receiver_approval_not_affected(accounts, usd):
    approval_amount = usd.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    usd.approve(accounts[1], approval_amount, {'from': accounts[0]})
    usd.approve(accounts[2], approval_amount, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert usd.allowance(accounts[0], accounts[2]) == approval_amount


def test_usd_total_supply_not_affected(accounts, usd):
    total_supply = usd.totalSupply()
    amount = usd.balanceOf(accounts[0])

    usd.approve(accounts[1], amount, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert usd.totalSupply() == total_supply


def test_usd_returns_true(accounts, usd):
    amount = usd.balanceOf(accounts[0])
    usd.approve(accounts[1], amount, {'from': accounts[0]})
    tx = usd.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert tx.return_value is True


def test_usd_transfer_full_balance(accounts, usd):
    amount = usd.balanceOf(accounts[0])
    receiver_balance = usd.balanceOf(accounts[2])

    usd.approve(accounts[1], amount, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert usd.balanceOf(accounts[0]) == 0
    assert usd.balanceOf(accounts[2]) == receiver_balance + amount


def test_usd_transfer_zero_usds(accounts, usd):
    sender_balance = usd.balanceOf(accounts[0])
    receiver_balance = usd.balanceOf(accounts[2])

    usd.approve(accounts[1], sender_balance, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert usd.balanceOf(accounts[0]) == sender_balance
    assert usd.balanceOf(accounts[2]) == receiver_balance


def test_usd_transfer_zero_usds_without_approval(accounts, usd):
    sender_balance = usd.balanceOf(accounts[0])
    receiver_balance = usd.balanceOf(accounts[2])

    usd.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert usd.balanceOf(accounts[0]) == sender_balance
    assert usd.balanceOf(accounts[2]) == receiver_balance


def test_usd_insufficient_balance(accounts, usd):
    balance = usd.balanceOf(accounts[0])

    usd.approve(accounts[1], balance + 1, {'from': accounts[0]})
    with brownie.reverts():
        usd.transferFrom(accounts[0], accounts[2], balance + 1, {'from': accounts[1]})


def test_usd_insufficient_approval(accounts, usd):
    balance = usd.balanceOf(accounts[0])
    print(balance)
    usd.approve(accounts[1], balance - 1, {'from': accounts[0]})
    with brownie.reverts():
        usd.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_usd_no_approval(accounts, usd):
    balance = usd.balanceOf(accounts[0])

    with brownie.reverts():
        usd.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_usd_revoked_approval(accounts, usd):
    balance = usd.balanceOf(accounts[0])

    usd.approve(accounts[1], balance, {'from': accounts[0]})
    usd.approve(accounts[1], 0, {'from': accounts[0]})

    with brownie.reverts():
        usd.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_usd_transfer_to_self(accounts, usd):
    sender_balance = usd.balanceOf(accounts[0])
    amount = sender_balance // 4

    usd.approve(accounts[0], sender_balance, {'from': accounts[0]})
    usd.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})

    assert usd.balanceOf(accounts[0]) == sender_balance
    assert usd.allowance(accounts[0], accounts[0]) == sender_balance - amount


def test_usd_transfer_to_self_no_approval(accounts, usd):
    amount = usd.balanceOf(accounts[0])

    with brownie.reverts():
        usd.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})


def test_usd_transfer_event_fires(accounts, usd):
    amount = usd.balanceOf(accounts[0])

    usd.approve(accounts[1], amount, {'from': accounts[0]})
    tx = usd.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[2], amount]
