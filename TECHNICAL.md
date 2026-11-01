# Technical notes

This is the technical companion to the [README](README.md). It covers the original study, the data, the method,
the full set of results and how to reproduce them. Every table is in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

Eric B. Rasmusen, J. Mark Ramseyer and John S. Wiley Jr., "Naked Exclusion," *American Economic Review* 81(5),
December 1991, pp. 1137–1145. The model has $`N`$ identical buyers, an incumbent and an equally efficient entrant
whose average cost falls until output reaches a minimum efficient scale. The incumbent offers payments for
exclusive contracts before the entrant decides whether to enter. The headline, from the abstract, is that with 100
customers and a minimum efficient scale of 15, the incumbent need only lock up 86. Proposition 2 shows that with
simultaneous offers both exclusion and entry are equilibria unless paying $`X^*`$ to $`N^*`$ customers is
profitable ($`N^* X^* \le N\pi`$, my reading of condition 3 from its proof), in which case exclusion at a zero
payment is the only one. Proposition 3 shows that with public sequential offers the outcome is unique; the
Section IV example ($`N = 100`$, $`N^* = 90`$, $`\pi = 10`$, $`X^* = 14`$) gives exclusion at zero cost although
paying all 90 in full would cost 1,260 against 1,000 of profit, and exclusion is not profitable if more than 71 customers must be paid in full.

Ilya R. Segal and Michael D. Whinston, "Naked Exclusion: Comment," *American Economic Review* 90(1), March 2000,
pp. 296–309, corrected the characterization of when exclusion is likely and what it costs and analyzed
discriminatory offers. I could not obtain the comment's full text; its results are taken from the summary in Chen
and Zápal (2022), which states that with discriminatory simultaneous offers exclusion occurs if and only if the
profit from all buyers exceeds full compensation to the minimum set of buyers needed, and that the sequential cutoff
is weaker.

## Headline results

| Quantity | Value | Source file |
|---|---|---|
| Paper's abstract example, customers to sign | 86 of 100 | `paper_examples.csv` |
| Paper's Section IV example, sequential payment | 0 | `paper_examples.csv` |
| Industries in sample | 333 ($6.77 trillion shipments) | `summary_2022.csv` |
| Median rival scale, leader plant / midpoint plant | 1.88% / 0.89% | `summary_2022.csv` |
| Industries with rival scale ≥ 15% / ≥ 1/3 | 2 / 0 | `summary_2022.csv` |
| Median share of demand to lock up | 98.1% (99 of 100 customers) | `summary_2022.csv` |
| Industries where full payment pays (linear / CES) | 0 / 0 | `summary_2022.csv` |
| Median customers for sequential exclusion (at zero cost) | 160, IQR 82–390 (213, IQR 109–488) | `summary_2022.csv` |
| Case industries' mean scale percentile | 61.6, one-sided p = 0.218 | `cases_rank_test.csv` |

## Data

| File | Source | Used for |
|---|---|---|
| `data/raw/EC2200SIZECONCEN.zip` | 2022 Economic Census, concentration by largest firms | CR4, plants of the top 4, firms, shipments, HHI (top 50) |
| `data/raw/EC2200SIZEEMPEST.zip` | 2022 Economic Census, establishment employment size | Value added, payroll and shipments for the price-cost margin |
| `data/raw/cbp22us.zip` | 2022 County Business Patterns, US file | Employment and plant counts by size class, midpoint plant |

All three were downloaded from www2.census.gov on November 1, 2026 and are committed unchanged. Case facts are
constants in `src/exclusion_cases.py` with citations to the opinions and agency documents.

## Method

Rules fixed before looking at results:

- Sample: national, all-establishment rows for six-digit NAICS 31–33 industries. Drop industries whose top-4 plant
  count is suppressed and a judgment list of 12 local-market codes (the same list used in `bain-1951-revisited`).
- Rival scale, main measure: one leading plant's share. Robustness: the midpoint plant and the largest-firm
  ceiling.

```math
\begin{aligned}
m_i &= \frac{CR4_i}{P_i}, \qquad m_i^{\text{mid}} = \frac{E_{i,c^*}/n_{i,c^*}}{E_i} \\
m_i^{\max} &= \min\!\left(\sqrt{HHI_i}/100,\ CR4_i/100\right)
\end{aligned}
```

where $`c^*`$ is the CBP employment class containing the median worker, $`E_{i,c}`$ and $`n_{i,c}`$ its
employment and plant count, and $`E_i`$ total employment.

- Profit-to-loss ratio: $`r = 2/3`$ (linear demand). Robustness: constant-elasticity demand with the monopoly
  Lerner index $`L_i`$ set equal to the Census price-cost margin, dropped outside 0.02 to 0.95.

```math
L_i = \frac{VA_i - W_i}{S_i}, \qquad \varepsilon_i = \frac{1}{L_i}, \qquad r_i = \frac{L_i(\varepsilon_i - 1)}{(1 - L_i)^{1 - \varepsilon_i} - 1}
```

- Simultaneous offers with full compensation (RRW condition 3; Segal and Whinston's discriminatory case) pay when
  the share to be signed is at most $`r`$. Sequential offers: solve the game backward. A buyer whose refusal would
  still leave exclusion feasible signs for zero; a crucial buyer needs $`X^*`$. Following the paper's proof of
  Proposition 3 (the benefit from exclusion shrinks as more customers sign, "because those S customers are not free
  to go to the entrant anyway"), the incumbent keeps paying while $`\pi`$ times the customers not yet signed covers
  the payments still to come. With payments in units of $`X^*`$, a rival that can lose $`j`$ customers, $`d`$
  further refusals tolerable and $`T`$ customers left, the first $`T - M_j(d-1) - 1`$ customers are crucial, and the
  binding budget check is at the start, where $`j - d + T`$ customers are unsigned:

```math
\begin{aligned}
r\,(j - d + T) &\ge T - M_j(d-1) - 1 \\
M_j(d) &= \left\lfloor \frac{(j - d)\,r + 1 + M_j(d-1)}{1 - r} \right\rfloor,\quad M_j(-1) = -1 \\
F(j) &= M_j(j), \qquad F_0(j) = M_j(j-1) + 1
\end{aligned}
```

  Exclusion succeeds with $`N`$ customers if $`N \le F(j)`$ and costs nothing if $`N \le F_0(j)`$. The script
  checks both, and the payments on the equilibrium path, against brute-force backward induction for every $`N`$
  from 2 to 60, every rival requirement and two ratios (10/14 and 2/3), with zero mismatches, and reproduces the
  paper's Section IV result.

- Fewest customers: $`N_i^{\min}`$ is one more than the largest market $`N`$ with $`N > F(\lceil m_i N \rceil - 1)`$,
  so exclusion succeeds in every market at least that large (a market just past a step in $`\lceil m_i N \rceil`$
  can fail when a smaller one succeeds). The zero-cost version uses $`F_0`$.
- Cases: four exclusive-dealing matters chosen because each has a published record of buyers and shares. The rank
  test compares their mean percentile of $`m_i`$ with 200,000 random draws of four industries without replacement
  (seed 1991).

## Full results

Rival scale across 333 industries:

| Measure | Median | 90th percentile | ≥ 15% | ≥ 1/3 | Industries |
|---|---|---|---|---|---|
| Leader plant | 1.88% | 6.47% | 2 | 0 | 333 |
| Midpoint plant | 0.89% | 3.33% | 2 | 0 | 317 |
| Largest firm, ceiling | 20.96% | 34.67% | 212 | 32 | 261 |

Lock-up share at or below 40% or 50%: 0 industries. Full payment pays: 0 with $`r = 2/3`$, 0 with CES at the Census
margin (median margin 33.6%, median $`r_i`$ 0.533). Sequential threshold: median 160 customers, quartiles 82 and
390, 29 industries (14.3% of shipments) above 1,000. At zero cost: median 213, quartiles 109 and 488, 29 above 1,000.
With $`r = 2/3`$, $`F(1), \ldots, F(5)`$ = 9, 54, 243, 972 and 3,645, and $`F_0`$ = 3, 18, 81, 324 and 1,215.

```math
\bar{u}_{\text{cases}} = 61.6, \qquad \mathbb{E}[\bar{u}_{\text{random}}] = 50.1, \qquad p = 0.218
```

With equal buyers, the rival must need 2 of 4 buyers one at a time or 3 of 4 with full payment (Eaton's market), and
3 of 23 one at a time or 9 of 23 with full payment (Dentsply's dealers).

## Reproducing the results

```bash
pip install -r requirements.txt
rm -f results/*.csv results/*.png
python src/naked_exclusion.py
python src/exclusion_cases.py
```

Both scripts run in under a minute from the committed data and print rows loaded, kept and dropped.

## Repository layout

| Path | What it is |
|---|---|
| `src/naked_exclusion.py` | Paper's arithmetic, sequential game solver, Census measures, summary, two figures |
| `src/exclusion_cases.py` | Case table, buyers grid, rank test |
| `results/FINDINGS.md` | Plain-English summary and every table |
| `results/*.csv`, `results/*.png` | Every number and figure in the README |

## References

- Chen, Y. & Zápal, J. (2022). Naked exclusion with heterogeneous buyers. CERGE-EI Working Paper 741.
- Fumagalli, C. & Motta, M. (2006). Exclusive dealing and entry, when buyers compete. *American Economic Review*
  96(3), 785–795.
- Landeo, C. & Spier, K. (2009). Naked exclusion: an experimental study of contracts with externalities. *American
  Economic Review* 99(5); NBER Working Paper 14115 (2008).
- Rasmusen, E., Ramseyer, J. M. & Wiley, J. S. (1991). Naked exclusion. *American Economic Review* 81(5), 1137–1145.
- Rasmusen, E., Ramseyer, J. M. & Wiley, J. S. (1999 draft). Naked exclusion: theory and law. Posted at rasmusen.org.
- Segal, I. & Whinston, M. (2000). Naked exclusion: comment. *American Economic Review* 90(1), 296–309.
- *McWane, Inc. v. FTC*, 783 F.3d 814 (11th Cir. 2015). *ZF Meritor, LLC v. Eaton Corp.*, 696 F.3d 254 (3d Cir.
  2012). *United States v. Dentsply Int'l*, 399 F.3d 181 (3d Cir. 2005). *United States v. Microsoft Corp.*, 253
  F.3d 34 (D.C. Cir. 2001).
