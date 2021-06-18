from utils import MAX_WEIGHT, parse_csv, read_block, ifValidBlock


mempool = parse_csv()


transactions = [tx for tx in mempool.values()]

# maps a transaction to all its children
children = {}
for tx in mempool.keys():
    children[tx] = []
for tx in transactions:
    tx_id = tx["tx_id"]
    parents = tx["parents"]
    for parent in parents:
        children[parent].append(tx_id)

# checks if transaction is added to the block
isAddedInBlock = {}
for tx in transactions:
    isAddedInBlock[tx["tx_id"]] = False

# check if all parents of a transaction are already in the block
isValidChild = {}
for tx in transactions:
    tx_id = tx["tx_id"]
    if(len(tx["parents"]) == 0):
        isValidChild[tx_id] = True
    else:
        isValidChild[tx_id] = False

# Greedily creating a block of transactions
total_weight = 0
total_fees = 0
block = []
sorted_transactions = sorted(
    transactions, key=lambda tx: int(tx["weight"])/int(tx["fees"]))


def addTx(tx, i):
    tx_id = tx["tx_id"]
    fees = int(tx["fees"])
    weight = int(tx["weight"])
    if(isAddedInBlock[tx_id]):
        return

    if(isValidChild[tx_id]):
        global total_weight, total_fees
        if(total_weight + weight > MAX_WEIGHT):
            return
        block.append(tx_id)
        total_fees += fees
        total_weight += weight
        isAddedInBlock[tx_id] = True

        # checking if any child of newly appended transaction is now a valid child
        for child_id in children[tx_id]:
            tx_child = mempool[child_id]
            child_parents = tx_child["parents"]
            flag = 1
            for child_parent in child_parents:
                if(not isAddedInBlock[child_parent]):
                    flag = 0
            if(flag):
                isValidChild[child_id] = True

        # checking if any of the previous ignored transaction could be added
        for j, newTx in enumerate(sorted_transactions[:i]):
            addTx(newTx, j)


for i, tx in enumerate(sorted_transactions):
    addTx(tx, i)


with open("block.txt", "w") as file:
    for tx in block:
        file.write(tx+'\n')

block_csv = read_block()
if(not ifValidBlock(mempool, block_csv)):
    print("Algo failed")
