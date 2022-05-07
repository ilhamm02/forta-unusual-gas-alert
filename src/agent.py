import math, statistics
from turtle import clear
from forta_agent import Finding, FindingType, FindingSeverity

BLOCK_LIMIT = 2

GAS_HISTORY = []
SAVE_DATA = []
HIGHEST_GAS_LIST = []

test = []

def handle_block(block_event):
    findings = []
    
    block_number = block_event.block_number
    total_transactions = len(block_event.block.transactions)
    
    if len(GAS_HISTORY) == 0:
        GAS_HISTORY.append({
            'block_number': block_number,
            'total_transactions': total_transactions,
            'gas_price': []
        })
    else:
        if block_number > GAS_HISTORY[-1]["block_number"]:
            insert_save_data()
            update_highest_gas()
            GAS_HISTORY.append({
                'block_number': block_number,
                'total_transactions': total_transactions,
                'gas_price': []
            })
    
    while len(GAS_HISTORY) > BLOCK_LIMIT+1:
        del GAS_HISTORY[0]

    print(test)
    return findings

def handle_transaction(transaction_event):
    findings = []
    
    if len(GAS_HISTORY) > 0 and transaction_event.block_number <= GAS_HISTORY[-1]["block_number"] and transaction_event.block_number >= GAS_HISTORY[0]["block_number"]:
        gas_now = float(f'{transaction_event.gas_price/10**9:.2f}')
        block_number = transaction_event.block_number
        
        if len(GAS_HISTORY) > 2:
            MIN_PERCENTAGE = 50
            if HIGHEST_GAS_LIST[-1] > HIGHEST_GAS_LIST[-2]:
                prev_rise_percentage = HIGHEST_GAS_LIST[-1] - HIGHEST_GAS_LIST[-2]/HIGHEST_GAS_LIST[-1]*100
                if prev_rise_percentage > 50:
                    MIN_PERCENTAGE = prev_rise_percentage
            
            if gas_now > HIGHEST_GAS_LIST[-1]:
                rise_percentage = gas_now - HIGHEST_GAS_LIST[-1]/gas_now*100
                if rise_percentage > MIN_PERCENTAGE:
                    findings.append(Finding({
                        'name': "Tremendous increase in gas price",
                        'description': f'A large increase in gas prices from the previous block.',
                        'alert_id': "GAS-DETECT-TCD",
                        'type': FindingType.Suspicious,
                        'severity': get_severity(gas_now, rise_percentage, MIN_PERCENTAGE),
                        'metadata': {
                            'block_number': block_number,
                            'tx_hash': transaction_event.hash,
                            'from': transaction_event.from_,
                            'gas_price': gas_now
                        },
                        'addresses': [
                            transaction_event.from_,
                            transaction_event.to
                        ]
                    }))
                    
                    test.append(transaction_event.hash)
                    
        if len(findings) == 0:
            block_index = 0
            while GAS_HISTORY[block_index]["block_number"] != block_number:
                block_index += 1
                
            GAS_HISTORY[block_index]["gas_price"].append(gas_now)
        else: 
            SAVE_DATA.append({
                'block_number': block_number,
                'gas_price': gas_now
            })
        
    return findings

def update_highest_gas():
    HIGHEST_GAS_LIST.clear()
    
    for lists in GAS_HISTORY:
        gas_list = []
        for gas in lists["gas_price"]:
            gas_list.append(math.ceil(gas/10)*10)
        HIGHEST_GAS_LIST.append(max(gas_list))
        
def insert_save_data():
    temp_data = []
    if len(SAVE_DATA) > 0:
        for data in SAVE_DATA:
            if data["block_number"] == GAS_HISTORY[-1]["block_number"]:
                temp_gas = data["gas_price"]
                if data["gas_price"] < 1000:
                    temp_gas = math.floor(data["gas_price"]/50)
                else:
                    temp_gas = math.floor(data["gas_price"]/100)
                temp_data.append(temp_gas)
        
        temp_mode = statistics.mode(temp_data)
        
        for data in temp_data:
            GAS_HISTORY[-1]["gas_price"].append(data)
            
        
def get_severity(gas_now, rise_percentage, min_percentage):
    severity = FindingSeverity.Info
    if min_percentage < 100:
        if rise_percentage > min_percentage:
            severity = FindingSeverity.Low
        if rise_percentage > 150:
            severity = FindingSeverity.Medium
        if rise_percentage > 200:
            severity = FindingSeverity.High
    
    if min_percentage > 100:
        if rise_percentage > min_percentage*1.3:
            severity = FindingSeverity.Low
        if rise_percentage > min_percentage*7:
            severity = FindingSeverity.Medium
        if rise_percentage > min_percentage*2:
            severity = FindingSeverity.High
    
    return severity