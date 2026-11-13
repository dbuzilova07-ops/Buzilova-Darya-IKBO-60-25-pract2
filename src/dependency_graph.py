"""Build dependency graphs using iterative BFS and inspect cycles."""

from collections import deque



def traverse_bfs(start, get_dependencies, max_nodes=40):
    """Build reachable adjacency map using BFS without recursion."""
    graph = {}
    queue = deque([start])
    discovered = {start}
    traversal = []
    while queue:
        name = queue.popleft()
        dependency_data = get_dependencies(name)
        deps = sorted(dependency_data)
        graph[name] = deps
        traversal.append(name)
        for dep in deps:
            if dep not in discovered:
                if len(discovered) >= max_nodes:
                    raise ValueError("Превышен предел --max-nodes")
                discovered.add(dep)
                queue.append(dep)
    return graph, traversal


def cycle_example(graph):
    """Find one directed cycle with iterative depth-first inspection."""
    color = {}
    for start in sorted(graph):
        if color.get(start):
            continue
        color[start] = 1
        stack = [(start, iter(graph.get(start, [])))]
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                color[node] = 2
                stack.pop()
                continue
            if color.get(child) == 1:
                path = [item[0] for item in stack]
                return path[path.index(child):] + [child]
            if not color.get(child):
                color[child] = 1
                stack.append((child, iter(graph.get(child, []))))
    return []
