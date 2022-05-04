from forta_agent import Finding, FindingType, FindingSeverity

LAST_BLOCK = [0]
GAS_CHECK = []

def handle_transaction(transaction_event):
    findings = []
    
    if len(GAS_CHECK) > 0:
        last_block_highest = max(GAS_CHECK)
        gas_now = transaction_event.gas_price/10**9
        if gas_now > last_block_highest+(last_block_highest*50/100):
            findings.append(Finding({
                'name': "Tremendous increase in gas price",
                'description': f'The increase in gas price is {(gas_now-last_block_highest)/last_block_highest*100:.2f}% greater than the previous block.',
                'alert_id': "GAS-DETECT-TCD",
                'severity': FindingSeverity.Info,
                'type': FindingType.Suspicious,
                'metadata': {
                    'block_number': transaction_event.block_number,
                    'tx_hash': transaction_event.hash,
                    'highest_gas_previous_block': last_block_highest,
                    'gas_price': gas_now,
                    'percentage': f'{(gas_now-last_block_highest)/last_block_highest:.2f}'
                }
            }))
            
    if transaction_event.block.number > LAST_BLOCK[0]:
        LAST_BLOCK[0] = transaction_event.block.number
        GAS_CHECK.clear()
    else:
        GAS_CHECK.append(transaction_event.gas_price/10**9)
        
    return findings