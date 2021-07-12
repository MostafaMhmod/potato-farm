#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def usd(Usd, accounts):
    return Usd.deploy("Usd", "USD", 18, 1e24, {'from': accounts[0]})


@pytest.fixture(scope="module")
def potato(Potato, accounts):
    return Potato.deploy("Potato", "PTO", 18, 1e24, {'from': accounts[0]})


@pytest.fixture(scope="module")
def simple_chef(SimpleChef, potato, usd, accounts):
    simple_chef = SimpleChef.deploy(potato.address, usd.address, {'from': accounts[0]})
    potato.updateAdmin(simple_chef.address, {'from': accounts[0]})
    return simple_chef
