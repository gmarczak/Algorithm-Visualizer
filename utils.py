
from typing import List
import random

def make_random_array(n: int, vmin: int, vmax: int, seed: int | None = None) -> List[int]:
    if seed is not None:
        random.seed(seed)
    return [random.randint(vmin, vmax) for _ in range(n)]
