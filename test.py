import json
import unittest

from typing import List

from BookCache import BookCache, get_book_info


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.book_cache = BookCache(3)
        self.json_file = open("books.json")
        self.books_json = json.load(self.json_file)
        self.json_file.close()

    def assert_list_and_map(self, expected_keys: List[str]):
        curr_from_head = self.book_cache.get_head()
        curr_from_tail = self.book_cache.get_tail()
        for i, isbn in enumerate(expected_keys):
            self.assertEqual(self.book_cache.get_book_val(isbn), get_book_info(self.books_json, isbn))  # check hashmap
            self.assertEqual(curr_from_head.next.key, isbn)  # check list from head to tail
            # check list from tail to head
            self.assertEqual(curr_from_tail.prev.key, expected_keys[len(expected_keys) - (i + 1)])
            curr_from_head = curr_from_head.next
            curr_from_tail = curr_from_tail.prev
        self.assertEqual(len(self.book_cache.get_map()), len(expected_keys))  # check hashmap elements

    def insert_books(self, isbns: List[str]):
        for isbn in isbns:
            book = get_book_info(self.books_json, isbn)
            self.book_cache.put(isbn, book)

    def test_single_insert(self):
        isbn = ['1234']
        self.insert_books(isbn)
        self.assert_list_and_map(isbn)

    def test_repeat_insert(self):
        isbns = ['1234', '1235', '1236', '1234']
        self.insert_books(isbns)
        expected = ['1234', '1236', '1235']
        self.assert_list_and_map(expected)

    def test_full_cap_insert(self):
        isbns = ['1234', '1235', '1236']
        self.insert_books(isbns)
        expected = isbns[::-1]
        self.assert_list_and_map(expected)

    def test_get(self):
        isbns = ['1234', '1235', '1236']
        self.insert_books(isbns)

        self.assertEqual(self.book_cache.get('1234'), get_book_info(self.books_json, '1234'))
        expected = ['1234', '1236', '1235']
        self.assert_list_and_map(expected)

    def test_over_cap_insert(self):
        isbns = ['1234', '1235', '1236', '1237', '1238']
        self.insert_books(isbns)

        expected = ['1238', '1237', '1236']
        self.assert_list_and_map(expected)

    def test_muli_gets(self):
        isbns = ['1234', '1235', '1236']
        self.insert_books(isbns)

        self.assertEqual(self.book_cache.get('1234'), get_book_info(self.books_json, '1234'))
        expected = ['1234', '1236', '1235']
        self.assert_list_and_map(expected)

        self.assertEqual(self.book_cache.get('1234'), get_book_info(self.books_json, '1234'))
        expected = ['1234', '1236', '1235']
        self.assert_list_and_map(expected)

        self.assertEqual(self.book_cache.get('1235'), get_book_info(self.books_json, '1235'))
        expected = ['1235', '1234', '1236']
        self.assert_list_and_map(expected)

        self.assertEqual(self.book_cache.get('1236'), get_book_info(self.books_json, '1236'))
        expected = ['1236', '1235', '1234']
        self.assert_list_and_map(expected)

    def test_not_exist_get(self):
        isbns = ['1234', '1235', '1236']
        self.insert_books(isbns)

        self.assertEqual(self.book_cache.get('1237'), {})
        expected = isbns[::-1]
        self.assert_list_and_map(expected)

        isbns = ['1238', '1239']
        self.insert_books(isbns)
        self.assertEqual(self.book_cache.get('1234'), {})
        expected = ['1239', '1238', '1236']
        self.assert_list_and_map(expected)

    def test_mix(self):
        isbns = ['1234', '1235', '1236', '1237', '1238']
        self.insert_books(isbns)

        expected = ['1238', '1237', '1236']
        self.assert_list_and_map(expected)

        self.assertEqual(self.book_cache.get('1236'), get_book_info(self.books_json, '1236'))
        expected = ['1236', '1238', '1237']
        self.assert_list_and_map(expected)

        self.assertEqual(self.book_cache.get('1238'), get_book_info(self.books_json, '1238'))
        expected = ['1238', '1236', '1237']
        self.assert_list_and_map(expected)

        isbns = ['1239', '1234', '1240']
        self.insert_books(isbns)

        expected = isbns[::-1]
        self.assert_list_and_map(expected)

        self.assertEqual(self.book_cache.get('1238'), {})
        self.assert_list_and_map(expected)

        isbns = ['1239', '1234']
        self.insert_books(isbns)

        expected = ['1234', '1239', '1240']
        self.assert_list_and_map(expected)

        isbns = ['1234', '1235', '1236', '1237', '1238', '1234', '1236']
        self.insert_books(isbns)

        expected = ['1236', '1234', '1238']
        self.assert_list_and_map(expected)

        self.assertEqual(self.book_cache.get('1238'), get_book_info(self.books_json, '1238'))
        expected = ['1238', '1236', '1234']
        self.assert_list_and_map(expected)


if __name__ == '__main__':
    unittest.main()
