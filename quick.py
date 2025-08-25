
from typing import Generator, List, Dict, Any

def quick_sort(arr: List[int]) -> Generator[Dict[str, Any], None, None]:
    def partition(lo: int, hi: int) -> Generator[Dict[str, Any], int, None]:
        pivot = arr[hi]
        yield {"type": "pivot", "k": hi}
        i = lo
        for j in range(lo, hi):
            yield {"type": "compare", "i": j, "j": hi}
            if arr[j] < pivot:
                if i != j:
                    yield {"type": "swap", "i": i, "j": j}
                    arr[i], arr[j] = arr[j], arr[i]
                i += 1
        yield {"type": "swap", "i": i, "j": hi}
        arr[i], arr[hi] = arr[hi], arr[i]
        yield {"type": "pivot", "k": None}
        return i

    def sort(lo: int, hi: int):
        if lo >= hi:
            if lo == hi:
                yield {"type": "sorted", "k": lo}
            return
        p = yield from partition(lo, hi)
        yield {"type": "sorted", "k": p}
        yield from sort(lo, p - 1)
        yield from sort(p + 1, hi)

    yield from sort(0, len(arr) - 1)
    for k in range(len(arr)):
        yield {"type": "sorted", "k": k}
