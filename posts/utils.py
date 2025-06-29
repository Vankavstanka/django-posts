# Алгоритмы сортировки и поиска.
# Используются во views и тестируются в posts/tests.py

from typing import Iterable, Callable, TypeVar, List, Sequence

T = TypeVar("T")

def bubble_sort(items: Iterable[T],
                key: Callable[[T], object] = lambda x: x,
                reverse: bool = False) -> List[T]:
    # Пузырьковая сортировка
    items = list(items)                 
    n = len(items)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            a, b = key(items[j]), key(items[j + 1])
            if (a > b and not reverse) or (a < b and reverse):
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        if not swapped:                 
            break
    return items


def binary_search(sorted_items: Sequence[T],
                  target,
                  key: Callable[[T], object] = lambda x: x) -> T | None:
    # Бинарный поиск по уже отсортированным данным
    left, right = 0, len(sorted_items) - 1
    while left <= right:
        mid = (left + right) // 2
        current = key(sorted_items[mid])
        if current == target:
            return sorted_items[mid]
        if current < target:
            left = mid + 1
        else:
            right = mid - 1
    return None
