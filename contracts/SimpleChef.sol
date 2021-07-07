pragma solidity ^0.5.0;

import "./Potato.sol";
import "./Usd.sol";

contract SimpleChef {
    address public admin;
    Potato public potato;
    Usd public usd;

    uint256 public startBlock;
    uint256 public lastRewardBlock;
    uint256 public potatoPerBlock;
    uint256 public accPotatoPerShare;


    address[] public stakers;
    mapping(address => uint256) public stakingBalance;
    mapping(address => uint256) public UserRewardDept;
    mapping(address => bool) public hasStaked;
    mapping(address => bool) public isStaking;

    constructor(Potato _potato, Usd _usd) public {
        potato = _potato;
        usd = _usd;
        startBlock = block.number;
        admin = msg.sender;
    }

    // Return reward multiplier over the given _from to _to block.
    function getMultiplier(uint256 _from, uint256 _to) public view returns (uint256) {
        return _to.sub(_from);
    }

    function update() {
        if (block.number <= lastRewardBlock) {
            return;
        }
        uint256 usdBalance = usd.balanceOf(address(this));
        if (usdBalance == 0) {
            lastRewardBlock = block.number;
            return;
        }
        uint256 multiplier = getMultiplier(lastRewardBlock, block.number);
        uint256 reward = multiplier.mul(potatoPerBlock);
        potato.mint(address(this), reward);
        accPotatoPerShare = accPotatoPerShare.add(reward.mul(1e12).div(usdBalance));
        lastRewardBlock = block.number;
    }

    function deposit(uint256 _amount) public {
        update();
        userBalance = stakingBalance[msg.sender];
        if (userBalance > 0) {
            uint256 pending = userBalance.mul(accPotatoPerShare).div(1e12).sub(UserRewardDept[msg.sender]);
            if(pending > 0) {
                safePotatoTransfer(msg.sender, pending);
            }
        }
        if(_amount > 0) {
            usd.transferFrom(address(msg.sender), address(this), _amount);
            stakingBalance[msg.sender] = userBalance.add(_amount);
            
            // Add user to stakers array *only* if they haven't staked already
            if (!hasStaked[msg.sender]) {
                stakers.push(msg.sender);
            }

            // Update staking status
            isStaking[msg.sender] = true;
            hasStaked[msg.sender] = true;
        }
        UserRewardDept[msg.sender] = userBalance.mul(accPotatoPerShare).div(1e12);
        emit Deposit(msg.sender, _amount);

    }

    // Safe potato transfer function, just in case if rounding error causes pool to not have enough potatos.
    function safePotatoTransfer(address _to, uint256 _amount) internal {
        uint256 potatoBal = potato.balanceOf(address(this));
        if (_amount > potatoBal) {
            potato.transfer(_to, potatoBal);
        } else {
            potato.transfer(_to, _amount);
        }
    }


}
