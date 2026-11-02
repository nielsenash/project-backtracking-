import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def main():

    filename = "_bssf_runtimes.json"

    with open(filename, "r") as f:
        bssf_runtimes = json.load(f)

    filename = "_backtracking_runtimes.json"

    with open(filename, "r") as f:
        backtracking_runtimes = json.load(f)

    g_NN, g_times = zip(*bssf_runtimes)
    g_nn = [n[0] for n in g_NN]

    b_NN, b_times = zip(*backtracking_runtimes)
    b_nn = [n[0] for n in b_NN]

    fig = plt.figure()
    plt.scatter(g_nn, g_times, marker="o")
    plt.plot(g_nn, g_times, c="k", lw=2, label="BSSF")

    plt.scatter(b_nn, b_times, marker="o")
    plt.plot(b_nn, b_times, c="r", lw=2, label="Backtracking")

    plt.legend()
    plt.xlabel("n")
    plt.ylabel("Runtime (sec)")
    plt.title("BSSF vs. Backtracking Runtime")

    fig.show()
    fig.savefig("bssf_v_backtracking.svg")


if __name__ == "__main__":
    main()
