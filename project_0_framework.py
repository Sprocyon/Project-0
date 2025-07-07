# Project 0 – A Framework for Decentralized, Honest Knowledge Accumulation

"""
Цей фреймворк – початковий кістяк системи, яка:
- накопичує знання,
- аналізує їх прозоро через дерево доказів,
- не прив'язана до авторитетів,
- доступна для всіх.
"""

from typing import List, Dict, Any, Optional
import hashlib
import datetime
import uuid

# ============================
# 🧠 Блок 1: Структура знань
# ============================

class KnowledgeEntry:
    def __init__(self, content: str, source: str, tags: List[str]):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.content = content
        self.source = source
        self.tags = tags
        self.fingerprint = self.compute_fingerprint()

    def compute_fingerprint(self) -> str:
        return hashlib.sha256((self.content + self.source).encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "content": self.content,
            "source": self.source,
            "tags": self.tags,
            "fingerprint": self.fingerprint
        }

# ============================
# 🌳 Блок 2: Дерево доказів
# ============================

class ProofNode:
    def __init__(self, claim: str, source: str, proof_type: str):
        self.id = str(uuid.uuid4())
        self.claim = claim
        self.source = source
        self.proof_type = proof_type  # e.g., "observation", "experiment", "text", "tradition"
        self.children: List[ProofNode] = []
        self.created = datetime.datetime.utcnow().isoformat()

    def add_child(self, node: 'ProofNode'):
        self.children.append(node)

    def evaluate_strength(self) -> float:
        base = 1.0
        weight_map = {
            "experiment": 1.0,
            "observation": 0.8,
            "text": 0.6,
            "tradition": 0.4,
            "opinion": 0.2
        }
        base *= weight_map.get(self.proof_type, 0.1)
        base += sum(child.evaluate_strength() for child in self.children) * 0.5
        return round(base, 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "claim": self.claim,
            "source": self.source,
            "proof_type": self.proof_type,
            "created": self.created,
            "strength": self.evaluate_strength(),
            "children": [child.to_dict() for child in self.children]
        }

# ============================
# 📊 Блок 3: Зберігання та пошук знань
# ============================

class KnowledgeBase:
    def __init__(self):
        self.entries: Dict[str, KnowledgeEntry] = {}

    def add_entry(self, entry: KnowledgeEntry):
        if entry.fingerprint not in self.entries:
            self.entries[entry.fingerprint] = entry

    def search_by_tag(self, tag: str) -> List[KnowledgeEntry]:
        return [e for e in self.entries.values() if tag in e.tags]

    def all_entries(self) -> List[KnowledgeEntry]:
        return list(self.entries.values())

# ============================
# 🔓 Блок 4: Демонстрація роботи
# ============================

if __name__ == "__main__":
    kb = KnowledgeBase()

    e1 = KnowledgeEntry(
        content="Water boils at 100°C at 1 atm pressure.",
        source="wikipedia.org",
        tags=["science", "physics"]
    )

    e2 = KnowledgeEntry(
        content="Some say ancient civilizations had unknown technologies.",
        source="user_submission",
        tags=["history", "alternative"]
    )

    kb.add_entry(e1)
    kb.add_entry(e2)

    print("\n📚 Stored Knowledge Entries:")
    for entry in kb.all_entries():
        print("[{}] {}".format(entry.id, entry.content))

    print("\n🌳 Example: Tree of Proof")
    root = ProofNode("The Earth is round", "textbook", "text")
    child1 = ProofNode("Satellite imagery shows curvature", "nasa.gov", "observation")
    child2 = ProofNode("Circumnavigation is possible", "historical records", "tradition")

    root.add_child(child1)
    root.add_child(child2)

    print(root.to_dict())
