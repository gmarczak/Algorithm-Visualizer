
import time
from typing import Callable, Dict, Generator, List, Tuple
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from algorithms import bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort
from utils import make_random_array

ALGORITHMS: Dict[str, Tuple[str, Callable[[List[int]], Generator[dict, None, None]]]] = {
    "quick": ("Quick Sort", quick_sort),
    "merge": ("Merge Sort", merge_sort),
    "insertion": ("Insertion Sort", insertion_sort),
    "selection": ("Selection Sort", selection_sort),
    "bubble": ("Bubble Sort", bubble_sort),
}

st.set_page_config(
    page_title="Algorithm Visualizer (Python)",
    page_icon="🧩",
    layout="wide"
)

st.sidebar.title("⚙️ Ustawienia")
algo_key = st.sidebar.selectbox("Algorytm", list(ALGORITHMS.keys()), format_func=lambda k: ALGORITHMS[k][0], index=0)
n = st.sidebar.slider("Rozmiar tablicy", min_value=5, max_value=200, value=50, step=1)
vmin, vmax = st.sidebar.slider("Zakres wartości", min_value=5, max_value=1000, value=(5, 300), step=5)
speed = st.sidebar.slider("Prędkość (kroków/sek)", min_value=1, max_value=100, value=60)
seed = st.sidebar.number_input("Ziarno losowe (dla powtarzalności)", min_value=0, value=0, step=1)

st.sidebar.caption("Wskazówka: przy większym rozmiarze zwiększ prędkość i wybierz Quick/Merge.")

if "arr" not in st.session_state or st.session_state.get("last_seed") != seed or st.session_state.get("last_n") != n or st.session_state.get("last_range") != (vmin, vmax):
    st.session_state.arr = make_random_array(n, vmin, vmax, seed)
    st.session_state.last_seed = seed
    st.session_state.last_n = n
    st.session_state.last_range = (vmin, vmax)

if "running" not in st.session_state:
    st.session_state.running = False
if "stop" not in st.session_state:
    st.session_state.stop = False

st.title("Algorithm Visualizer (Python + Streamlit)")
st.write("Sortowanie z animacjami, kontrolą prędkości i statystykami.")

col_a, col_b, col_c, col_d = st.columns([1,1,1,1])
with col_a:
    if st.button("▶️ Start", disabled=st.session_state.running):
        st.session_state.running = True
        st.session_state.stop = False
with col_b:
    if st.button("⏹️ Stop", disabled=not st.session_state.running):
        st.session_state.stop = True
with col_c:
    if st.button("🎲 Losuj tablicę", disabled=st.session_state.running):
        st.session_state.arr = make_random_array(n, vmin, vmax, seed)
with col_d:
    st.write("")

stats_container = st.container()
chart_container = st.container()

def draw_bars(arr: List[int], highlights: Dict[str, List[int]]):
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(arr))
    bars = ax.bar(x, arr)

    compare = set(highlights.get("compare", []))
    swap = set(highlights.get("swap", []))
    pivot = set(highlights.get("pivot", []))
    sorted_idx = set(highlights.get("sorted", []))

    for idx, bar in enumerate(bars):
        if idx in sorted_idx:
            bar.set_color("#10b981")
        elif idx in pivot:
            bar.set_color("#22d3ee")
        elif idx in swap:
            bar.set_color("#ef4444")
        elif idx in compare:
            bar.set_color("#f59e0b")
        else:
            bar.set_color("#6366f1")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, len(arr)-0.5)
    ax.set_title(ALGORITHMS[algo_key][0])
    ax.set_facecolor("#111827")
    fig.patch.set_facecolor("#0F172A")
    chart_container.pyplot(fig, clear_figure=True)

def run_visualization():
    arr = st.session_state.arr.copy()
    gen = ALGORITHMS[algo_key][1](arr)
    comparisons = 0
    swaps = 0
    sorted_set = set()
    t0 = time.perf_counter()
    delay = max(0.004, (1 - (speed/100))**2 * 0.6)

    for step in gen:
        if st.session_state.stop:
            break

        highlights = {"compare": [], "swap": [], "pivot": [], "sorted": list(sorted_set)}
        if step["type"] == "compare":
            comparisons += 1
            i, j = step["i"], step["j"]
            highlights["compare"] = [i, j]
        elif step["type"] == "swap":
            swaps += 1
            i, j = step["i"], step["j"]
            arr[i], arr[j] = arr[j], arr[i]
            highlights["swap"] = [i, j]
        elif step["type"] == "set":
            i, val = step["i"], step["val"]
            arr[i] = val
            highlights["compare"] = [i]
        elif step["type"] == "pivot":
            k = step["k"]
            highlights["pivot"] = [k] if k is not None else []
        elif step["type"] == "sorted":
            k = step["k"]
            sorted_set.add(k)
            highlights["sorted"] = list(sorted_set)

        draw_bars(arr, highlights)
        with stats_container:
            st.markdown(
                f"**Porównania:** {comparisons} &nbsp;&nbsp; **Zamiany:** {swaps} &nbsp;&nbsp; **Czas:** {(time.perf_counter()-t0):.2f}s"
            )
        time.sleep(delay)

    sorted_set = set(range(len(arr)))
    draw_bars(arr, {"sorted": list(sorted_set)})
    with stats_container:
        st.markdown(
            f"**Porównania:** {comparisons} &nbsp;&nbsp; **Zamiany:** {swaps} &nbsp;&nbsp; **Czas:** {(time.perf_counter()-t0):.2f}s"
        )
    st.session_state.arr = arr

draw_bars(st.session_state.arr, {"compare": [], "swap": [], "pivot": [], "sorted": []})

if st.session_state.running and not st.session_state.stop:
    run_visualization()
    st.session_state.running = False
    st.session_state.stop = False
