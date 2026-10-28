"""Hand-written data structures: linked list, stack, queue, BST, graph (BFS)."""
import csv, os
from collections import deque

class Node:
    def __init__(s, d): s.d, s.next = d, None

class LinkedList:
    def __init__(s): s.head = None
    def insert(s, d):
        n = Node(d); n.next = s.head; s.head = n
    def delete(s, pred):
        p, c = None, s.head
        while c:
            if pred(c.d):
                if p: p.next = c.next
                else: s.head = c.next
                return True
            p, c = c, c.next
        return False
    def traverse(s):
        c = s.head
        while c: yield c.d; c = c.next

class Stack(LinkedList):          # undo history of grading corrections
    push = LinkedList.insert
    def pop(s):
        if not s.head: return None
        d = s.head.d; s.head = s.head.next; return d

class Queue:                      # FIFO order of samples awaiting testing
    def __init__(s): s.head = s.tail = None
    def enqueue(s, d):
        n = Node(d)
        if s.tail: s.tail.next = n
        else: s.head = n
        s.tail = n
    def dequeue(s):
        if not s.head: return None
        d = s.head.d; s.head = s.head.next
        if not s.head: s.tail = None
        return d

class BST:                        # grade classifier keyed by score threshold
    def __init__(s): s.root = None
    def insert(s, k, v):
        def ins(n):
            if not n: return [k, v, None, None]
            if k < n[0]: n[2] = ins(n[2])
            else: n[3] = ins(n[3])
            return n
        s.root = ins(s.root)
    def floor(s, x):              # largest key <= x
        n, best = s.root, None
        while n:
            if n[0] <= x: best, n = n, n[3]
            else: n = n[2]
        return best[1] if best else "Reject"
    def inorder(s, n="root"):
        n = s.root if n == "root" else n
        if n: yield from s.inorder(n[2]); yield n[:2]; yield from s.inorder(n[3])

GRADES = BST()
for k, v in [(0, "Reject"), (50, "C"), (70, "B"), (85, "A")]: GRADES.insert(k, v)

def load_chain(path=os.path.join(os.path.dirname(__file__), "data", "edges.csv")):
    g = {}
    for r in csv.DictReader(open(path)):
        g.setdefault(r["from"], []).append(r["to"]); g.setdefault(r["to"], [])
    return g

CHAIN = load_chain()   # supply-chain graph as adjacency list (data/edges.csv)
def bfs_path(a, b):
    q, seen = deque([[a]]), {a}
    while q:
        p = q.popleft()
        if p[-1] == b: return p
        for n in CHAIN.get(p[-1], []):
            if n not in seen: seen.add(n); q.append(p + [n])
    return None
