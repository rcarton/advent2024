from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import TextIO


@dataclass
class NumRules:
    must_be_after: set[int] = field(default_factory=set)
    must_be_before: set[int] = field(default_factory=set)


Rules = dict[int, NumRules]


def parse_rules(rules_str: str) -> Rules:
    rules: dict[int, NumRules] = defaultdict(lambda: NumRules())
    for rule_str in rules_str.split("\n"):
        left, right = rule_str.strip().split("|")
        before, after = int(left), int(right)
        rules[before].must_be_before.add(after)
        rules[after].must_be_after.add(before)

    return rules


def parse_update(update_str: str) -> list[int]:
    return [int(n) for n in update_str.strip().split(",")]


def is_update_valid(update: list[int], rules: Rules) -> bool:
    for i, n in enumerate(update):
        before = set(update[:i])
        after = set(update[i + 1 :])
        if before & rules[n].must_be_before or after & rules[n].must_be_after:
            return False
    return True


def make_valid(update: list[int], rules: Rules) -> list[int]:
    update_set = set(update)
    new_rules = {}
    # Create a set of rules only for the current update numbers
    for n in update_set:
        new_rules[n] = NumRules(
            must_be_after=rules[n].must_be_after & update_set,
            must_be_before=rules[n].must_be_before & update_set,
        )
    return make_only_valid_update_for_rules(new_rules)


def make_only_valid_update_for_rules(rules: Rules) -> list[int]:
    q = deque()
    left = set(rules.keys())

    while left:
        # Find the only rule without a before
        first = None
        for n in left:
            nr = rules[n]
            if len(nr.must_be_after) == 0:
                first = n
                continue
        assert first is not None
        q.append(first)
        left.remove(first)

        # Remove from must_be_after for all the other ones
        for n in left:
            rules[n].must_be_after.remove(first)
    return list(q)


def first(input: TextIO) -> int:
    rules_str, updates_str = input.read().split("\n\n")
    rules = parse_rules(rules_str)
    updates = [parse_update(u) for u in updates_str.strip().split("\n")]
    valid_updates = [u for u in updates if is_update_valid(u, rules)]
    return sum(u[len(u) // 2] for u in valid_updates)


def second(input: TextIO) -> int:
    rules_str, updates_str = input.read().split("\n\n")
    rules = parse_rules(rules_str)
    updates = [parse_update(u) for u in updates_str.strip().split("\n")]
    invalid_updates = [u for u in updates if not is_update_valid(u, rules)]
    valid_updates = [make_valid(u, rules) for u in invalid_updates]

    # Are there numbers not in rules? -> no, so all numbers are in rules, so we can order any update deterministically
    # all_numbers = set(item for sublist in updates for item in sublist)
    # numbers_not_in_rules = all_numbers - set(rules.keys())
    # -> empty set

    return sum(u[len(u) // 2] for u in valid_updates)
