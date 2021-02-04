from typing import *
_KT = TypeVar('KT')  # Key type.
_VT = TypeVar('VT')  # Value type.
_VT_co = TypeVar('VT_co', covariant=True)  # Value type covariant containers.


class AttrDict(dict):
    def __init__(self, data: dict) -> None:
        print("__init__")
        for key in list(data.keys()):
            if type(data[key]) == dict:
                self.__dict__[key.replace(" ", "_")] = self.__class__(data[key])
            else:
                self.__dict__[key.replace(" ", "_")] = data[key]

    def __repr__(self) -> str:
        def recursive(data: __class__) -> str:
            try:
                __ = ""
                for key in list(data.__dict__.keys()):
                    if isinstance(data[key], self.__class__):
                        __ += f"{key!r}: " "{" + recursive(data[key]) + "}, "
                    else:
                        __ += f"{key!r}: {data[key]!r}, "
                return __[:-2]
            except RecursionError:
                return "The Data in this class might be to big and because of that a RecursionError occurred"
        return "{" + recursive(self) + "}"
    
    __str__ = __repr__

    def __getitem__(self, item): return self.__dict__.__getitem__(item.replace(" ", "_"))
    def __getattr__(self, item): return self.__getitem__(item)
    def __setitem__(self, key, value): self.__dict__[key.replace(" ", "_")] = self.__class__(value.copy()); print("DEBUG")
    def __setattr__(self, key, value): return self.__setitem__(key, value)
    def __contains__(self, item): return self.__dict__.__contains__(item)
    def __delitem__(self, key): return self.__dict__.__delitem__(key)
    def __eq__(self, other): return self.__dict__.__eq__(other)
    def __ge__(self, other): return self.__dict__.__ge__(other)
    def __gt__(self, other): return self.__dict__.__gt__(other)
    def __iter__(self): return self.__dict__.__iter__()
    def __len__(self): return self.__dict__.__len__()
    def __le__(self, other): return self.__dict__.__le__(other)
    def __lt__(self, other): return self.__dict__.__lt__(other)
    def __ne__(self, other): return self.__dict__.__ne__(other)
    def __reversed__(self): return self.__dict__.__reversed__()
    def __sizeof__(self): return self.__dict__.__sizeof__()

    def clear(self) -> None: return self.__dict__.clear()
    def copy(self) -> Dict[_KT, _VT]: return self.__dict__.copy()
    def get(self, k: _KT) -> Optional[_VT_co]: return self.__dict__.get(k)
    def items(self) -> ItemsView[_KT, _VT]: return self.__dict__.items()
    def keys(self) -> KeysView[_KT]: return self.__dict__.keys()
    def pop(self, k: _KT) -> _VT: return self.__dict__.pop(k)
    def popitem(self) -> Tuple[_KT, _VT]: return self.__dict__.popitem()
    def setdefault(self, k: _KT, default: _VT = ...) -> _VT: return self.__dict__.setdefault(k, default)
    def update(self, __m: Mapping[_KT, _VT], **kwargs: _VT) -> None: return self.__dict__.update(__m, **kwargs)
    def values(self) -> ValuesView[_VT]: return self.__dict__.values()
