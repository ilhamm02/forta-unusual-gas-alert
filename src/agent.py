import math, statistics
from forta_agent import Finding, FindingType, FindingSeverity

LIMIT_BLOCK = 10
BLOCK_START = 5

GAS_HISTORY = []
SAVE_DATA = []

def handle_transaction(transaction_event):
    findings = []
    
    gas_now = float(f'{transaction_event.gas_price/10**9:.2f}')
    block_number = transaction_event.block_number
    
    if len(GAS_HISTORY) == 0:
        GAS_HISTORY.append([[block_number, gas_now]])
    else:
        if GAS_HISTORY[-1][0][0] == block_number:
            GAS_HISTORY[-1].append([block_number, gas_now])
        else:
            insert_save_data()
            GAS_HISTORY.append([[block_number, gas_now]])
        
    while len(GAS_HISTORY) > LIMIT_BLOCK+1:
        del GAS_HISTORY[0]
        
    if len(GAS_HISTORY) > BLOCK_START:
        highest_gas_list = get_highest_gas()
        if gas_now > max(highest_gas_list[:-1])+(max(highest_gas_list[:-1])*50/100):
            findings.append(Finding({
                'name': "Tremendous increase in gas price",
                'description': f'A large increase in gas prices from the previous block..',
                'alert_id': "GAS-DETECT-TCD",
                'type': FindingType.Suspicious,
                'severity': get_severity(gas_now, highest_gas_list),
                'metadata': {
                    'block_number': transaction_event.block_number,
                    'tx_hash': transaction_event.hash,
                    'from': transaction_event.from_,
                    'gas_price': gas_now
                },
                'addresses': [
                    transaction_event.from_,
                    transaction_event.to
                ]
            }))
            
            SAVE_DATA.append(gas_now)
            
    return findings

def get_highest_gas():
    chart = []
    
    for lists in GAS_HISTORY:
        gas_list = []
        for gas in lists:
            gas_list.append(math.ceil(gas[1]/10)*10)
        chart.append(max(gas_list))
        
    return chart

def insert_save_data():
    temp_data = []
    if len(SAVE_DATA) > 0:
        block_number = GAS_HISTORY[-1][0][0]
        for data in SAVE_DATA:
            gas_price = data
            if data < 1000:
                gas_price = math.floor(data/50)
            else:
                gas_price = math.floor(data/100)
            temp_data.append(gas_price)
    
        temp_mode = statistics.mode(temp_data)
        count = 0
        
        for data in temp_data:
            if data > temp_mode:
                GAS_HISTORY[-1].append([block_number, SAVE_DATA[count]])
            count += 1
            
def get_severity(now, list):
    max_gas = max(list[:-1])
    print(max_gas)
    if now > max_gas+(max_gas*50/100):
        severity = FindingSeverity.Info
        if now > max_gas+(max_gas*70/100):
            severity = FindingSeverity.Low
        if now > max_gas+(max_gas*100/100):
            severity = FindingSeverity.Medium
        if now > max_gas+(max_gas*200/100):
            severity = FindingSeverity.High
        
    return severity