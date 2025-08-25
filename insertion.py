
from typing import Generator, List, Dict, Any

def insertion_sort(arr: List[int]) -> Generator[Dict[str, Any], None, None]:
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            yield {"type": "compare", "i": j, "j": j + 1}
            if arr[j] > key:
                arr[j + 1] = arr[j]
                yield {"type": "set", "i": j + 1, "val": arr[j + 1]}
                j -= 1
            else:
                break
        arr[j + 1] = key
        yield {"type": "set", "i": j + 1, "val": key}
    for k in range(n):
        yield {"type": "sorted", "k": k}
