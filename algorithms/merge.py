
from typing import Generator, List, Dict, Any

def merge_sort(arr: List[int]) -> Generator[Dict[str, Any], None, None]:
    aux = arr.copy()

    def merge(lo: int, mid: int, hi: int):
        for k in range(lo, hi + 1):
            aux[k] = arr[k]
        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if i > mid:
                arr[k] = aux[j]; j += 1
                yield {"type": "set", "i": k, "val": arr[k]}
            elif j > hi:
                arr[k] = aux[i]; i += 1
                yield {"type": "set", "i": k, "val": arr[k]}
            else:
                yield {"type": "compare", "i": i, "j": j}
                if aux[j] < aux[i]:
                    arr[k] = aux[j]; j += 1
                else:
                    arr[k] = aux[i]; i += 1
                yield {"type": "set", "i": k, "val": arr[k]}

    def sort(lo: int, hi: int):
        if hi <= lo:
            return
        mid = (lo + hi) // 2
        yield from sort(lo, mid)
        yield from sort(mid + 1, hi)
        yield from merge(lo, mid, hi)

    yield from sort(0, len(arr) - 1)

    for k in range(len(arr)):
        yield {"type": "sorted", "k": k}
