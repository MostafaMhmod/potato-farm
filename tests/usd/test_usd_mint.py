import brownie


def test_usd_is_minted(accounts, usd):
    usd_total_supply_before_mint = usd.totalSupply.call()
    usd.mint(accounts[1], 1e24, {'from': accounts[1]})
    usd_total_supply_after_mint = usd.totalSupply.call()

    assert usd_total_supply_before_mint < usd_total_supply_after_mint

