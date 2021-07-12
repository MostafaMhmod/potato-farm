#!/usr/bin/python3

from brownie import accounts, Potato, Usd, SimpleChef

account=accounts.load('testing')
usd_token=None
potato_token=None
simple_chef=None

def main():
    usd_token = Usd.deploy("Usd", "USD", 18, 1e24, {'from': account}, publish_source=True)
    potato_token = Potato.deploy("Potato", "PTO", 18, 0, {'from': account}, publish_source=True)
    simple_chef = SimpleChef.deploy(potato_token.address, usd_token.address,{'from': account}, publish_source=True)
    potato_token.updateAdmin(simple_chef.address,{'from': account})
    return
    