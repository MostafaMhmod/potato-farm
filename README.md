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

5. Run the deployment script against the Ropsten testnet

    ```bash
    brownie run deployment --network ropsten
    ```
## License

This project is licensed under the [MIT license](LICENSE).
