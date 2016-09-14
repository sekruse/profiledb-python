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

## License

Copyright 2016 Sebastian Kruse

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
