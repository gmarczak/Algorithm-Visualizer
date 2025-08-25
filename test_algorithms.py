
import random
import pytest

from algorithms import bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort

ALGORITHMS = [bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort]

@pytest.mark.parametrize("algo", ALGORITHMS)
def test_sorts_random_arrays(algo):
    random.seed(0)
    arr = [random.randint(0, 1000) for _ in range(128)]
    expected = sorted(arr)
    gen = algo(arr)
    for _ in gen:
        pass
    assert arr == expected

def test_small_arrays_edge_cases():
    for base in ([], [1]):
        for algo in ALGORITHMS:
            arr = base.copy()
            gen = algo(arr)
            for _ in gen:
                pass
            assert arr == sorted(base)
