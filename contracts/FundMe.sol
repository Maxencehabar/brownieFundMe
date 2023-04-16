// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    mapping(address => uint256) public money;
    address public owner;
    AggregatorV3Interface public priceFeed;
    event String(string message);
    event Address(address addr);

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimum = 50; // 50 wei
        require(msg.value >= minimum, "Not enough sent");
        money[address(msg.sender)] += msg.value;
    }

    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }

    function getUserBalance() public view returns (uint) {
        return money[address(msg.sender)];
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        return (minimumUSD * precision) / price;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getDescription() public view returns (string memory) {
        return priceFeed.description();
    }

    function getEthAmountToUSD(uint256 amount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethPrice * amount) / 1000000000000000000;
        return ethAmountInUSD;
    }

    modifier OnlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable {
        emit Address(msg.sender);
        require(msg.sender == owner, "You're not allowed to withdraw");

        payable(msg.sender).transfer(money[msg.sender]);
        money[msg.sender] = 0;
    }
}
