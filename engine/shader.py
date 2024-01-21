from typing import Any


class Shader:
    def __init__(self, func) -> None:
        self.func = func
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.func(*args, **kwds)