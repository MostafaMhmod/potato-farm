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

}
