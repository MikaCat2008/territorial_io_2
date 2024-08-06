from __future__ import annotations

from typing import Generic, TypeVar, Iterable

T = TypeVar("T")


class DoubleLinkedNode(Generic[T]):
    value: T
    after_node: DoubleLinkedNode[T]
    before_node: DoubleLinkedNode[T]

    def __init__(
        self, value: T, 
        before_node: DoubleLinkedNode[T],
        after_node: DoubleLinkedNode[T]
    ) -> None:
        self.value = value
        self.after_node = after_node
        self.before_node = before_node

    def __repr__(self) -> str:
        return f"Node({self.value})"


class LinkedListIterator(Generic[T]):
    index: int
    length: int
    dl_list: DoubleLinkedList
    current_node: DoubleLinkedNode

    def __init__(self, dl_list: DoubleLinkedList) -> None:
        self.index = 0
        self.length = dl_list.length
        self.dl_list = dl_list
        self.current_node = None

    def __iter__(self) -> LinkedListIterator:
        return self
    
    def __next__(self) -> T:
        if self.index == self.length:
            raise StopIteration
        
        self.index += 1

        if self.current_node is None:
            self.current_node = self.dl_list.first_node
        else:
            self.current_node = self.current_node.after_node

        return self.current_node


class DoubleLinkedList(Generic[T]):
    length: int
    last_node: DoubleLinkedNode
    first_node: DoubleLinkedNode
    
    def __init__(self, iterable: Iterable = None) -> None:
        self.length = 0
        self.last_node = None
        self.first_node = None

        if iterable:
            for item in iterable:
                self.append_end(item)

    def append_start(self, value: T) -> DoubleLinkedNode:
        new_node = DoubleLinkedNode(value, None, self.first_node)
        
        if self.length == 0:
            self.last_node = new_node
            self.first_node = new_node
        else:
            self.first_node.before_node = new_node
            self.first_node = new_node

        self.length += 1

        return new_node

    def append_end(self, value: T) -> DoubleLinkedNode:
        new_node = DoubleLinkedNode(value, self.last_node, None)

        if self.length == 0:
            self.last_node = new_node
            self.first_node = new_node
        else:
            self.last_node.after_node = new_node
            self.last_node = new_node

        self.length += 1

        return new_node

    def insert_before(self, value: T, node: DoubleLinkedNode) -> DoubleLinkedNode:
        new_node = DoubleLinkedNode(value, node.before_node, node.after_node)

        if node.before_node is not None:
            node.before_node.after_node = new_node

        node.before_node = new_node

        if node is self.first_node:
            self.first_node = new_node

        self.length += 1

        return new_node
    
    # def insert_after(self, value: T, node: DoubleLinkedNode) -> DoubleLinkedNode:
    #     new_node = DoubleLinkedNode(value, node.before_node, node.after_node)

    #     if node.after_node is not None:
    #         node.after_node.before_node = new_node

    #     node.after_node = new_node

    #     if node is self.last_node_node:
    #         self.last_node = new_node

    #     self.length += 1

    #     return new_node

    def flip_nodes(self, node_a: DoubleLinkedNode, node_b: DoubleLinkedNode) -> None:
        value = node_a.value

        node_a.value = node_b.value
        node_b.value = value

    def remove_node(self, node: DoubleLinkedNode) -> None:
        if node is self.last_node:
            self.last_node = node.before_node
        if node is self.first_node:
            self.first_node = node.after_node
        
        if node.after_node:
            node.after_node.before_node = node.before_node
        if node.before_node:
            node.before_node.after_node = node.after_node

        self.length -= 1

    def to_list(self) -> Iterable[T]:
        return [ item.value if item is not None else None for item in self ]

    def __iter__(self) -> LinkedListIterator[DoubleLinkedNode[T]]:
        return LinkedListIterator[T](self)

    def __repr__(self) -> str:
        return f"DoubleLinkedList({', '.join(str(item) for item in self)})"
