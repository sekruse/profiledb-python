def find(func, iterable):
    '''Find an element that satisfies a predicate.'''
    filtered = [item for item in iterable if func(item)]
    if len(filtered) == 0: return None
    if len(filtered) > 1:
        print("Warning: find(...) found more than one matching element.")
    return filtered[0]

def median(values):
    size = len(values)
    sortedvalues = sorted(values)
    if size % 2 == 0:
        return (values[size / 2] + values[size / 2 - 1]) / 2
    else:
        return values[size / 2]

class ProfileDB:
    def __init__(self, experiments):
        self.experiments = experiments

    def singleseries(self, title, xfunc, yfunc, selfunc = lambda val: True, groupfunc = None):
        return self._createseries(self.experiments, title, xfunc, yfunc, selfunc, groupfunc)

    def _createseries(self, data, title, xfunc, yfunc, selfunc, groupfunc):
        # Extract the data.
        mapping = {}
        for element in data:
            if not selfunc(element): continue
            x = xfunc(element)
            y = yfunc(element)
            if x is not None and y is not None:
                if x in mapping.keys():
                    mapping[x].append(y)
                else:
                    mapping[x] = [y]

        #Group the data.
        sorteditems = sorted(mapping.items(), key = lambda item: item[0])
        x = []
        y = []
        for item in sorteditems:
            # Flatten if there is no group function.
            if groupfunc is None:
                for yval in item[1]:
                    x.append(item[0])
                    y.append(yval)
            # Otherwise group.
            else:
                x.append(item[0])
                y.append(groupfunc(item[1]))
        return Series(title, x, y)


    def multipleseries(self, keyfunc, xfunc, yfunc, selfunc = lambda val: True, groupfunc = None, titlefunc = lambda key: str(key)):
        # Find the series keys and according experiments.
        experimentgroups = {}
        for exp in self.experiments:
            if not selfunc(exp): continue
            key = keyfunc(exp)
            if key is None: continue
            if key in experimentgroups.keys():
                experimentgroups[key].append(exp)
            else:
                experimentgroups[key] = [exp]

        # Create a series for all of the experiment groups.
        return [(item[0], self._createseries(item[1], titlefunc(item[0]), xfunc, yfunc, lambda exp: True, groupfunc)) for item in experimentgroups.items()]


    def confkeys(self, selfunc = lambda exp: True):
        keys = set()
        for exp in self.experiments:
            if not selfunc(exp): continue
            for key in exp.subject().configuration().keys():
                keys.add(key)
        return keys

    def confvalues(self, key):
        return set([exp.conf(key) for exp in self.experiments])

    def tags(self):
        return set([tag for exp in self.experiments for tag in exp.tags()])

class Subject:
    def __init__(self, data):
        self.data = data

    def id(self):
        return self.data['id']

    def version(self):
        return self.data['version']

    def configuration(self):
        return self.data['configuration']

class Experiment:
    def __init__(self, data):
        self.data = data

    def tags(self):
        return self.data.get('tags', [])

    def measurements(self):
        return self.data.get('measurements', [])

    def subject(self):
        return Subject(self.data.get('subject', {}))

    def conf(self, key, fallback = None):
        return self.subject().configuration().get(key, fallback)

    def measurement(self, path, fallback = {}):
        measurements = self.measurements()
        for elem in path:
            next = find(lambda m: m['id'] == elem, measurements)
            if next is None: return fallback
            measurements = next.get('rounds', [])
            return next
        raise Exception

class Series:

    def __init__(self, title, x, y):
        self.title = title
        self.x = x
        self.y = y

def load(path):
    import json
    f = open(path)
    experiments = []
    for line in f:
        experiments.append(Experiment(json.loads(line)))
    return ProfileDB(experiments)
