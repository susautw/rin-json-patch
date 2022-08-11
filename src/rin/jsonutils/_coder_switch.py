from json import JSONEncoder, JSONDecoder

from typing import Tuple

from . import set_default_encoder, set_default_decoder


class CoderSwitch:
    def __init__(self):
        self.coders = {}

    def use(self, profile_name: str) -> None:
        encoder, decoder = self.coders[profile_name]
        set_default_encoder(encoder)
        set_default_decoder(decoder)

    def register(self, profile_name: str, encoder: JSONEncoder, decoder: JSONDecoder) -> None:
        self.coders[profile_name] = (encoder, decoder)

    def get_coder(self, profile_name: str) -> Tuple[JSONEncoder, JSONDecoder]:
        return self.coders[profile_name]
