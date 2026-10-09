import hashlib
import json
import datetime

def hash_blok(block: dict) -> str:
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def valid_proof(self, previous_proof, proof):
        h = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
        return h.startswith("0" * self.difficulty)

    def mine_block(self):
        prev = self.chain[-1]
        proof = 1
        while not self.valid_proof(prev["proof"], proof):
            proof += 1
        return self.create_block(proof, self.hash(prev))

    def hash(self, block: dict) -> str:
        return hash_blok(block)

    def add_transaction(self, sender, recipient, amount):
        if not sender or not isinstance(sender, str) or not sender.strip():
            raise ValueError("Sender tidak valid")
        if not recipient or not isinstance(recipient, str) or not recipient.strip():
            raise ValueError("Recipient tidak valid")
        if sender == recipient:
            raise ValueError("Sender dan Recipient tidak boleh sama")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount tidak valid")
        
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return len(self.chain) + 1

    def riwayat(self, user: str) -> list:
        hasil = []
        for blok in self.chain:
            for tx in blok.get("transactions", []):
                if tx["sender"] == user or tx["recipient"] == user:
                    hasil.append((blok["index"], tx))
        return hasil
