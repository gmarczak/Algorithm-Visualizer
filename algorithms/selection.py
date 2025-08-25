
from typing import Generator, List, Dict, Any

def selection_sort(arr: List[int]) -> Generator[Dict[str, Any], None, None]:
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            yield {"type": "compare", "i": min_idx, "j": j}
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            yield {"type": "swap", "i": i, "j": min_idx}
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield {"type": "sorted", "k": i}
    yield {"type": "sorted", "k": n - 1}
