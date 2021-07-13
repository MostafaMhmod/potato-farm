# Potato-Farm

A simpler implementation of the well known [MasterChef](https://github.com/sushiswap/sushiswap/blob/canary/contracts/MasterChef.sol) contract, written in [Solidity](https://github.com/ethereum/solidity).

## deployment

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already.

2. Clone the Repo 
    ```bash
    git clone https://github.com/MostafaMhmod/potato-farm.git
    ```


3. Run the tests

    ```bash
    brownie test
    ```
4. Add your own private key to the brownie account variable and here it assumes its named `testing`

    ```bash
    brownie accounts new testing
    ```
5. Add your RPC key (infura in our case):
    ```bash
    export WEB3_INFURA_PROJECT_ID=YOUR KEY
    ```
6. Add your Etherscan API key for contract verfication:
    ```bash
    export ETHERSCAN_TOKEN=YOUR KEY
    ```
5. Run the deployment script to the Ropsten testnet (the only one supported by the script so far)

    ```bash
    brownie run deployment --network ropsten
    ```
## License

This project is licensed under the [MIT license](LICENSE).
