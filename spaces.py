"""Gym spaces involving Literals.

Unlike typical spaces, Literal spaces may change with
each episode, since objects, and therefore possible
groundings, may change with each new PDDL problem.
"""
from gym.spaces import Space
from collections import defaultdict


class LiteralSpace(Space):

    def __init__(self, predicates):
        self.predicates = sorted(predicates)
        self.num_predicates = len(predicates)
        self.objects = set()
        super().__init__()

    def update(self, objs):
        # Organize objects by type
        self.type_to_objs = defaultdict(list)

        for obj in sorted(objs):
            self.type_to_objs[obj.var_type].append(obj)

        self.objects = objs

    def sample(self):
        # Sample a random predicate
        idx = self.np_random.choice(self.num_predicates)
        predicate = self.predicates[idx]

        # Sample grounding
        grounding = []
        for var_type in predicate.var_types:
            choices = self.type_to_objs[var_type]
            choice = choices[self.np_random.choice(len(choices))]
            grounding.append(choice)
        return predicate(*grounding)

    def all_ground_literals(self):
        all_ground_literals = set()
        for predicate in self.predicates:
            choices = [self.type_to_objs[vt] for vt in predicate.var_types]
            for choice in itertools.product(*choices):
                if len(set(choice)) != len(choice):
                    continue
                lit = predicate(*choice)
                all_ground_literals.add(lit)
        return all_ground_literals

class LiteralSetSpace(LiteralSpace):

    def sample(self):
        raise NotImplementedError()