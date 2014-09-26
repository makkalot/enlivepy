"""
Some utils used in project
"""

def concat(l1=None, l2=None):
    """
    concats the 2 lists
    """
    lst = []
    if l1:
        lst.extend(l1)
    if l2:
        lst.extend(l2)
    return lst


def flatten(lst):
    """
    flattens specified list iteratively
    """
    def _concater(init, rest):
        if type(rest) == list:
            return concat(init, reduce(_concater, rest, []))
        else:
            return concat(init, [rest])

    return reduce(_concater, lst, [])

