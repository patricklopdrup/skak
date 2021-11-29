

class TranspositionTable:
    EXACT = 1
    LOWERBOUND = 2
    UPPERBOUND = 3

    depth = 0
    flag = 0
    value = 0

    # The transposition table (hash table)
    table = {}

    def add_to_table(self, hash, table_entry):
        self.table[hash] = table_entry