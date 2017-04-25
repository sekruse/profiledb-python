def quote(string, char):
    return char+str(string)+char if char else string or ''

def export_multiple_series(series_list, separator=',', quote_char='"', x_title="x-value", series_name=lambda s: s.title):
    """Formats multiple `Series` as CSV.

    Arguments:
        series_list (iterable): the `Series` objects to format
        separator (str): a CSV separator
        quote_char (str): a CSV quote char or `None`
        series_name (callable): extracts the name of a Series for the header line

    Returns:
        (str) a string containing the formatted CSV data"""
    # Collect and sort the x-values.
    x_values = set()
    for series in series_list:
        x_values = x_values.union(series.x)
    x_values = list(x_values)
    x_values.sort()

    # Build the header line.
    csv = quote(x_title, quote_char)
    for series in series_list:
        csv += separator + quote(series_name(series), quote_char)
    csv += '\n'

    # Build the following lines.
    xy_maps = [dict(zip(series.x, series.y)) for series in series_list]
    for x in x_values:
        csv += str(x)
        for xy_map in xy_maps:
            csv += separator
            csv += quote(xy_map.get(x, ''), quote_char)
        csv += '\n'

    return csv
