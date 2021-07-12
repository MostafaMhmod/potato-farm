import brownie


def test_simple_chef_potato_per_block(accounts, simple_chef):
    assert simple_chef.potatoPerBlock.call() >= 1e18


def test_simple_chef_deposit_fails_if_not_approved(accounts, simple_chef):
    with brownie.reverts():
        simple_chef.deposit(1e18, {'from': accounts[0]})


def test_simple_chef_deposits_if_approved(accounts, usd, simple_chef):
    usd.approve(simple_chef.address, 1e24, {'from': accounts[0]})
    simple_chef.deposit(1e18, {'from': accounts[0]})


def test_simple_chef_stake_successed(accounts, usd, potato, simple_chef):
    start_block = simple_chef.startBlock.call()
    potato_total_supply = potato.totalSupply.call()
    usd.approve(simple_chef.address, 1e24, {'from': accounts[0]})

    simple_chef.deposit(1, {'from': accounts[0]})
    simple_chef.withdraw(1, {'from': accounts[0]})

    assert potato_total_supply < potato.totalSupply.call()


def test_simple_chef_stake_reverts_if_no_usd_balance(accounts, usd, potato, simple_chef):
    start_block = simple_chef.startBlock.call()
    account_usd_balance = usd.balanceOf(accounts[0])

    usd.approve(simple_chef.address, 1e24, {'from': accounts[0]})
    with brownie.reverts():
        simple_chef.deposit(account_usd_balance + 1, {'from': accounts[0]})


def test_simple_chef_stake_reverts_if_no_usd_sufficient_allowance(accounts, usd, simple_chef):
    start_block = simple_chef.startBlock.call()
    account_usd_balance = usd.balanceOf(accounts[0])

    usd.approve(simple_chef.address, 1, {'from': accounts[0]})
    with brownie.reverts():
        simple_chef.deposit(account_usd_balance, {'from': accounts[0]})


def test_account_usd_balance_decreases_after_a_deposit(accounts, usd, potato, simple_chef):
    account_usd_balance = usd.balanceOf(accounts[0])
    usd.approve(simple_chef.address, 1, {'from': accounts[0]})
    simple_chef.deposit(1, {'from': accounts[0]})
    assert usd.balanceOf(accounts[0]) < account_usd_balance


def test_account_usd_balance_increases_after_a_withdraw(accounts, usd, potato, simple_chef):
    
    usd.approve(simple_chef.address, usd.balanceOf(accounts[0]), {'from': accounts[0]})
    simple_chef.deposit(usd.balanceOf(accounts[0]), {'from': accounts[0]})
    account_usd_balance_after_deposit = usd.balanceOf(accounts[0])
    account_usd_staked_balance = simple_chef.stakingBalance(accounts[0])
    t = simple_chef.withdraw(account_usd_staked_balance, {'from': accounts[0]})
    account_usd_balance_after_withdraw = usd.balanceOf(accounts[0])

    assert account_usd_balance_after_withdraw > account_usd_balance_after_deposit



def test_simple_chef_mints_more_potatos_after_deposits(accounts, usd, potato, simple_chef):
    start_block = simple_chef.startBlock.call()
    potato_total_supply = potato.totalSupply.call()
    usd.approve(simple_chef.address, 1e24, {'from': accounts[0]})

    simple_chef.deposit(1, {'from': accounts[0]})
    simple_chef.deposit(1, {'from': accounts[0]})

    assert potato_total_supply < potato.totalSupply.call()


def test_simple_chef_mints_more_potatos_after_withdraws(accounts, usd, potato, simple_chef):
    start_block = simple_chef.startBlock.call()
    potato_total_supply = potato.totalSupply.call()
    usd.approve(simple_chef.address, 1e24, {'from': accounts[0]})

    simple_chef.deposit(1, {'from': accounts[0]})
    simple_chef.withdraw(1, {'from': accounts[0]})

    assert potato_total_supply < potato.totalSupply.call()


def test_simple_chef_admin_updates_potato_per_block(accounts, usd, potato, simple_chef):
    potato_per_block_before_update = simple_chef.potatoPerBlock.call()
    simple_chef.updatePotatoPerBlock(1e24, {'from': accounts[0]})
    potato_per_block_after_update = simple_chef.potatoPerBlock.call()

    assert potato_per_block_after_update > potato_per_block_before_update


def test_only_the_simple_chef_admin_can_update_potato_per_block(accounts, usd, potato, simple_chef):
    with brownie.reverts():
        simple_chef.updatePotatoPerBlock(1e24, {'from': accounts[1]})
