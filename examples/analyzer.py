"""Teaching IR analyzer: flat constant propagation over an explicit CFG.
No source parser, calls, heap, exceptions or path feasibility. Python 3.10+.
"""
from collections import deque
import argparse
import json

TOP = "?"  # Values are integers or TOP; None is an unreachable environment.


def join(a, b):
    if a is None:
        return None if b is None else b.copy()
    if b is None:
        return a.copy()
    return {v: a[v] if a[v] == b[v] else TOP for v in a}


def validate(program):
    if not isinstance(program, dict) or set(program) != {"entry", "nodes"}:
        raise ValueError("program needs exactly entry and nodes")
    nodes = program["nodes"]
    if not isinstance(program["entry"], str) or not isinstance(nodes, dict) or not nodes or program["entry"] not in nodes:
        raise ValueError("invalid entry/nodes")
    layouts = {
        "const": {"op", "dst", "value", "next"},
        "input": {"op", "dst", "next"},
        "copy": {"op", "dst", "src", "next"},
        "add": {"op", "dst", "a", "b", "next"},
        "sub": {"op", "dst", "a", "b", "next"},
        "mul": {"op", "dst", "a", "b", "next"},
        "div": {"op", "dst", "a", "b", "next"},
        "branch": {"op", "cond", "true", "false"},
        "goto": {"op", "next"},
        "assert_nonzero": {"op", "src", "next"},
        "stop": {"op"},
    }
    variables = set()
    for name, node in nodes.items():
        if not isinstance(name, str) or not isinstance(node, dict):
            raise ValueError("node names must be strings; nodes must be objects")
        op = node.get("op")
        if not isinstance(op, str) or op not in layouts or set(node) != layouts[op]:
            raise ValueError(f"invalid node {name}")
        for key in ("dst", "src", "a", "b", "cond"):
            if key in node:
                if not isinstance(node[key], str) or not node[key]:
                    raise ValueError(f"invalid variable in {name}")
                variables.add(node[key])
        if op == "const" and type(node["value"]) is not int:
            raise ValueError("const requires an integer (not bool)")
        for target in successors(node):
            if not isinstance(target, str) or target not in nodes:
                raise ValueError(f"missing target {target}")
    return sorted(variables)


def successors(node):
    if node["op"] == "branch":
        return [node["true"], node["false"]]
    return [node["next"]] if "next" in node else []


def transfer(node, state):
    out = state.copy()
    op = node["op"]
    if op == "const":
        out[node["dst"]] = node["value"]
    elif op == "input":
        out[node["dst"]] = TOP
    elif op == "copy":
        out[node["dst"]] = state[node["src"]]
    elif op in {"add", "sub", "mul", "div"}:
        a, b = state[node["a"]], state[node["b"]]
        value = TOP
        if a != TOP and b != TOP:
            if op == "add": value = a + b
            elif op == "sub": value = a - b
            elif op == "mul": value = a * b
            elif b != 0: value = a // b
        out[node["dst"]] = value
    return out


def analyze(program):
    variables = validate(program)
    nodes = program["nodes"]
    states = {n: None for n in nodes}
    states[program["entry"]] = {v: TOP for v in variables}
    work = deque([program["entry"]])
    iterations = 0
    while work:
        name = work.popleft()
        iterations += 1
        out = transfer(nodes[name], states[name])
        for target in successors(nodes[name]):
            updated = join(states[target], out)
            if updated != states[target]:
                states[target] = updated
                work.append(target)
    # Report only after convergence: temporary constants are not final facts.
    reports = []
    for name, node in nodes.items():
        if states[name] is None:
            continue
        op = node["op"]
        variable = node["b"] if op == "div" else node.get("src")
        if op not in {"div", "assert_nonzero"}:
            continue
        value = states[name][variable]
        if value == 0 or value == TOP:
            reports.append({"node": name, "property": "nonzero-denominator" if op == "div" else "nonzero-assertion",
                            "operand": variable, "abstract_value": value,
                            "status": "known-zero-in-abstract-state" if value == 0 else "unknown-may-be-zero"})
    return {"in_states": states, "reports": reports, "worklist_steps": iterations}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program")
    args = parser.parse_args()
    with open(args.program, encoding="utf-8") as f:
        print(json.dumps(analyze(json.load(f)), ensure_ascii=False, indent=2))
