"""Create Graphviz DOT and PNG; display PNG and an iterative ASCII tree."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import webbrowser


def build_dot(graph, root):
    """Return valid Graphviz DOT for a directed dependency graph."""
    lines = [
        "digraph npm_dependencies {", "  rankdir=LR;",
        "  node [shape=box];",
    ]
    for name in sorted(graph):
        quoted = json.dumps(name, ensure_ascii=False)
        attrs = " [style=filled, fillcolor=lightblue]" if name == root else ""
        lines.append(f"  {quoted}{attrs};")
    for name in sorted(graph):
        left = json.dumps(name, ensure_ascii=False)
        for dep in graph[name]:
            right = json.dumps(dep, ensure_ascii=False)
            lines.append(f"  {left} -> {right};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_graph(graph, root, output, open_image=True):
    """Save DOT and generate PNG using Graphviz dot when installed."""
    folder = Path(output)
    folder.mkdir(parents=True, exist_ok=True)
    base = root.replace("/", "_").replace("@", "scope_")
    dot_file = folder / f"{base}.dot"
    image_file = folder / f"{base}.png"
    dot_file.write_text(build_dot(graph, root), encoding="utf-8")
    print(f"Описание Graphviz: {dot_file}")
    if shutil.which("dot") is None:
        print("Graphviz (dot) не найден. Установи: winget install graphviz")
        return dot_file, None
    command = ["dot", "-Tpng", str(dot_file), "-o", str(image_file)]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(f"Graphviz: {result.stderr.strip()}")
    print(f"Изображение графа: {image_file}")
    if open_image:
        open_local_image(image_file.resolve())
    return dot_file, image_file


def open_local_image(file_path):
    """Open the generated image in the OS default image viewer."""
    if os.name == "nt":
        os.startfile(str(file_path))
    else:
        webbrowser.open(file_path.as_uri())


def ascii_tree(graph, root):
    """Represent dependencies as a tree without infinite cyclic expansion."""
    lines = [root]
    children = list(reversed(graph.get(root, [])))
    stack = [(child, "", index == 0, frozenset([root]))
             for index, child in enumerate(children)]
    while stack:
        name, prefix, last, ancestors = stack.pop()
        lines.append(prefix + ("└── " if last else "├── ") + name
                     + (" [цикл]" if name in ancestors else ""))
        if name in ancestors:
            continue
        next_prefix = prefix + ("    " if last else "│   ")
        deps = list(reversed(graph.get(name, [])))
        for index, dep in enumerate(deps):
            stack.append((dep, next_prefix, index == 0,
                          ancestors | frozenset([name])))
    return "\n".join(lines)
