# Gas Price Monitoring

## Description

This agency monitors all transactions on Ethereum to detect unusual gas prices by comparing from previous blocks.

## Supported Chains

- Ethereum

## Alerts

An alarm is triggered if a transaction uses a gas price greater than 50% with the maximum gas cost in the previous block.

## Test Data

```
1 findings for transaction 0x3745b8a8746d95ba269bce36c7969080b41432f5e70ef8e62de6140bcdda29c1 {
  "name": "Tremendous increase in gas price",
  "description": "The increase in gas price is 129.23% greater than the previous block.",
  "alertId": "GAS-DETECT-TCD",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Suspicious",
  "metadata": {
    "block_number": 14709884,
    "tx_hash": "0x3745b8a8746d95ba269bce36c7969080b41432f5e70ef8e62de6140bcdda29c1",
    "highest_gas_previous_block": 52.349632969,
    "gas_price": 120,
    "percentage": "1.29"
  },
  "addresses": []
}
```

```
1 findings for transaction 0x19bfd78cacf29847ebf34d5c8fd52e7cefc84465e929aca842fb27f528ec5ab4 {
  "name": "Tremendous increase in gas price",
  "description": "The increase in gas price is 108.60% greater than the previous block.",
  "alertId": "GAS-DETECT-TCD",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Suspicious",
  "metadata": {
    "block_number": 14709884,
    "tx_hash": "0x19bfd78cacf29847ebf34d5c8fd52e7cefc84465e929aca842fb27f528ec5ab4",
    "highest_gas_previous_block": 120,
    "gas_price": 250.323189286,
    "percentage": "1.09"
  },
  "addresses": []
}
```
