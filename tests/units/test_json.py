from unittest.mock import MagicMock

from json import JSONEncoder, JSONDecoder


def test_get_set_encoder(json, jsonutils):
    assert json._default_encoder is jsonutils.get_default_encoder()
    encoder = JSONEncoder(indent=0)
    jsonutils.set_default_encoder(encoder)
    assert json._default_encoder is encoder
    assert json.dumps({"test": 1}) == '{\n"test": 1\n}'


def test_get_set_decoder(json, jsonutils):
    assert json._default_decoder is jsonutils.get_default_decoder()
    parse_int = MagicMock(side_effect=int)
    decoder = JSONDecoder(parse_int=parse_int)
    jsonutils.set_default_decoder(decoder)
    assert json._default_decoder is decoder
    assert json.loads('[1, 2, 3.5, "test"]') == [1, 2, 3.5, "test"]
    assert parse_int.call_count == 2
