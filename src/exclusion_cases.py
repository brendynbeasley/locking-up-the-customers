"""The theory run on the exclusive-dealing cases people know: Dentsply, McWane, Eaton, Syngenta/Corteva.

For each case this script lines up (1) facts from the court or agency record, written as constants
below with their sources, (2) the Census 2022 figures for the seller's industry and, where one fits,
the buyers' industry, and (3) what the Rasmusen-Ramseyer-Wiley / Segal-Whinston model needs to be
true for exclusion to pay with that many buyers. It also asks whether the four sellers' industries
sit unusually high in the distribution of rival scale computed by naked_exclusion.py.

Run src/naked_exclusion.py first; this reads results/industries_2022.csv.

Usage (from the repository root):
    python src/exclusion_cases.py
"""

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import naked_exclusion as ne  # noqa: E402

# Facts from the record. Sources:
#   Dentsply: Brief for the United States in Opposition, Dentsply Int'l v. United States, No. 05-337
#     (U.S. 2005), pp. 3-5, summarizing the district court's findings; United States v. Dentsply
#     Int'l, 399 F.3d 181 (3d Cir. 2005).
#   McWane: McWane, Inc. v. FTC, 783 F.3d 814 (11th Cir. 2015), slip op. pp. 6-10 and 44-46.
#   Eaton: ZF Meritor, LLC v. Eaton Corp., 696 F.3d 254 (3d Cir. 2012), Parts I.A-C and III.
#   Syngenta/Corteva: FTC press release, September 29, 2022 (ftc.gov/node/79719).
CASES = [
    dict(case="Dentsply (artificial teeth)", year="2005", seller_naics="339114", buyer_naics="423450",
         buyers_in_record=23, buyers_described="23 national and regional dental dealers",
         incumbent_share="75-80% of revenue", rival_shares="Ivoclar 5%, Vita 3%",
         lock_up="dealers barred from adding rival tooth lines (Dealer Criterion 6, 1993)",
         payment_to_buyers="none; threat of losing the Dentsply line"),
    dict(case="McWane (domestic pipe fittings)", year="2015", seller_naics="331511", buyer_naics="",
         buyers_in_record=np.nan, buyers_described="waterworks distributors; HD Supply and Ferguson about 50-60%",
         incumbent_share="100% of domestic-only fittings, 2006-09; about 90% in 2011",
         rival_shares="Star about 5% (2010), just under 10% (2011)",
         lock_up="rebates withheld from distributors buying rival domestic fittings",
         payment_to_buyers="rebates conditioned on buying only from McWane"),
    dict(case="Eaton (heavy truck transmissions)", year="2012", seller_naics="336350", buyer_naics="336120",
         buyers_in_record=4, buyers_described="Freightliner, International, PACCAR, Volvo",
         incumbent_share="above 80%, 2000-07", rival_shares="Meritor 17% (1999), 4% (2005), exit 2007",
         lock_up="rebates for buying 70-78% (Volvo) up to 87-97.5% (International) from Eaton",
         payment_to_buyers="rebates; up-front payments of $2.5M (International) and $1M (PACCAR)"),
    dict(case="Syngenta and Corteva (crop protection)", year="2022", seller_naics="325320",
         buyer_naics="424910", buyers_in_record=np.nan, buyers_described="pesticide distributors",
         incumbent_share="not stated in release", rival_shares="generic makers of six active ingredients",
         lock_up="distributor payments only if purchases of generics stay below a low threshold",
         payment_to_buyers="loyalty payments (alleged; case filed with 10 states)"),
]
# Share of the market left open to Eaton's rivals by 2003, per plaintiffs' expert (ZF Meritor, Part III).
EATON_OPEN_SHARE_2003 = 0.15
# Random draws for the rank test.
N_DRAWS = 200_000
SEED = 1991


def buyer_industry(table, naics):
    """Census firm count and top-4 / top-8 share for a buyer industry (any sector)."""
    df = table[(table.GEOTYPE == "01") & (table.TYPOP == "00") & (table.NAICS2022 == naics)].set_index("CONCENFI")
    pct = pd.to_numeric(df.VAL_PCT, errors="coerce")
    return dict(buyer_label=df.loc["001", "NAICS2022_LABEL"], buyer_firms=int(df.loc["001", "FIRM"]),
                buyer_cr4=pct.get("604"), buyer_cr8=pct.get("608"))


def need_for_exclusion(n_buyers, r=ne.R_LINEAR):
    """Fewest buyers the rival must need for exclusion to be the sure outcome with n equal buyers.

    Simultaneous offers with full compensation: signing N* = n - need + 1 must cost no more than the
    profit protected, N* <= r n. Sequential offers: n <= M(need - 1), from naked_exclusion.py."""
    simult = n_buyers - math.floor(r * n_buyers + 1e-9) + 1
    seq = next(k for k in range(2, n_buyers + 1) if n_buyers <= ne.max_customers_sequential(k - 1, r)[0])
    return simult, seq


def main():
    ind = pd.read_csv(ne.OUT / "industries_2022.csv", dtype={"naics": str}).set_index("naics")
    ne.log(f"loaded results/industries_2022.csv: {len(ind)} industries")
    ind["scale_pctile"] = 100 * ind.m_leader_plant.rank(pct=True)

    conc = ne.read_census_zip("EC2200SIZECONCEN")
    rows = []
    for c in CASES:
        s = ind.loc[c["seller_naics"]]
        row = dict(case=c["case"], decided_or_filed=c["year"], seller_naics=c["seller_naics"],
                   seller_industry=s.label, seller_cr4=s.cr4, seller_firms=int(s.firms),
                   rival_scale_leader_plant_pct=round(100 * s.m_leader_plant, 2),
                   rival_scale_percentile=round(s.scale_pctile, 1),
                   lock_up_share_pct=round(100 * s.lock_up_share, 1),
                   min_customers_sequential=int(s.min_customers_sequential),
                   buyers_described=c["buyers_described"], buyers_in_record=c["buyers_in_record"],
                   incumbent_share=c["incumbent_share"], rival_shares=c["rival_shares"],
                   lock_up=c["lock_up"], payment_to_buyers=c["payment_to_buyers"])
        if c["buyer_naics"]:
            row.update(buyer_naics=c["buyer_naics"], **buyer_industry(conc, c["buyer_naics"]))
        n = c["buyers_in_record"]
        if pd.notna(n):
            simult, seq = need_for_exclusion(int(n))
            row.update(rival_must_need_simultaneous=simult, rival_must_need_sequential=seq,
                       rival_must_need_sequential_pct=round(100 * seq / n, 1))
        rows.append(row)
    cases = pd.DataFrame(rows)
    cases.to_csv(ne.OUT / "cases.csv", index=False)
    ne.log("\nCases:")
    ne.log(cases[["case", "seller_cr4", "rival_scale_leader_plant_pct", "rival_scale_percentile",
                  "min_customers_sequential", "buyers_in_record", "rival_must_need_simultaneous",
                  "rival_must_need_sequential"]].to_string(index=False))

    # How many buyers must a rival need, for markets with a given number of equal buyers?
    grid = []
    for n in (2, 3, 4, 6, 8, 10, 15, 23, 50, 100, 1000, 4928):
        simult, seq = need_for_exclusion(n)
        grid.append(dict(buyers=n, rival_must_need_simultaneous=simult,
                         simultaneous_share_pct=round(100 * simult / n, 1),
                         rival_must_need_sequential=seq, sequential_share_pct=round(100 * seq / n, 2),
                         no_natural_monopoly_ok=seq <= n / 2))
    grid = pd.DataFrame(grid)
    grid.to_csv(ne.OUT / "buyers_grid.csv", index=False)
    ne.log("\nBuyers needed by the rival before exclusion is the sure outcome (linear demand):")
    ne.log(grid.to_string(index=False))

    # Rank test: are the four sellers' industries unusually high in rival scale?
    pct = ind.scale_pctile.to_numpy()
    observed = cases.rival_scale_percentile.mean()
    rng = np.random.default_rng(SEED)
    draws = np.array([rng.choice(pct, size=len(cases), replace=False).mean() for _ in range(N_DRAWS)])
    p_upper = (draws >= observed).mean()
    test = pd.DataFrame([dict(cases=len(cases), mean_percentile=round(observed, 1),
                              mean_percentile_if_random=round(draws.mean(), 1),
                              p_value_one_sided=round(p_upper, 3), draws=N_DRAWS,
                              eaton_open_share_2003_pct=100 * EATON_OPEN_SHARE_2003,
                              eaton_industry_lock_up_needed_pct=cases.lock_up_share_pct.iloc[2])])
    test.to_csv(ne.OUT / "cases_rank_test.csv", index=False)
    ne.log("\nRank test of the case industries' rival scale:")
    ne.log(test.to_string(index=False))
    ne.log("\nwrote results/cases.csv, buyers_grid.csv, cases_rank_test.csv")


if __name__ == "__main__":
    main()
