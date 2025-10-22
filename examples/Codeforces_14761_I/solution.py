def minimal_distinct_deadlines(n, deadlines):
    """
    Determines the minimal number of distinct deadlines needed such that each task has a unique deadline.
    """
    deadlines = sorted(deadlines)
    unique_deadlines = 0
    taken_deadlines = set()

    for deadline in deadlines:
        while deadline in taken_deadlines:
            deadline += 1
        taken_deadlines.add(deadline)
        unique_deadlines += 1

    return unique_deadlines
