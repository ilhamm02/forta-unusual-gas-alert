# Gas Price Monitoring

## Description

This agency monitors all transactions on Ethereum to detect unusual gas prices by comparing from previous blocks. This bot is live on Forta with agent hash `0x563020223474e0b4d4219459335cddee627d729e7305d0195ebfded3ed190de3`

## Supported Chains

- Ethereum

## Alerts

- GAS-DETECT-TCD
  - Works if bot received more than 5 blocks
  - Triggered when a transaction has a `gas_price` exceeding 50% of the highest `gas_price` in the previous block.
  - Type is always Suspicious
  - Severity level depends on the percentage of the current `gas_price` with the previous block.
    - Info if the percentage is more than 50
    - Low if the percentage is more than 70
    - Medium is percentage is more than 100
    - Hight is percentage is more than 200
  - Metadata value:
    - `block_number` is the block number of the transaction
    - `tx_hash` is the hash of the transaction
    - `from` is the sender of the transaction
    - `gas_price` is the gas price of the transaction in GWEI

## Test
The test is done by letting the bot run and get the first 5 blocks and the bot can record all transactions in each block and give an alarm if needed.

## Test Data
```
{
  "name": "Tremendous increase in gas price",
  "description": "A large increase in gas prices from the previous block..",
  "alertId": "GAS-DETECT-TCD",
  "protocol": "ethereum",
  "severity": "High",
  "type": "Suspicious",
  "metadata": {
    "block_number": 14725879,
    "tx_hash": "0xa6d0b7aefeb8cfb508b5d1034f199682337eeac9353482ca212f74799a04e716",
    "from": "0x3462d4f128e214f09a5483ab2613fbf13cd4e57e",
    "gas_price": 777
  },
  "addresses": [
    "0x3462d4f128e214f09a5483ab2613fbf13cd4e57e",
    "0x59728544b08ab483533076417fbbb2fd0b17ce3a"
  ]
}
```

```
{
  "name": "Tremendous increase in gas price",
  "description": "A large increase in gas prices from the previous block..",
  "alert_id": "GAS-DETECT-TCD",
  "severity": "High",
  "type": "Suspicious",
  "metadata": {
    "block_number": 14725906,
    "tx_hash": "0xac86ea96140a9dcdb6dfca0341177dc216b102a9adb7ee93b8cbd373d94acbef",
    "from": "0xa08200ccf97b4dd994c6e2a08d117a4ac27260c1",
    "gas_price": 5000
  },
  "addresses": [
    "0xa08200ccf97b4dd994c6e2a08d117a4ac27260c1",
    "0x30bbdfd29b90a320a447875a75a5d32d23fa763b"
  ]
}
```
