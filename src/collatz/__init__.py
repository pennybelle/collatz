import matplotlib.pyplot as plt
from time import time


class collatz(dict):  # subclass dict is used as cache
    def __getitem__(self, x):
        value = self.get(
            x, None
        )  # value (v) is cache dict[x] if not None else dict[x] = None

        if value:
            return value  # if x is in cache return value at key x

        value = self.calc_seq(x)  # else set value using conjecture function
        self[x] = value  # then fill cache dict[x] with value (v)

        return value  # return value of cache dict[x]

    def calc_seq(self, x, steps=0):
        if x == 1:
            return steps  # guard clause

        x = x // 2 if x % 2 == 0 else x * 3 + 1  # conjecture function
        steps += 1  # sequence length tracker

        value = self.get(x, None)  # v is class dict[x] if not None else dict[x] = None
        if value is None:
            return self.calc_seq(x, steps)  # if x not in cache, recurse

        return steps + value  # else return tracker + cached seq length for v


def plotter(
    title,
    x,
    y,
    x_label,
    y_label,
    marker=".",
    markersize=1,
    linestyle="",
):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x, y, marker, markersize, linestyle)
    collatz().clear()  # redundant data dump
    plt.savefig(title + ".png")
    plt.show()


def run_val(start_val, stop_val):  # run conjecture in range of i & j
    print("Running Calculations...")

    cache = collatz()  # set class dict to var for reference
    timer_start = time()  # timer
    for x in range(start_val, stop_val + 1):
        cache[x]  # fill cache.dict[i through j+1]
    time_taken = time() - timer_start  # timer results

    print(f"Calculation duration: {time_taken:.2f} sec")

    return cache, time_taken  # return cache dict for reference as well as timer results


def plot_seq_len(start_val, stop_val):
    cache, time_taken = run_val(
        start_val, stop_val
    )  # referencing collatz dict to var & fills cache
    title = f"Collatz Sequence Length Analysis [{start_val:,}, {stop_val:,}] {time_taken:.0f}secs"
    x_label = "Sequence Length"
    y_label = "Frequency"
    points = {}  # local cache for frequency analysis of sequence lengths in cache.dict.values

    for value in cache.values():
        points[value] = points.setdefault(value, 0) + 1  # seq freq analysis algo

    cache.clear()  # dump cache
    plotter(
        title, points.keys(), points.values(), x_label, y_label
    )  # plot results on graph


def plot_collatz_graph(start_val, stop_val):
    cache, time_taken = run_val(start_val, stop_val)
    title = f"Collatz Conjecture [{start_val:,} - {stop_val:,}] {time_taken:.0f} secs"
    x_label = "X"
    y_label = "Sequence Length for X"

    plotter(title, cache.keys(), cache.values(), x_label, y_label, marker=",")


def main():
    user_choice = input("""
    Choose Plot Type ():
        [c] Original Collatz Conjecture
        [s] Sequence Frequency Analysis
    """).lower()

    if user_choice == "c":
        plot_collatz_graph(int(input("Start Value: ")), int(input("Stop Value: ")))

    if user_choice == "s":
        plot_seq_len(int(input("Start Value: ")), int(input("Stop Value: ")))
