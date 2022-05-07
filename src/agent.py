import math, statistics
from forta_agent import Finding, FindingType, FindingSeverity

BLOCK_LIMIT = 2 # total blocks to be stored as reference data

GAS_HISTORY = [] # data history as much as BLOCK_LIMIT+1 for the current block
SAVE_DATA = [] # temporary data storage if an alarm is triggered and will be filtered again to be re-entered into GAS_HISTORY each time there is a new block
HIGHEST_GAS_LIST = [] # storage for the highest gas list in each block in GAS_HISTORY

def handle_block(block_event):
    findings = []
    
    block_number = block_event.block_number # the current block number
    total_transactions = len(block_event.block.transactions) # total transactions in current block
    
    if len(GAS_HISTORY) == 0:
        GAS_HISTORY.append({
            'block_number': block_number,
            'total_transactions': total_transactions,
            'gas_price': []
        }) # add data into GAS_HISTORY
    else:
        if block_number > GAS_HISTORY[-1]["block_number"]: # conditions to check if a new block has been mined 
            insert_save_data() # filter data SAVE_DATA to put in GAS_HISTORY
            update_highest_gas() # updated highest gas list on HIGHEST_GAS_LIST based on GAS_HISTORY data
            GAS_HISTORY.append({
                'block_number': block_number,
                'total_transactions': total_transactions,
                'gas_price': []
            }) # add data into GAS_HISTORY
    
    while len(GAS_HISTORY) > BLOCK_LIMIT+1: # delete data block that exceeds BLOCK_LIMIT + 1 for the current block
        del GAS_HISTORY[0] # deleting oldest block
        
    return findings

def handle_transaction(transaction_event):
    findings = []
    
    if len(GAS_HISTORY) > 0 and transaction_event.block_number <= GAS_HISTORY[-1]["block_number"] and transaction_event.block_number >= GAS_HISTORY[0]["block_number"]: # checks whether GAS_HISTORY has been filled from handle_block to start checking each transaction
        gas_now = float(f'{transaction_event.gas_price/10**9:.2f}') # convert gas price to GWEI
        block_number = transaction_event.block_number # block number of transaction
        
        if len(GAS_HISTORY) > 2: # checking if the data block in GAS_HISTORY is more than 2 as a benchmark to start detection
            MIN_PERCENTAGE = 50 # default tolerance increase from previous block
            if HIGHEST_GAS_LIST[-1] > HIGHEST_GAS_LIST[-2]: # check if in the previous 2 blocks there was the highest increase in gas price
                prev_rise_percentage = HIGHEST_GAS_LIST[-1] - HIGHEST_GAS_LIST[-2]/HIGHEST_GAS_LIST[-1]*100 # the highest percentage increase in gas price in the previous 2 blocks
                if prev_rise_percentage > 50: # if the highest increase in gas in the previous 2 block transactions with the previous 1 block exceeding the tolerance, it will be used as a tolerance benchmark
                    MIN_PERCENTAGE = prev_rise_percentage
            
            if gas_now > HIGHEST_GAS_LIST[-1]: # checking if this transaction has gas_price higher than previous block
                rise_percentage = gas_now - HIGHEST_GAS_LIST[-1]/gas_now*100 # the percentage increase in gas price on this transaction with the previous block
                if rise_percentage > MIN_PERCENTAGE: # checking if rise_percentage is higher than prev_rise_percentage, if so alarm is triggered
                    addresses = [] 
                    for address in transaction_event.addresses: # collectiong addresses on transaction
                        addresses.append(address)
                        
                    findings.append(Finding({
                        'name': "Tremendous increase in gas price",
                        'description': f'A large increase in gas prices from the previous block.',
                        'alert_id': "GAS-DETECT-TCD",
                        'type': FindingType.Suspicious,
                        'severity': get_severity(rise_percentage, MIN_PERCENTAGE), # get severity level by rise_percentage and the tolerance pencentage
                        'metadata': {
                            'block_number': block_number,
                            'tx_hash': transaction_event.hash,
                            'from': transaction_event.from_,
                            'gas_price': gas_now
                        },
                        'addresses': addresses
                    }))
                    
        if len(findings) == 0: # checking if alarm is not triggered for this transaction
            block_index = 0
            while GAS_HISTORY[block_index]["block_number"] != block_number: # searching the match block_number with GAS_HISTORY
                block_index += 1
                
            GAS_HISTORY[block_index]["gas_price"].append(gas_now) # add gas_price to GAS_HISTORY
        else: # checking if alarm is triggered for this transaction
            SAVE_DATA.append({
                'block_number': block_number,
                'gas_price': gas_now
            }) # store gas_price on this transaction for benchmark accuracy on the block in this transaction and will be filtered to enter GAS_HISTORY
        
    return findings

def update_highest_gas(): # function for update the HIGHEST_GaS_LIST
    HIGHEST_GAS_LIST.clear() # clearing all list for the data accuracy
    
    for lists in GAS_HISTORY: # getting all block data
        if len(lists["gas_price"]) > 0:
            gas_list = []
            for gas in lists["gas_price"]:
                gas_list.append(math.ceil(gas/10)*10) # the data is converted into multiples of 10 as a benchmark and tolerance
                
            HIGHEST_GAS_LIST.append(max(gas_list)) # add data to HIGHEST_GAS_LIST
        
def insert_save_data(): # function for move and filtering SAVE_DATA to GAS_HISTORY
    temp_data = []
    if len(SAVE_DATA) > 0: # checking the length of SAVE_DATA
        for data in SAVE_DATA:
            if data["block_number"] == GAS_HISTORY[-1]["block_number"]: # checking the block_number to anticipate data crashing 
                temp_gas = data["gas_price"] 
                if data["gas_price"] < 1000: # checking if block is not clogging
                    temp_gas = math.floor(data["gas_price"]/50)
                else: # checking if block is block clogging
                    temp_gas = math.floor(data["gas_price"]/100) # tolerance in multiples of 100
                temp_data.append(temp_gas)
                
        temp_mode = statistics.mean(temp_data) # the mean of SAVE_DATA which has been tolerated as a benchmark for filtering to GAS_HISTORY
        data_index = 0
        
        for data in temp_data:
            if data <= temp_mode: # checking if SAVE_DATA value less than temp_mode 
                GAS_HISTORY[-1]["gas_price"].append(GAS_HISTORY[-1]["gas_price"][data_index]) # move to GAS_HISTORY
    
    SAVE_DATA.clear()
        
def get_severity(rise_percentage, min_percentage):
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
        if rise_percentage > min_percentage*1.7:
            severity = FindingSeverity.Medium
        if rise_percentage > min_percentage*2:
            severity = FindingSeverity.High
    
    return severity