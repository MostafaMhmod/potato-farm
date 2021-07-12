import brownie


def test_potato_is_minted_by_owner(accounts, potato):
    potato_total_supply_before_mint = potato.totalSupply.call()
    potato.mint(accounts[0],1e24),{'from': accounts[0]}
    potato_total_supply_after_mint = potato.totalSupply.call()

    assert potato_total_supply_before_mint < potato_total_supply_after_mint


def test_potato_mint_fails_if_not_by_the_owner(accounts, potato):
    with brownie.reverts():
        potato.mint(accounts[1], 1e24,{'from': accounts[1]})
