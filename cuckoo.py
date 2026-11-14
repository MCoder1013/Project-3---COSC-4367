
import random


class CuckooHashTable:
    def __init__(self, size=11, max_kicks=20):
        self.size = size
        self.max_kicks = max_kicks

        # Two separate hash tables
        self.table1 = [None] * size
        self.table2 = [None] * size

        # Two hash functions with randomized parameters
        self.a1 = random.randint(1, 1000)
        self.a2 = random.randint(1, 1000)

        self.count = 0

    def hash1(self, key):
        return (key * self.a1) % self.size

    def hash2(self, key):
        return (key * self.a2 + 1) % self.size

    def lookup(self, key):
        """Lookups check at most two cells."""
        i = self.hash1(key)
        j = self.hash2(key)

        return (
            self.table1[i] == key
            or self.table2[j] == key
        )

    def insert(self, key):
        """Insert a key using cuckoo displacement."""
        if self.lookup(key):
            return True

        current = key
        table_number = 1

        for _ in range(self.max_kicks):
            if table_number == 1:
                index = self.hash1(current)

                if self.table1[index] is None:
                    self.table1[index] = current
                    self.count += 1
                    return True

                # Kick out the existing key
                self.table1[index], current = (
                    current, self.table1[index]
                )
                table_number = 2

            else:
                index = self.hash2(current)

                if self.table2[index] is None:
                    self.table2[index] = current
                    self.count += 1
                    return True

                # Kick out the existing key
                self.table2[index], current = (
                    current, self.table2[index]
                )
                table_number = 1

        # For now, detect failure rather than rehash.
        # The table may have been changed by the kick-outs,
        # so it needs rebuilding before further use.
        raise RuntimeError(
            "Insertion failed: relocation limit reached. "
            "Rehashing will be implemented next."
        )

    def load_factor(self):
        return self.count / (2 * self.size)

    def display(self):
        print("Table 1:", self.table1)
        print("Table 2:", self.table2)
        print("Load factor:", round(self.load_factor(), 3))
