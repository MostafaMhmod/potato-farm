#!/usr/bin/python3

import pytest


@pytest.mark.parametrize("idx", range(5))
def test_potato_initial_approval_is_zero(usd, accounts, idx):
    assert usd.allowance(accounts[0], accounts[idx]) == 0


def test_potato_approve(usd, accounts):
    usd.approve(accounts[1], 10**19, {'from': accounts[0]})

    assert usd.allowance(accounts[0], accounts[1]) == 10**19


def test_potato_modify_approve(usd, accounts):
    usd.approve(accounts[1], 10**19, {'from': accounts[0]})
    usd.approve(accounts[1], 12345678, {'from': accounts[0]})

    assert usd.allowance(accounts[0], accounts[1]) == 12345678


def test_potato_revoke_approve(usd, accounts):
    usd.approve(accounts[1], 10**19, {'from': accounts[0]})
    usd.approve(accounts[1], 0, {'from': accounts[0]})

    assert usd.allowance(accounts[0], accounts[1]) == 0


def test_potato_approve_self(usd, accounts):
    usd.approve(accounts[0], 10**19, {'from': accounts[0]})

    assert usd.allowance(accounts[0], accounts[0]) == 10**19


def test_potato_only_affects_target(usd, accounts):
    usd.approve(accounts[1], 10**19, {'from': accounts[0]})

    assert usd.allowance(accounts[1], accounts[0]) == 0


def test_potato_returns_true(usd, accounts):
    tx = usd.approve(accounts[1], 10**19, {'from': accounts[0]})

    assert tx.return_value is True


def test_potato_approval_event_fires(accounts, usd):
    tx = usd.approve(accounts[1], 10**19, {'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Approval"].values() == [accounts[0], accounts[1], 10**19]
