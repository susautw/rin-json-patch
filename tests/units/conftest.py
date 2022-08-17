import importlib

import pytest


@pytest.fixture()
def json():
    import json
    importlib.reload(json)
    return json


@pytest.fixture()
def jsonutils(json):
    from rin import jsonutils
    importlib.reload(jsonutils)
    return jsonutils
