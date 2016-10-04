def find(func, iterable):
    '''Find an element that satisfies a predicate.'''
    filtered = [item for item in iterable if func(item)]
    if len(filtered) == 0: return None
    if len(filtered) > 1:
        print("Warning: find(...) found more than one matching element.")
    return filtered[0]

def median(values):
    '''Calculates the median of the given values'''
    size = len(values)
    center = size // 2
    sortedvalues = sorted(values)
    if size % 2 == 0:
        return (values[center - 1] + values[center]) / 2
    else:
        return values[center]

def geomean(values):
    '''Calculates the geometric mean of a sequence of non-negative values.'''
    import math
    accu = 0
    for value in values:
        if value < 0:
            raise ValueError('Cannot include element {} into geometric mean calculation'.format(value))
        accu += math.log(value, 2)
    return 2 ** (accu / len(values))
