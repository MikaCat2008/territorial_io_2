from typing import Any, Type, TypeVar, ClassVar, Callable, Optional
from functools import wraps
from threading import Thread
from multiprocessing import Pool
from multiprocessing.pool import Pool as PoolType

T = TypeVar("T", bound="PoolObject")
CallableT = TypeVar("CallableT", bound=Callable)


class PoolObject:
    id: int

    _pool: ClassVar[Optional[PoolType]] = None
    _instances: ClassVar[dict[int, "PoolObject"]] = {}

    def __init__(self, id: int) -> None:
        self.id = id

    @classmethod
    def new(cls, id: int) -> None:
        if cls._instances.get(id) is None:
            cls._instances[id] = cls(id)

    @classmethod
    def link(cls: Type[T]) -> T:
        id = len(cls._instances)

        cls._pool.apply(cls.new, (id, ))
        
        return cls(id)

    @classmethod
    def call(cls, function_name: str, id: int, args: tuple) -> None:
        instance = cls._instances[id]
        function = getattr(instance, function_name)

        return function(*args)

    @classmethod
    def create_pool(cls) -> None:
        cls._pool = Pool(1)

    @classmethod
    def get_pool(cls) -> PoolType:
        return cls._pool


def in_pool(function: CallableT) -> CallableT:
    @wraps(function)
    def _(self, *args: Any):
        pool = PoolObject.get_pool()
        
        if pool is None:
            return function(self, *args)

        return pool.apply(PoolObject.call, (function.__name__, self.id, args))
    
    return _


def in_thread(function: Callable) -> Callable:
    @wraps(function)
    def _(*args) -> Thread:
        thread = Thread(target=function, args=args)
        thread.start()

        return thread
        
    return _
