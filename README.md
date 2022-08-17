# rin-jsonutils

Add custom JSON coders and provide functions to set and get the default json coders

```python
import json
import numpy as np
from datetime import datetime
from rin import jsonutils

jsonutils.use_advanced_coders()

assert json.dumps({1, 2, 3}) == '[1, 2, 3]'  # sets
assert json.dumps(np.arange(6).reshape((2, 3))) == '[[0, 1, 2], [3, 4, 5]]'  # numpy array

assert json.dumps(datetime.fromordinal(1)) == '"0001-01-01T00:00:00"' # datetime

encoder, decoder = jsonutils.coder_switch.get_coder("advanced")
assert isinstance(encoder, jsonutils.AdvancedJSONEncoder)
encoder.context['datetime_format'] = "%Y-%m-%d"
assert json.dumps(datetime.fromordinal(1)) == '"1-01-01"'
```