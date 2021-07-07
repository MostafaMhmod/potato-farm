#!/usr/bin/python3

from brownie import Lambo, Usd, accounts


def main():
    usd_token.deploy("Usd", "USD", 18, 1e6, {'from': accounts[0]})
    lambo_token.deploy("Lambo", "LMB", 18, 1e8, {'from': accounts[0]})

    return