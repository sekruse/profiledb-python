from profiledb.helpers import *

class ProfileDB:
    def __init__(self, experiments):
        self.experiments = experiments

    def _createseries(self, experiments, key, title, xfunc, yfunc, selfunc, groupfunc):
        '''Creates a single Series by extracting data from the `experiments`.'''
        # Extract the data.
        mapping = {}
        for experiment in experiments:
            if not selfunc(experiment): continue
            x = xfunc(experiment)
            y = yfunc(experiment)
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
        return Series(key, title, x, y)

    def singleseries(self, title, xfunc, yfunc, selfunc = lambda val: True, groupfunc = None):
        return self._createseries(self.experiments, title, title, xfunc, yfunc, selfunc, groupfunc)


    def multipleseries(self, keyfunc, xfunc, yfunc, selfunc = lambda val: True, groupfunc = None, titlefunc = lambda key: str(key)):
        """Creates multiple series according to the definition.

        Returns:
            (list) a list containing the created `Series`"""
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
        return [self._createseries(item[1], item[0], titlefunc(item[0]), xfunc, yfunc, lambda exp: True, groupfunc)\
                for item in experimentgroups.items()]


    def configkeys(self, selfunc = lambda exp: True):
        '''Retrieve the used configuration keys for a set of experiments.'''
        keys = set()
        for exp in self.experiments:
            if not selfunc(exp): continue
            for key in exp.subject().configuration().keys():
                keys.add(key)
        return keys

    def configvalues(self, key, selfunc = lambda exp: True, mapfunc = lambda value: value):
        return set([mapfunc(exp.conf(key)) for exp in self.experiments if selfunc(exp)])

    def tags(self, selfunc = lambda exp: True):
        return set([tag for exp in self.experiments for tag in exp.tags() if selfunc(exp)])

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

    def id(self):
        return self.data['id']

    def tags(self):
        return self.data.get('tags', [])

    def measurements(self):
        return self.data.get('measurements', [])

    def subject(self):
        return Subject(self.data.get('subject', {}))

    def conf(self, key, fallback = None):
        return self.subject().configuration().get(key, fallback)

    def measurement(self, *path):
        measurements = self.measurements()
        for elem in path:
            next = find(lambda m: m['id'] == elem, measurements)
            if next is None: return None
            measurements = next.get('rounds', [])
        return next
        raise Exception

    def __str__(self):
        return 'Experiment({})'.format(self.id())

class Series:
    def __init__(self, key, title, x, y):
        self.key = key
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
