import matplotlib.pyplot as plt

def plot(series, **kwargs):
    '''Plot a single series.'''
    plt.plot(series.x, series.y, label = series.title, **evaluate(series, **kwargs))

def plotall(seriesset, **kwargs):
    '''Plot all of the series in the seriesset.'''
    for series in seriesset:
        plot(series, **kwargs)

def evaluate(series, **kwargs):
    '''Resolves any keyword arguments that are functions by applying the series to them.'''
    evaluated = {}
    for kwarg in kwargs.items():
        key = kwarg[0]
        val = kwarg[1]
        if callable(val): val = val(series)
        evaluated[key] = val
    return evaluated
