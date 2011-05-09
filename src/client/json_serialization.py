#!../../bin/python2.7
from __future__ import division, print_function, unicode_literals

import base64
import json

class JsonSerializer(object):
    """Provides JSON serialization for a set of classes."""
    
    def __init__(self, types=None, type_property=None, sort_keys=None,
                 indent=None, separators=None):
        if types:
            self.types = dict(types)
        else:
            self.types = None
        
        if type_property is not None:
            self.type_property = type_property
        
        if separators is not None:
            self.separators = separators
        
        if indent is not None:
            self.indent = indent
        
        if sort_keys is not None:
            self.sort_keys = sort_keys
        
        self.value_serializer = self._make_value_serializer()
    
    def dump(self, obj, fp, indent=None, separators=None):
        """Serialize an object and write it to a file."""
        
        return json.dump(obj=obj, fp=fp,
                         indent=indent or self.indent,
                         sort_keys=self.sort_keys,
                         separators=separators or self.separators,
                         default=self.value_serializer)
    
    def dumps(self, obj, indent=None, separators=None):
        """Serialize an object and return it as a string."""
        
        return json.dumps(obj=obj,
                          indent=indent or self.indent,
                          sort_keys=self.sort_keys,
                          separators=separators or self.separators,
                          default=self.value_serializer)
    
    def load(self, fp):
        """Loads and deserializes an object from a file."""
        
        return json.load(fp=fp,
                         object_hook=self.object_hook,
                         parse_constant=self._parse_constant)
    
    def loads(self, s):
        """Deserializes an object from a string."""
        
        return json.loads(s=s,
                          object_hook=self.object_hook,
                          parse_constant=self._parse_constant)
    
    type_property = "__type__"
    
    sort_keys = True
    indent = None
    separators = (",", ":")
    
    _constants = {
        "true": True,
        "false": False,
        "null": None
    }
    
    def _parse_constant(self, name):
        return self._constants[name]
    
    def object_hook(self, o):
        if self.type_property in o and o[self.type_property] in self.types:
            return (self.types[o[self.type_property]]
                    .from_json_equivilent(o))
        else:
            return o

    def _make_value_serializer(self):
        if self.types is not None:
            def default(o):
                if hasattr(o, "to_json_equivilent"):
                    for name, cls in self.types.items():
                        if isinstance(o, cls):
                            result = o.to_json_equivilent()
                            
                            result[self.type_property] = name
                            return result
                    else:
                        raise TypeError("{}s not known to serializer."
                                        .format(type(o).__name__))
                else:
                    print(dir(o))
                    raise TypeError("{}s can not be JSON-serialized."
                                    .format(type(o).__name__))
            
            return default
        else:
            return None
