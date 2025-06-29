from django.test import SimpleTestCase
from posts.utils import bubble_sort, binary_search

class UtilsTest(SimpleTestCase):

    def test_bubble_sort_numbers(self):
        data = [5, 1, 4, 2, 3]
        self.assertEqual(bubble_sort(data), [1, 2, 3, 4, 5])
        self.assertEqual(bubble_sort(data, reverse=True), [5, 4, 3, 2, 1])

    def test_bubble_sort_objects(self):
        objs = [{"id": 2}, {"id": 1}, {"id": 3}]
        sorted_objs = bubble_sort(objs, key=lambda o: o["id"])
        self.assertEqual([o["id"] for o in sorted_objs], [1, 2, 3])

    def test_binary_search_found(self):
        data = bubble_sort([5, 1, 4, 2, 3])
        self.assertEqual(binary_search(data, 4), 4)

    def test_binary_search_not_found(self):
        data = [1, 2, 3]
        self.assertIsNone(binary_search(data, 10))
