MAX_WEIGHT = 4000000


def parse_csv():
    with open("mempool.csv", 'r') as file:
        next(file)      # ignoring first line
        mempool = {}
        for line in file.readlines():
            args = line.strip().split(',')
            tx_id = args[0]
            fees = args[1]
            weight = args[2]
            parents = args[3].split(';')
            if(parents[0] == ''):
                parents = []
            transaction = {
                "tx_id": tx_id,
                "fees": fees,
                "weight": weight,
                "parents": parents
            }
            mempool[tx_id] = transaction

        return mempool


def read_block():
    transactions = []
    with open("block.txt", "r") as file:
        for tx in file.readlines():
            transactions.append(tx.strip())
        return transactions


def ifValidBlock(mempool, blockTransactions):
    tx_included = {}
    for tx_id in mempool.keys():
        tx_included[tx_id] = False

    total_fees = 0
    total_weight = 0

    for tx_id in blockTransactions:
        if tx_id not in mempool:
            print("Transaction {} not in mempool".format(tx_id))
            return False

        transaction = mempool[tx_id]
        total_fees += int(transaction["fees"])
        total_weight += int(transaction["weight"])
        if(total_weight > MAX_WEIGHT):
            print("Weight of block exceeds required limit")
            return False

        parents = transaction["parents"]
        if(len(parents) > 0):
            for parent in parents:
                if(tx_included[parent] == False):
                    print(
                        "Parent {} of transaction {} not present in the block".format(parent, tx_id))
                    return False

        tx_included[tx_id] = True

    print("Block is correct with transaction fees {} satoshis, total weight {} and numer of transations is {}".format(
        total_fees, total_weight, len(blockTransactions)))
    return True
