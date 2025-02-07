// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Oracle {
    uint256 private value;

    // Constructor to initialize the oracle with a non-zero value
    constructor(uint256 _initialValue) {
        value = _initialValue;
    }

    function getValue() public view returns (uint256) {
        return value;
    }

    function updateValue(uint256 newValue) public {
        value = newValue;
    }
}
