import json


class Node:
    def __init__(self, key: str, val: dict) -> None:
        """
        Doublely linked list node.
        """
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class BookCache:
    """
    Implement book cache using least recently used (LRU) cache.
    """

    def __init__(self, capacity: int):
        self._capacity = capacity
        self._hashmap = {}
        # dummy head and tail
        self._head = Node("0000", {})
        self._tail = Node("0001", {})
        self._head.next = self._tail
        self._tail.prev = self._head

    def get(self, key: str) -> dict:
        """
        Retrieve cached book by isbn, return empty dict if book is not found.
        """
        if key in self._hashmap:
            node = self._hashmap[key]
            self.put(key, node.val)  # put recently retrieved book back to the head of the list
            return node.val
        return {}

    def put(self, key: str, val: dict) -> None:
        """
        Put book into cache and remove the least recently retrieved book if reaches capacity.
        """
        if key in self._hashmap:
            node = self._hashmap[key]
            self._remove_node_from_list(node)
            self._insert_to_head(node)
            return
        new_book = Node(key, val)
        if len(self._hashmap) >= self._capacity:  # remove the least recently retrieved book if reaches capacity.
            self._remove_node_from_tail()
        self._insert_to_head(new_book)
        self._hashmap[key] = new_book

    def _insert_to_head(self, node: Node) -> None:
        """
        Always insert node at the head.
        """
        node.next = self._head.next
        node.prev = self._head
        node.next.prev = node
        self._head.next = node

    @staticmethod
    def _remove_node_from_list(node: Node) -> None:
        """
        Remove node from list.
        """
        node.prev.next = node.next
        node.next.prev = node.prev

    def _remove_node_from_tail(self) -> None:
        """
        Remove node from the tail of list.
        """
        if self._hashmap:
            last_node = self._tail.prev
            del self._hashmap[last_node.key]
            self._remove_node_from_list(last_node)

    # Helpers for testing
    def get_head(self) -> Node:
        return self._head

    def get_tail(self) -> Node:
        return self._tail

    def get_map(self) -> dict:
        return self._hashmap

    def get_book_val(self, isbn) -> dict:
        return self._hashmap[isbn].val


def get_book_info(books: dict, isbn: str) -> dict:
    """
    Retrieve the book from data by isbn.
    :param books: book available
    :param isbn: the isbn of the requested book
    :return: the retrieved book info. Return empty dict if the book is not found.
    """
    if isbn in books:
        return books[isbn]
    return {}


if __name__ == '__main__':
    book_cache = BookCache(3)
    json_file = open("books.json")
    books_json = json.load(json_file)

    isbns = ['1234', '1235', '1236', '1237', '1238']
    for isbn in isbns:
        book = get_book_info(books_json, isbn)
        book_cache.put(isbn, book)
    cached_book = book_cache.get('1237')
    print(cached_book)
    json_file.close()
