"""Small executable models for display chapters 43–45 (stable IDs 49–51), not production services/tools.
Standard library only. Refund exploration caps external effects at two;
invalidation computes a conservative dependency closure; repair search checks
only the explicitly finite input domain and fixed candidate set.
"""
from collections import deque
from dataclasses import dataclass
from hashlib import sha256
from itertools import product
import json


@dataclass(frozen=True)
class RefundState:
    local: str = 'paid'        # persistent local database status
    phase: str = 'idle'        # volatile sender state
    effects: int = 0           # persistent external effect count, capped at two
    remote_seen: bool = False  # external dedup record for one stable request key


def refund_steps(s, deduplicate):
    """Assume atomic local intent write and atomic remote dedup+effect.
    No concurrent orders, key expiry, message reordering, amount limits or disk
    failures are modeled. A crash loses phase, not either durable store.
    """
    if s.local == 'paid':
        yield 'commit pending intent', RefundState('pending', 'idle', s.effects, s.remote_seen)
    if s.local == 'pending' and s.phase == 'idle':
        increment = not (deduplicate and s.remote_seen)
        if s.effects + increment <= 2:
            yield 'deliver same key', RefundState('pending', 'waiting', s.effects + increment, True)
    if s.local == 'pending' and s.phase == 'waiting':
        yield 'crash before local acknowledgement', RefundState('pending', 'idle', s.effects, s.remote_seen)
        yield 'commit refunded acknowledgement', RefundState('refunded', 'idle', s.effects, s.remote_seen)


def explore_refunds(deduplicate):
    if type(deduplicate) is not bool:
        raise ValueError('deduplicate must be bool')
    initial = RefundState()
    queue = deque([(initial, ())])
    seen = {initial}
    duplicate_trace = None
    while queue:
        state, trace = queue.popleft()
        if state.effects == 2 and duplicate_trace is None:
            duplicate_trace = trace
        for event, nxt in refund_steps(state, deduplicate):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, trace + (event,)))
    return seen, duplicate_trace


def invalidated(graph, changed):
    """graph[node] lists inputs used by that cached result. Handles cycles.
    Returns changed nodes and their transitive consumers, not recomputation.
    """
    if not isinstance(graph, dict) or any(not isinstance(n, str) for n in graph):
        raise ValueError('graph must have string node names')
    reverse = {n: set() for n in graph}
    for node, deps in graph.items():
        if not isinstance(deps, (list, tuple, set, frozenset)):
            raise ValueError('dependencies must be an explicit collection')
        for dep in deps:
            if not isinstance(dep, str) or dep not in graph:
                raise ValueError('every dependency must name a graph node')
            reverse[dep].add(node)
    if not isinstance(changed, (list, tuple, set, frozenset)) or any(not isinstance(n, str) or n not in graph for n in changed):
        raise ValueError('every changed node must name a graph node')
    result = set(changed)
    queue = deque(changed)
    while queue:
        for consumer in reverse[queue.popleft()]:
            if consumer not in result:
                result.add(consumer)
                queue.append(consumer)
    return result


def analysis_key(source, semantics, library_model, configuration):
    """Illustrative cache identity. Caller still must enumerate all real inputs."""
    payload = json.dumps([source, semantics, library_model, configuration], sort_keys=True, separators=(',', ':'))
    return sha256(payload.encode('utf-8')).hexdigest()


def refund_spec(remaining, requested):
    """Policy for this example: accept up to available positive balance."""
    return min(max(requested, 0), remaining)


CANDIDATES = {
    'always-zero': lambda remaining, requested: 0,
    'raw-request': lambda remaining, requested: requested,
    'upper-bound-only': lambda remaining, requested: min(requested, remaining),
    'clamp': lambda remaining, requested: min(max(requested, 0), remaining),
}


def counterexample(candidate, domain):
    for remaining, requested in domain:
        actual = CANDIDATES[candidate](remaining, requested)
        expected = refund_spec(remaining, requested)
        if actual != expected:
            return (remaining, requested, actual, expected)
    return None


def finite_cegis():
    """Four candidates, 18 explicit pairs. No claim over arbitrary programs."""
    domain = list(product(range(3), range(-1, 5)))
    observations = [(0, 0)]
    history = []
    while True:
        eligible = [name for name in CANDIDATES if counterexample(name, observations) is None]
        if not eligible:
            return None, history
        chosen = eligible[0]
        witness = counterexample(chosen, domain)
        history.append({'candidate': chosen, 'counterexample': witness})
        if witness is None:
            return chosen, history
        observations.append(witness[:2])


if __name__ == '__main__':
    for dedup in (False, True):
        states, witness = explore_refunds(dedup)
        print('refund', {'deduplicate': dedup, 'states': len(states), 'duplicate_trace': witness})
    graph = {'gateway-model': [], 'refund-summary': ['gateway-model'], 'handler-summary': ['refund-summary'], 'report': ['handler-summary'], 'unrelated': []}
    print('invalidated', sorted(invalidated(graph, {'gateway-model'})))
    print('finite repair search', finite_cegis())
