from typing import Dict
from datetime import datetime

import cattr


class Marshaller:
    """A class for structuring and unstructuring Python data."""

    def __init__(self):
        self._initialize_converter()

    def _initialize_converter(self):
        converter = cattr.Converter()

        # dict
        converter.register_unstructure_hook(dict, lambda obj: {k: obj[k] for k in obj})

        # datetime
        converter.register_unstructure_hook(datetime, lambda obj: obj.timestamp())
        # TODO: converter.register_structure_hook()

        self.converter = converter

    def unmarshall(self, obj) -> Dict:
        """Convert a dataclass object to unstructured Python data.

        Args:
            obj: a dataclass object

        Returns:
            A nested Python dict.

        """

        obj = self.converter.unstructure(obj)
        return obj

    def marshall(self, obj, kind):
        """Convert a dataclass object to unstructured Python data.

        Args:
            obj: a dataclass object

        Returns:
            A nested Python dict.

        """
        
        return self.converter.structure(obj, kind)
