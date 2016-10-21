import matplotlib.pyplot as plt

def series_title(series):
    '''This helper function extracts the title of a series.'''
    return series.title

def plot(series, axes = plt, label = series_title, **kwargs):
    '''Plot a single series.'''
    kwargs['label'] = label
    axes.plot(series.x, series.y, **evaluate(series, **kwargs))

def plotall(seriesset, axes = plt, label = series_title, **kwargs):
    '''Plot all of the series in the seriesset.'''
    for series in seriesset:
        plot(series, axes, label = label, **kwargs)

def evaluate(series, **kwargs):
    '''Resolves any keyword arguments that are functions by applying the series to them.'''
    evaluated = {}
    for kwarg in kwargs.items():
        key = kwarg[0]
        val = kwarg[1]
        if callable(val): val = val(series)
        evaluated[key] = val
    return evaluated
