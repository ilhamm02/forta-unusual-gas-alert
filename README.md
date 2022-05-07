# Gas Price Monitoring

## Description

This agency monitors all transactions on Ethereum to detect unusual gas prices by comparing from previous blocks. This bot is live on Forta with agent hash `0x0d37655e02536081721672ce27fecb6d26754bf63597aa5c9d024a1bdf0e3a82`

## Supported Chains

- Ethereum

## Alerts

- GAS-DETECT-TCD
  - Works if bot received more than 5 blocks
  - Triggered when a transaction has a `gas_price` exceeding more than 50% of the highest `gas_price` in the previous block.
  - Type is always Suspicious
  - Severity level depends on the percentage of the current `gas_price` with the previous block.
    - Low if the rise percentage of the transaction more than 50% from the previous block or 1.3x from the increase in gas in the previous 2 blocks
    - Medium if the rise percentage of the transaction more than 150% from the previous block or 1.7x from the increase in gas in the previous 2 blocks
    - Low if the rise percentage of the transaction more than 200% from the previous block or 2x from the increase in gas in the previous 2 blocks
  - Metadata value:
    - `block_number` is the block number of the transaction
    - `tx_hash` is the hash of the transaction
    - `from` is the sender of the transaction
    - `gas_price` is the gas price of the transaction in GWEI

## Test
Testing is done by letting the bot run and getting 2 blocks as reference data

## Test Data
```
1 findings for transaction 0x827cf75f6996afb2765326dc35e2d2dd4303d9e0b9b20d78c6d764c0070f65bb {
  "name": "Tremendous increase in gas price",
  "description": "A large increase in gas prices from the previous block.",
  "alertId": "GAS-DETECT-TCD",
  "protocol": "ethereum",
  "severity": "Low",
  "type": "Suspicious",
  "metadata": {
    "block_number": 14729988,
    "tx_hash": "0x827cf75f6996afb2765326dc35e2d2dd4303d9e0b9b20d78c6d764c0070f65bb",
    "from": "0x1938a448d105d26c40a52a1bfe99b8ca7a745ad0",
    "gas_price": 120.62
  },
  "addresses": [
    "0x1938a448d105d26c40a52a1bfe99b8ca7a745ad0",
    "0xc18360217d8f7ab5e7c516566761ea12ce7f9d72"
  ]
}
```
```
1 findings for transaction 0xc7f43c970398674f35eafc26df1944d8082e265acafd670be85b95c41f974633 {
  "name": "Tremendous increase in gas price",
  "description": "A large increase in gas prices from the previous block.",
  "alertId": "GAS-DETECT-TCD",
  "protocol": "ethereum",
  "severity": "High",
  "type": "Suspicious",
  "metadata": {
    "block_number": 14729988,
    "tx_hash": "0xc7f43c970398674f35eafc26df1944d8082e265acafd670be85b95c41f974633",
    "from": "0x26bce6ecb5b10138e4bf14ac0ffcc8727fef3b2e",
    "gas_price": 1215.31
  },
  "addresses": [
    "0x26bce6ecb5b10138e4bf14ac0ffcc8727fef3b2e",
    "0x4cb18386e5d1f34dc6eea834bf3534a970a3f8e7"
  ]
}
```
