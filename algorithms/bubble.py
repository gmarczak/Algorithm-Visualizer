
from typing import Generator, List, Dict, Any

def bubble_sort(arr: List[int]) -> Generator[Dict[str, Any], None, None]:
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            yield {"type": "compare", "i": j, "j": j + 1}
            if arr[j] > arr[j + 1]:
                yield {"type": "swap", "i": j, "j": j + 1}
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        yield {"type": "sorted", "k": n - i - 1}
        if not swapped:
            break
    for k in range(max(0, n - i - 1)):
        yield {"type": "sorted", "k": k}
