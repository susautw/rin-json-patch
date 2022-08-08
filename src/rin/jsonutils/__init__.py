import json
from functools import partial

from .typing import JSONSerializable, JSONType
from .advanced_json_encoder import AdvancedJSONEncoder, IResolver, ResolveError, ResolverPriority

__all__ = [
    "get_default_encoder", "set_default_encoder", "get_default_decoder", "set_default_decoder",
    "AdvancedJSONEncoder", "IResolver", "ResolveError", "ResolverPriority",
    "coder_switch", "JSONSerializable", "JSONType"
]


def get_default_encoder() -> json.JSONEncoder:
    return json._default_encoder


def set_default_encoder(encoder: json.JSONEncoder) -> None:
    json._default_encoder = encoder


def get_default_decoder() -> json.JSONDecoder:
    return json._default_decoder


def set_default_decoder(decoder: json.JSONDecoder) -> None:
    json._default_decoder = decoder


def get_default_advanced_encoder() -> AdvancedJSONEncoder:
    from .resolvers import NumpyResolver, IterableResolver, DateTimeResolver, NumberResolver, JSONSerializableResolver
    resolvers = {
        "serializable": JSONSerializableResolver(),
        "numpy": NumpyResolver(),
        "iterable": IterableResolver(),
        "datetime": DateTimeResolver(),
        "number": NumberResolver()
    }
    encoder = AdvancedJSONEncoder()
    for n, r in resolvers.items():
        encoder.add_resolver(n, r)
    return encoder

from ._coder_switch import CoderSwitch

coder_switch = CoderSwitch()
coder_switch.register("basic", json._default_encoder, json._default_decoder)
coder_switch.register("advanced", get_default_advanced_encoder(), json._default_decoder)
use_basic_coders = partial(coder_switch.use, "basic")
use_advanced_coders = partial(coder_switch.use, "advanced")
