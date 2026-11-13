"""Construct dependency-first order and report cyclic dependencies."""

import heapq


def dependency_first_order(graph):
    """Topologically order dependencies before dependents (DAG only)."""
    pending = {name: len(set(deps)) for name, deps in graph.items()}
    dependents = {name: set() for name in graph}
    for name, deps in graph.items():
        for dep in set(deps):
            dependents[dep].add(name)
    ready = [name for name, count in pending.items() if count == 0]
    heapq.heapify(ready)
    result = []
    while ready:
        name = heapq.heappop(ready)
        result.append(name)
        for dependent in sorted(dependents[name]):
            pending[dependent] -= 1
            if pending[dependent] == 0:
                heapq.heappush(ready, dependent)
    unresolved = sorted(name for name in graph if name not in result)
    return result, unresolved


def show_order(graph):
    """Print safe dependency-first ordering or a cycle warning."""
    order, unresolved = dependency_first_order(graph)
    print("Порядок подготовки зависимостей:")
    for position, name in enumerate(order, start=1):
        print(f"  {position}. {name}")
    if unresolved:
        print("Цикл: строгий порядок невозможен для: ", ", ".join(unresolved))
    return order, unresolved
