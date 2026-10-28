import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ds import LinkedList, Stack, Queue, GRADES, bfs_path
from algos import quicksort, binsearch_ge, greedy_blend, dp_knapsack, backtrack_blend

def test_linked_list():
    l = LinkedList()
    for i in (1, 2, 3): l.insert(i)
    assert list(l.traverse()) == [3, 2, 1]
    assert l.delete(lambda x: x == 2) and list(l.traverse()) == [3, 1]

def test_stack_queue():
    s = Stack(); s.push(1); s.push(2); assert s.pop() == 2
    q = Queue(); q.enqueue("a"); q.enqueue("b"); assert q.dequeue() == "a"

def test_bst_grades():
    assert [GRADES.floor(x) for x in (90, 75, 55, 10)] == ["A", "B", "C", "Reject"]

def test_bfs():
    assert bfs_path("Farm", "Retailer") == ["Farm", "Mill", "Warehouse", "Distributor", "Retailer"]
    assert bfs_path("Retailer", "Farm") is None

def test_sort_search():
    assert quicksort([3, 1, 2, 2], key=lambda x: x) == [1, 2, 2, 3]
    assert binsearch_ge([1, 3, 5, 7], 4, lambda x: x) == 2

def test_greedy():
    b = [{"name": "A", "quality": 90, "cost": 60, "qty": 40}, {"name": "B", "quality": 70, "cost": 10, "qty": 100}]
    r = greedy_blend(b, 50, 60)
    assert r["mix"] == [{"name": "B", "qty": 50}] and r["meets_target"]

def test_dp():
    items = [{"name": "A", "qty": 2, "quality": 3}, {"name": "B", "qty": 3, "quality": 4}, {"name": "C", "qty": 4, "quality": 5}]
    assert dp_knapsack(items, 5) == {"best_total_quality": 7, "batches": ["A", "B"]}

def test_backtrack():
    ok = dict(moisture=12, broken=5, purity=97, qty=10)
    items = [dict(name="X", **ok), dict(name="Y", **{**ok, "moisture": 20}), dict(name="Z", **ok)]
    r = backtrack_blend(items, 20, {"moisture": 14, "broken": 10, "purity": 95})
    assert r == {"found": True, "batches": ["X", "Z"]}
