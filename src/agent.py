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
                'name': "Tremendous increase in gas costs",
                'description': f'The increase in gas costs is {(gas_now-last_block_highest)/last_block_highest*100}% greater than the previous block. Last block highest gas price is {last_block_highest} GWEI, gas price this tx is {gas_now} GWEI',
                'alert_id': "GAS-DETECT-TCD",
                'severity': FindingSeverity.Info,
                'type': FindingType.Suspicious,
            }))
            
    if transaction_event.block.number > LAST_BLOCK[0]:
        LAST_BLOCK[0] = transaction_event.block.number
        GAS_CHECK.clear()
    else:
        GAS_CHECK.append(transaction_event.gas_price/10**9)
        
    return findings