"""Naked exclusion (Rasmusen, Ramseyer & Wiley 1991; Segal & Whinston 2000) on 2022 US manufacturing.

Part 1 reproduces the paper's own arithmetic: the abstract's 100 customers with a minimum efficient
scale of 15 (lock up 86), and the Section IV numerical example (N = 100, N* = 90, profit 10, customer
loss 14), solved by backward induction.

Part 2 measures the two things the theory turns on for every 6-digit manufacturing industry in the
2022 Economic Census: the share of the national market a rival needs to reach minimum efficient scale
(m), and the ratio of the incumbent's monopoly profit to each customer's loss (r = pi / X*). It then
asks, industry by industry, (a) what share of demand an incumbent must lock up (1 - m), (b) whether
exclusion pays even when every needed customer is paid in full (simultaneous offers: 1 - m <= r), and
(c) how many separately approached customers the market needs before one-at-a-time offers make
exclusion free (sequential offers).

Usage (from the repository root):
    python src/naked_exclusion.py
Reads data/raw/*.zip (committed). Writes results/*.csv and results/*.png.
"""

import io
import math
import zipfile
from fractions import Fraction
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

# Linear demand: monopoly profit is 2/3 of the surplus a customer loses to monopoly pricing
# (profit = (a-c)^2/4b, lost surplus = 3(a-c)^2/8b). The paper's own example uses 10/14 = 0.714.
R_LINEAR = 2 / 3
# The paper's abstract example and its Section IV numerical example (RRW 1991, pp. 1137 and 1142).
ABSTRACT_N, ABSTRACT_MES = 100, 15
EXAMPLE_N, EXAMPLE_NSTAR, EXAMPLE_PI, EXAMPLE_X = 100, 90, 10, 14
# The paper's illustrative minimum efficient scale, as a share of the market.
RRW_MES_SHARE = 0.15
# Courts' usual foreclosure benchmark for exclusive dealing: "roughly 40% or 50%"
# (United States v. Microsoft, 253 F.3d 34, 70 (D.C. Cir. 2001), quoted in McWane v. FTC (11th Cir. 2015)).
FORECLOSURE_BENCHMARKS = (0.40, 0.50)
# Industries whose national figures badly understate local market shares (same judgment list as
# brendynbeasley/bain-1951-revisited): bakeries, fluid milk, ice, printing, asphalt, brick, cement, concrete.
LOCAL_MARKET_NAICS = {"311811", "311812", "311511", "312113", "323111", "324121", "327121",
                      "327310", "327320", "327331", "327332", "327390"}
# County Business Patterns employment-size classes, smallest to largest.
CBP_CLASSES = ["<5", "5_9", "10_19", "20_49", "50_99", "100_249", "250_499", "500_999", "1000"]


def log(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------------------
# The theory
# ---------------------------------------------------------------------------

def signers_needed(n_customers, mes_customers):
    """Customers the incumbent must sign so the free ones fall short of the rival's scale."""
    return n_customers - mes_customers + 1


def sequential_game(n, n_star, pi, x):
    """Backward induction for RRW Section IV: customers asked one at a time, decisions public.

    State is (signed, remaining). A customer whose refusal would not stop exclusion signs for
    nothing; a crucial one must be paid x. The incumbent keeps paying while the profit at stake,
    pi from each customer not already signed (RRW p. 1142: signed customers "are not free to go to
    the entrant anyway"), covers the payments still to come. Returns (exclusion succeeds, payments
    made on the equilibrium path).
    """
    ok = np.zeros((n + 1, n + 1), dtype=bool)
    cost = np.zeros((n + 1, n + 1))
    for t in range(n + 1):
        for s in range(n - t, -1, -1):
            if s >= n_star:
                ok[s, t] = True
            elif s + t < n_star or t == 0:
                ok[s, t] = False
            elif ok[s, t - 1]:                       # refusal would not matter: signs for zero
                ok[s, t], cost[s, t] = True, cost[s + 1, t - 1]
            elif ok[s + 1, t - 1] and pi * (n - s) >= x + cost[s + 1, t - 1]:
                ok[s, t], cost[s, t] = True, x + cost[s + 1, t - 1]
    return bool(ok[0, n]), float(cost[0, n])


def slack_frontier(j, r):
    """M(0), ..., M(j) for a rival that can lose j customers and survive (it needs j + 1).

    M(d) is the most customers still to be asked, with d further refusals tolerable, for which
    sequential offers still exclude. Payments are in units of X*, so each customer not yet signed
    is worth r = pi / X*. Recursion M(d) = floor(((j - d) r + 1 + M(d - 1)) / (1 - r)), M(-1) = -1.
    Exact arithmetic with fractions avoids rounding at the floor."""
    r = Fraction(r).limit_denominator(1000)
    m, out = -1, []
    for d in range(j + 1):
        m = math.floor(((j - d) * r + 1 + m) / (1 - r))
        out.append(m)
    return out


def max_customers_sequential(j, r):
    """(most customers for which sequential offers exclude, most for which they exclude at zero
    cost) when the rival needs j + 1 customers. Payments start once N exceeds M(j - 1) + 1."""
    if j < 1:
        return 0, 0
    m = slack_frontier(j, r)
    return m[j], m[j - 1] + 1


def min_customers_sequential(m, r, free=False):
    """Smallest market size N such that one-at-a-time offers exclude, in every market of N or more
    equal customers, a rival that needs share m of them (with free=True, exclude without paying
    anyone). A market of N customers has a rival needing ceil(m*N); exclusion iff N <= M(need-1),
    and at zero cost iff N <= M(need-2) + 1. Markets just above a jump in ceil(m*N) can fail even
    when a smaller market succeeds, so the answer is one more than the largest failing N."""
    last_fail = math.floor(1 / m + 1e-9)            # a rival needing one customer is never excluded
    j = 1
    while True:
        hi = math.floor((j + 1) / m + 1e-9)          # largest N in which the rival needs j + 1
        most = max_customers_sequential(j, r)[1 if free else 0]
        if most < hi:
            last_fail = hi
        elif most > 100 * hi:                        # M grows geometrically in j, N only linearly
            return last_fail + 1
        j += 1


def profit_to_loss_ces(lerner):
    """pi / X* for constant-elasticity demand when the monopoly markup (p - c)/p equals `lerner`."""
    eps = 1 / lerner
    return lerner * (eps - 1) / ((1 - lerner) ** (1 - eps) - 1)


# ---------------------------------------------------------------------------
# Part 1: the paper's own numbers
# ---------------------------------------------------------------------------

def paper_examples():
    rows = []
    n_s = signers_needed(ABSTRACT_N, ABSTRACT_MES)
    rows.append(("Abstract: customers the incumbent must sign (N=100, MES=15)", n_s, "86"))
    total = EXAMPLE_N * EXAMPLE_PI
    rows.append(("Sec. IV: monopoly profit from all customers (N*pi)", total, "1,000"))
    rows.append(("Sec. IV: cost of paying N* customers in full (N* X*)", EXAMPLE_NSTAR * EXAMPLE_X, "1,260"))
    rows.append(("Sec. IV: most customers worth paying in full (floor(N pi / X*))",
                 total // EXAMPLE_X, "71"))
    rows.append(("Sec. IV: cost of paying 71 customers", (total // EXAMPLE_X) * EXAMPLE_X, "994"))
    ok, cost = sequential_game(EXAMPLE_N, EXAMPLE_NSTAR, EXAMPLE_PI, EXAMPLE_X)
    rows.append(("Sec. IV: sequential offers exclude? (1 = yes)", int(ok), "yes"))
    rows.append(("Sec. IV: total paid under sequential offers", cost, "0"))
    rows.append(("Simultaneous offers exclude for sure? (N* X* <= N pi, 1 = yes)",
                 int(EXAMPLE_NSTAR * EXAMPLE_X <= total), "no (two equilibria)"))
    rows.append(("Profit-to-loss ratio in the example (pi / X*)", EXAMPLE_PI / EXAMPLE_X, "10/14"))
    rows.append(("Profit-to-loss ratio, linear demand", R_LINEAR, "derived"))
    df = pd.DataFrame(rows, columns=["quantity", "computed", "paper"])
    log("\nPart 1: the paper's arithmetic")
    log(df.to_string(index=False))

    # Check the closed-form frontier against brute-force backward induction on small markets,
    # for both the paper's ratio (10/14) and the linear-demand ratio (2/3 as pi = 2, X* = 3).
    mismatches = 0
    for pi, x in ((EXAMPLE_PI, EXAMPLE_X), (2, 3)):
        for n in range(2, 61):
            for need in range(1, n + 1):
                ok, paid = sequential_game(n, signers_needed(n, need), pi, x)
                most, most_free = max_customers_sequential(need - 1, pi / x)
                expected_paid = x * max(0, n - most_free) if n <= most else 0
                mismatches += (ok != (n <= most)) or (paid != expected_paid)
    log(f"frontier check against backward induction, N = 2..60, two ratios: {mismatches} mismatches")
    return df


def frontier_table():
    rows = []
    for r in (0.5, R_LINEAR, EXAMPLE_PI / EXAMPLE_X):
        for j in range(1, 13):
            most, most_free = max_customers_sequential(j, r)
            rows.append(dict(profit_to_loss=round(r, 4), rival_needs_customers=j + 1,
                             max_customers_sequential_excludes=most,
                             max_customers_sequential_excludes_free=most_free))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Part 2: Census data
# ---------------------------------------------------------------------------

def read_census_zip(name):
    with zipfile.ZipFile(RAW / f"{name}.zip") as z:
        raw = z.read(f"{name}.dat").decode("latin-1")
    df = pd.read_csv(io.StringIO(raw), sep="|", dtype=str, keep_default_na=False)
    df.columns = [c.lstrip("#") for c in df.columns]
    log(f"loaded {name}: {len(df):,} rows")
    return df


def num(df, col):
    return pd.to_numeric(df[col], errors="coerce")


def load_concentration():
    df = read_census_zip("EC2200SIZECONCEN")
    df = df[(df.GEOTYPE == "01") & (df.TYPOP == "00") & df.NAICS2022.str.fullmatch(r"3[1-3]\d{4}")]
    df = df.assign(rcp=num(df, "RCPTOT"), est=num(df, "ESTAB"), firm=num(df, "FIRM"),
                   pct=num(df, "VAL_PCT"), hhi=num(df, "HHI"))
    by = {c: df[df.CONCENFI == c].set_index("NAICS2022") for c in ("001", "604", "650")}
    out = pd.DataFrame({
        "label": by["001"].NAICS2022_LABEL,
        "shipments_musd": by["001"].rcp / 1000,
        "firms": by["001"].firm,
        "plants": by["001"].est,
        "cr4": by["604"].pct,
        "top4_plants": by["604"].est,
        "hhi50": by["650"].hhi.where(by["650"].hhi > 0),
    })
    log(f"manufacturing 6-digit industries in the concentration table: {len(out)}")
    return out


def load_value_added():
    df = read_census_zip("EC2200SIZEEMPEST")
    df = df[(df.GEOTYPE == "01") & (df.TYPOP == "00") & (df.EMPSZFE == "001")
            & df.NAICS2022.str.fullmatch(r"3[1-3]\d{4}")].set_index("NAICS2022")
    va, pay, rcp = num(df, "VALADD"), num(df, "PAYANN"), num(df, "RCPTOT")
    # Census price-cost margin (Collins & Preston): (value added - payroll) / shipments.
    return pd.DataFrame({"pcm": ((va - pay) / rcp).where((va > 0) & (rcp > 0))})


def load_midpoint_plant():
    """Midpoint plant: the size class holding the median worker; its average plant, as a share."""
    with zipfile.ZipFile(RAW / "cbp22us.zip") as z:
        df = pd.read_csv(z.open("cbp22us.txt"), dtype={"naics": str})
    log(f"loaded cbp22us: {len(df):,} rows")
    df = df[(df.lfo == "-") & df.naics.str.fullmatch(r"3[1-3]\d{4}")].set_index("naics")
    as_num = lambda cols: df[cols].apply(pd.to_numeric, errors="coerce").fillna(0).to_numpy(float)
    emp = as_num([f"e{c}" for c in CBP_CLASSES])   # "N" (not available) counts as zero
    est = as_num([f"n{c}" for c in CBP_CLASSES])
    total = emp.sum(axis=1)
    cum = emp.cumsum(axis=1) / total[:, None]
    k = (cum >= 0.5).argmax(axis=1)
    rows = np.arange(len(df))
    mid = emp[rows, k] / np.where(est[rows, k] > 0, est[rows, k], np.nan)
    return pd.DataFrame({"cbp_emp": total, "midpoint_plant_emp": mid,
                         "m_midpoint": mid / total}, index=df.index)


def build_industries():
    ind = load_concentration().join(load_value_added()).join(load_midpoint_plant())
    n0 = len(ind)
    ind = ind[(ind.top4_plants > 0) & ind.cr4.notna()]
    log(f"dropped {n0 - len(ind)} industries with suppressed top-4 plant counts")
    local = ind.index.isin(LOCAL_MARKET_NAICS)
    log(f"dropped {local.sum()} local-market industries (national shares understate local ones)")
    ind = ind[~local].copy()

    # Main measure: the average plant run by the four largest companies, as a share of the industry.
    ind["m_leader_plant"] = ind.cr4 / 100 / ind.top4_plants
    # Generous ceiling: the largest company's share can be no more than sqrt(HHI).
    ind["m_largest_firm_max"] = np.minimum(np.sqrt(ind.hhi50) / 100, ind.cr4 / 100)
    ind["lock_up_share"] = 1 - ind.m_leader_plant
    # The paper's framing: of 100 equal customers, how many must sign?
    ind["signers_of_100"] = ind.m_leader_plant.map(
        lambda m: signers_needed(100, math.ceil(100 * m - 1e-9)))
    ind["r_ces"] = ind.pcm.where((ind.pcm > 0.02) & (ind.pcm < 0.95)).map(
        lambda x: profit_to_loss_ces(x) if pd.notna(x) else np.nan)
    ind["pays_simultaneous_linear"] = ind.lock_up_share <= R_LINEAR
    ind["pays_simultaneous_ces"] = ind.lock_up_share <= ind.r_ces
    ind["min_customers_sequential"] = ind.m_leader_plant.map(lambda m: min_customers_sequential(m, R_LINEAR))
    ind["min_customers_sequential_free"] = ind.m_leader_plant.map(
        lambda m: min_customers_sequential(m, R_LINEAR, free=True))
    log(f"final sample: {len(ind)} industries, ${ind.shipments_musd.sum() / 1e6:.2f} trillion of shipments")
    return ind


def summarize(ind):
    w = ind.shipments_musd
    share = lambda mask: 100 * w[mask].sum() / w.sum()
    rows = []

    def add(label, value, unit=""):
        rows.append(dict(statistic=label, value=value, unit=unit))

    add("industries in sample", len(ind))
    add("shipments in sample", round(w.sum() / 1e6, 3), "trillion USD")
    for col, name in (("m_leader_plant", "leader plant"), ("m_midpoint", "midpoint plant"),
                      ("m_largest_firm_max", "largest firm, upper bound")):
        s = ind[col].dropna()
        add(f"median rival scale, {name}", round(100 * s.median(), 2), "% of national shipments")
        add(f"90th percentile rival scale, {name}", round(100 * s.quantile(0.9), 2), "% of national shipments")
        add(f"industries with rival scale >= 15% (paper's example), {name}", int((s >= RRW_MES_SHARE).sum()))
        add(f"industries with rival scale >= 1/3 (pays with full compensation), {name}",
            int((s >= 1 - R_LINEAR).sum()))
        add(f"industries measured, {name}", len(s))
    add("median share of demand to lock up (leader plant)", round(100 * ind.lock_up_share.median(), 1), "%")
    add("median customers to sign, of 100 (leader plant)", int(ind.signers_of_100.median()))
    for b in FORECLOSURE_BENCHMARKS:
        add(f"industries where lock-up share <= {int(b * 100)}%", int((ind.lock_up_share <= b).sum()))
    add("industries where exclusion pays with full compensation, linear demand",
        int(ind.pays_simultaneous_linear.sum()))
    add("industries where exclusion pays with full compensation, CES demand at Census margin",
        int(ind.pays_simultaneous_ces.sum()))
    add("median Census price-cost margin", round(100 * ind.pcm.median(), 1), "%")
    add("median profit-to-loss ratio, CES at Census margin", round(ind.r_ces.median(), 3))
    q = ind.min_customers_sequential
    add("median customers needed for one-at-a-time offers to exclude", int(q.median()))
    add("25th percentile customers needed", int(q.quantile(0.25)))
    add("75th percentile customers needed", int(q.quantile(0.75)))
    add("industries needing more than 1,000 customers", int((q > 1000).sum()))
    add("shipments share needing more than 1,000 customers", round(share(q > 1000), 1), "%")
    qf = ind.min_customers_sequential_free
    add("median customers needed for one-at-a-time offers to exclude at zero cost", int(qf.median()))
    add("25th percentile customers needed, zero cost", int(qf.quantile(0.25)))
    add("75th percentile customers needed, zero cost", int(qf.quantile(0.75)))
    add("industries needing more than 1,000 customers, zero cost", int((qf > 1000).sum()))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def figure_scale(ind):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bins = np.logspace(np.log10(0.0002), np.log10(0.6), 40)
    ax.hist(ind.m_leader_plant, bins=bins, color="#4C72B0", alpha=0.85, label="Leader plant")
    ax.hist(ind.m_midpoint.dropna(), bins=bins, histtype="step", color="#333333", lw=1.4,
            label="Midpoint plant (CBP)")
    ax.set_xscale("log")
    top = ax.get_ylim()[1]
    for x, txt, y in ((RRW_MES_SHARE, "Paper's\nexample:\n15%", 0.55),
                      (1 - R_LINEAR, "Pays even\nfully paid:\n33%", 0.85)):
        ax.axvline(x, color="#C44E52", ls="--", lw=1.2)
        ax.text(x * 1.08, top * y, txt, color="#C44E52", fontsize=8, va="top")
    ax.set_xticks([0.001, 0.01, 0.1, 0.5])
    ax.set_xticklabels(["0.1%", "1%", "10%", "50%"])
    ax.set_xlabel("Scale a rival needs, as a share of national shipments (log scale)")
    ax.set_ylabel("Manufacturing industries")
    ax.set_title("A single efficient plant is a small slice of almost every US market (2022)")
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "rival_scale_2022.png", dpi=150)
    plt.close(fig)


def figure_sequential(ind):
    ms = np.logspace(np.log10(0.0004), np.log10(0.3), 120)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for r, style, lab in ((R_LINEAR, "-", "Linear demand (profit = 2/3 of customer loss)"),
                          (0.5, "--", "Profit = 1/2 of customer loss")):
        ax.plot(ms, [min_customers_sequential(m, r) for m in ms], style, color="#333333", label=lab)
    ax.scatter(ind.m_leader_plant, ind.min_customers_sequential, s=10, color="#4C72B0", alpha=0.6,
               label="2022 manufacturing industries (linear)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([0.001, 0.003, 0.01, 0.03, 0.1, 0.3])
    ax.set_xticklabels(["0.1%", "0.3%", "1%", "3%", "10%", "30%"])
    ax.set_xlabel("Scale a rival needs, as a share of the market (log scale)")
    ax.set_ylabel("Fewest customers at which\none-at-a-time offers exclude")
    ax.set_title("Divide and conquer needs many separate customers")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "customers_needed_sequential.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    paper_examples().to_csv(OUT / "paper_examples.csv", index=False)
    frontier_table().to_csv(OUT / "sequential_frontier.csv", index=False)
    lerners = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    pd.DataFrame({"monopoly_markup": lerners, "profit_to_loss_ces": [profit_to_loss_ces(x) for x in lerners],
                  "profit_to_loss_linear": R_LINEAR}).round(4).to_csv(OUT / "profit_to_loss.csv", index=False)

    log("\nPart 2: 2022 Economic Census")
    ind = build_industries()
    cols = ["label", "shipments_musd", "firms", "plants", "cr4", "top4_plants", "hhi50", "pcm",
            "m_leader_plant", "m_midpoint", "m_largest_firm_max", "lock_up_share", "signers_of_100", "r_ces",
            "pays_simultaneous_linear", "pays_simultaneous_ces", "min_customers_sequential",
            "min_customers_sequential_free"]
    ind[cols].sort_values("m_leader_plant", ascending=False).round(5).to_csv(
        OUT / "industries_2022.csv", index_label="naics")
    summ = summarize(ind)
    summ.to_csv(OUT / "summary_2022.csv", index=False)
    log("\n" + summ.to_string(index=False))
    top = ind.sort_values("m_leader_plant", ascending=False).head(12)
    log("\nlargest rival scale (leader plant):")
    log(top[["label", "cr4", "top4_plants", "m_leader_plant", "min_customers_sequential"]].to_string())
    figure_scale(ind)
    figure_sequential(ind)
    log("\nwrote results/paper_examples.csv, sequential_frontier.csv, profit_to_loss.csv, "
        "industries_2022.csv, summary_2022.csv and two figures")


if __name__ == "__main__":
    main()
