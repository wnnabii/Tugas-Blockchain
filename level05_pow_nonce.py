import hashlib
import json
import datetime

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []
        genesis = {
            "index": 0,
            "timestamp": str(datetime.datetime.now()),
            "transactions": [],
            "previous_hash": "0",
        }
        self.proof_of_work(genesis)
        self.chain.append(genesis)

    @staticmethod
    def hash_block(block: dict) -> str:
        b = block.copy()
        b.pop("hash", None)
        return hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()

    def proof_of_work(self, block: dict) -> int:
        nonce = 0
        while True:
            block["nonce"] = nonce
            h = self.hash_block(block)
            if h.startswith("0" * self.difficulty):
                block["hash"] = h
                return nonce + 1
            nonce += 1

    def new_block(self, transactions):
        prev = self.chain[-1]
        block = {
            "index": len(self.chain),
            "timestamp": str(datetime.datetime.now()),
            "transactions": transactions,
            "previous_hash": prev["hash"],
        }
        self.proof_of_work(block)
        self.chain.append(block)
        return block

    def chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr["previous_hash"] != prev["hash"]:
                return False
            
        for curr in self.chain:
            if curr.get("hash") != self.hash_block(curr):
                return False
            if not curr.get("hash", "").startswith("0" * self.difficulty):
                return False
                
        return True

    def tambang_ulang_dari(self, index: int) -> int:
        usaha_total = 0
        for i in range(index, len(self.chain)):
            if i > 0:
                self.chain[i]["previous_hash"] = self.chain[i - 1]["hash"]
            usaha_total += self.proof_of_work(self.chain[i])
        return usaha_total
