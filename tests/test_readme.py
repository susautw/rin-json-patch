from typing import Dict, Any

import numpy as np
from datetime import datetime


def test_use_advanced_encoder(json, jsonutils):
    jsonutils.use_advanced_coders()  # switch to advanced encoder
    # jsonutils.use_basic_coders()  # switch back to original json coders

    assert json.dumps({1, 2, 3}) == '[1, 2, 3]'  # built-in set
    assert json.dumps(np.arange(6).reshape((2, 3))) == '[[0, 1, 2], [3, 4, 5]]'  # numpy array

    assert json.dumps(datetime.fromordinal(1)) == '"0001-01-01T00:00:00"'  # datetime


def test_change_context_of_advanced_encoder(json, jsonutils):
    jsonutils.use_advanced_coders()
    encoder: jsonutils.AdvancedJSONEncoder = jsonutils.get_current_coder().encoder

    assert json.dumps(datetime.fromordinal(1)) == '"0001-01-01T00:00:00"'  # default format is isoformat
    # change the format of the datetime resolver in the encoder
    encoder.context['datetime.format'] = "%Y-%m-%d"
    assert json.dumps(datetime.fromordinal(1)) == '"0001-01-01"'


def test_custom_resolver(json, jsonutils):
    class MyObject:
        def __init__(self, i: int):
            self.i = i

    class MyObjectResolver(jsonutils.IResolver):
        def __init__(self, show_name: bool):
            self.show_name = show_name

        def get_priority(self) -> int:
            return jsonutils.ResolverPriority.MEDIUM

        def initialize(self) -> bool:
            """
            :return: False if initialization failed
            """
            return True

        def resolve(self, o, context: Dict[str, Any]) -> jsonutils.JSONType:
            """
            :raises ResolveError when cannot resolve the object.
                     If you aren't resolves the object, you MUST raise this exception.
            """
            show_name = context.get("my_object.show_name", self.show_name)
            if show_name:
                return {"name": "MyObject", "i": o.i}
            else:
                return {"i": o.i}

    encoder = jsonutils.get_coder("advanced").encoder
    encoder.add_resolver("my_object", MyObjectResolver(True))  # register the resolver to the encoder

    assert encoder.encode(MyObject(1)) == '{"name": "MyObject", "i": 1}'
    encoder.context['my_object.show_name'] = False  # change context
    assert encoder.encode(MyObject(1)) == '{"i": 1}'


def test_custom_object_with_json_serializable(json, jsonutils):
    class MyObject(jsonutils.JSONSerializable):  # inherit from JSONSerializable is optional.
        show_name: bool = True

        def __init__(self, i: int):
            self.i = i

        def __json__(self, context: Dict[str, Any]) -> jsonutils.JSONType:  # implement this method is required.
            show_name = context.get("my_object.show_name", self.show_name)
            if show_name:
                return {"name": "MyObject", "i": self.i}
            else:
                return {"i": self.i}

    encoder = jsonutils.get_coder("advanced").encoder
    assert encoder.encode(MyObject(1)) == '{"name": "MyObject", "i": 1}'
    encoder.context['my_object.show_name'] = False
    assert encoder.encode(MyObject(1)) == '{"i": 1}'


def tset_register_custom_coder(json, jsonutils):
    class MyJSONEncoder(json.JSONEncoder):
        ...

    class MyJsonDecoder(json.JSONDecoder):
        ...

    my_encoder = MyJSONEncoder()
    my_decoder = MyJsonDecoder()

    jsonutils.register_coder("my_coder", my_encoder, my_decoder)
    jsonutils.use("my_coder")
    coder_pair = jsonutils.get_current_coder()

    assert coder_pair.encoder is my_encoder
    assert coder_pair.decoder is my_decoder
