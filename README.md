# rin-jsonutils

Add custom JSON coders and provide functions to set and get the default json coders

```python
import json
import numpy as np
from datetime import datetime
from rin import jsonutils

jsonutils.use_advanced_coders()

json.dumps({1, 2, 3})  # sets
json.dumps(np.arange(30).reshape((2, 3, 5)))  # np.ndarray
json.dumps(datetime.now())  # datetime

encoder, decoder = jsonutils.coder_switch.get_coder("advanced")
assert isinstance(encoder, jsonutils.AdvancedJSONEncoder)
encoder.context['datetime_format'] = "%Y-%m-%d"
json.dumps(datetime.now())

```