#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(Token, accounts):
    return Token.deploy("Test Token", "TST", 18, 1e21, {'from': accounts[0]})

@pytest.fixture(scope="module")
def usd_token(usd_token, accounts):
    return usd_token.deploy("Usd", "USD", 18, 1e6, {'from': accounts[0]})

@pytest.fixture(scope="module")
def potato_token(potato_token, accounts):
    return potato_token.deploy("Potato", "LMB", 18, 1e8, {'from': accounts[0]})

