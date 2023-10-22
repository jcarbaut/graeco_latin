# Computing graeco-latin squares of order 4.

import sys
from itertools import permutations
from collections import Counter

a = list(permutations(range(4)))

# First, latin squares
# Looking for tuples (p0, p1, p2, p3) of permutations of (0, 1, 2, 3)
# such that no two permutations have the same value at any index
latin = set()
for p0 in a:
    for p1 in a:
        if any(any(u == v for u, v in zip(p, p1)) for p in [p0]): continue
        for p2 in a:
            if any(any(u == v for u, v in zip(p, p2)) for p in [p0, p1]): continue
            for p3 in a:
                if any(any(u == v for u, v in zip(p, p3)) for p in [p0, p1, p2]): continue
                latin.add((p0, p1, p2, p3))

latin = sorted(latin)
print("Number of latin squares:", len(latin))

# Then inspecting pairs of latin squares
# For each pair (p, q) of latin squares, how many distinct pairs (x, y) are there,
# with pairs taken from corresponding elements of each square?
sol = set()
h = Counter()
for p in latin:
    for q in latin:
        e = set()
        for u, v in zip(p, q):
            for x, y in zip(u, v):
                e.add((x, y))
                
        # How many distinct pairs ? If 16, this is a graeco-latin square
        h[len(e)] += 1
        if len(e) == 16:
            # Build the graeco-latin square as a tuple of tuples of pairs (x, y)
            # For instance
            # (((0, 0), (1, 1), (2, 2), (3, 3)),
            #  ((1, 2), (0, 3), (3, 0), (2, 1)),
            #  ((2, 3), (3, 2), (0, 1), (1, 0)),
            #  ((3, 1), (2, 0), (1, 3), (0, 2)))
            gl = tuple([tuple([(x, y) for x, y in zip(u, v)]) for u, v in zip(p, q)])
            sol.add(gl)

sol = sorted(sol)
print("Number of graeco-latin squares:", len(sol))

# For the record, how many distinct pairs may the couple of latin squares yield?
for k in sorted(h.keys()):
    print(k, h[k])

# Now we are reducing each graeco-latin square to 'normal' form:
# - rows are sorted w.r.t the first element of each pair of the first column,
#   i.e. the first colume reads (0, _), (1, _), (2, _), (3, _)
# - columns are sorted likewise
# - the second elements are renamed so that the first row is exactly
#   (0, 0), (1, 1), (2, 2), (3, 3)
sol_red = set()
for gl in sol:
    gl = sorted(gl)
    gl = tuple(list(zip(*gl)))
    gl = sorted(gl)
    gl = tuple(list(zip(*gl)))
    tr = {y: x for x, y in gl[0]}
    gl = tuple([tuple([(x, tr[y]) for x, y in u]) for u in gl])
    sol_red.add(gl)

sol_red = sorted(sol_red)
print("Number of reduced graeco-latin squares:", len(sol_red))

# Printing them
for gl in sol_red:
    print("-" * 40)
    for u in gl:
        print(list(u))
