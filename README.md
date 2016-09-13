# ProfileDB

ProfileDB is thought as a tool to alleviate the instrumentation and evaluation of applications. This project is a library to load measured experiment data into Python and provides utilities to evaluate and plot them. Check out the [Java client](https://github.com/sekruse/profiledb-java) to instrument JVM code and serialize the obtained measurements.

## Instructions

You can easily use the ProfileDB Python client into your app or notebook as follows:
```python
sys.path.append('/path/to/profiledb-python')
# Load the ProfileDB model and deserialization utility.
import profiledb
# To use helpers, such as find(...) and geomean(...)
from profiledb.helpers import *
# To make use of matplotlib plotting utilities.
import profiledb.pyplot as pdbplt
```
