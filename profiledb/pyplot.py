import matplotlib.pyplot as plt

def plot(series, axes = plt, **kwargs):
    '''Plot a single series.'''
    axes.plot(series.x, series.y, **evaluate(series, **kwargs))

def plotall(seriesset, axes = plot, **kwargs):
    '''Plot all of the series in the seriesset.'''
    for series in seriesset:
        plot(series, axes, **kwargs)

def evaluate(series, **kwargs):
    '''Resolves any keyword arguments that are functions by applying the series to them.'''
    evaluated = {}
    for kwarg in kwargs.items():
        key = kwarg[0]
        val = kwarg[1]
        if callable(val): val = val(series)
        evaluated[key] = val
    return evaluated

def series_title(series):
    return series.title
