# Naked exclusion on 2022 US manufacturing: findings

## In plain English

In 1991 Rasmusen, Ramseyer and Wiley showed that a dominant firm can keep out an equally efficient rival by
signing exclusive contracts with enough customers, and that customers who cannot coordinate may sign for almost
nothing. With 100 customers and a rival that needs 15, the incumbent must sign 86. This repository measures how
much of each American manufacturing market a rival actually needs.

- **A single efficient plant is a sliver of the national market.** In the median industry a leading plant serves
  1.88% of shipments, so an incumbent would have to lock up 99 of every 100 customers. Only computer storage devices
  and telephone apparatus reach the paper's 15%. Even aircraft (Boeing's industry, top four with 83.5%) runs 31
  plants, so one plant is 2.7% of the market.
- **Paying the needed customers in full never pays.** With a monopolist keeping two dollars for every three its
  customers lose, full payment requires a rival that needs a third of the market. No industry qualifies.
- **One customer at a time, a few hundred buyers are enough.** In the paper's sequential game, exclusion is the sure
  outcome in every market of 160 or more separately approached customers in the median industry, and costs nothing
  from 213. Whether buyers can coordinate matters more than factory size.
- **The famous cases had few buyers.** Eaton faced four truck makers (Freightliner, International, PACCAR, Volvo),
  where one-at-a-time offers exclude only a rival that needs two of the four and full payment only one that needs
  three. Dentsply's 23 dealers and McWane's two big
  distributors (HD Supply and Ferguson) were also few. The four case industries are not unusual in plant scale
  (mean percentile 61.6, p = 0.218).

A friendlier tour is in the [README](../README.md). Method and reproduction are in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels.** *Rival scale* or *m* = one leading plant's share of national shipments, CR4 divided by the
plants the top four run. *Midpoint plant* = average plant in the County Business Patterns employment class holding
the median worker, as a share of employment. *Largest firm ceiling* = min(sqrt(HHI)/100, CR4/100), an upper bound.
*r* = monopoly profit per customer divided by each customer's loss of surplus (2/3 with linear demand). *Lock-up
share* = 1 − m. *Signers of 100* = customers out of 100 equal ones the incumbent must sign. *Min customers
sequential* = market size (equal customers) from which one-at-a-time offers exclude in every larger market;
*_free* = the same, with nobody paid. *pcm* = Census price-cost
margin, (value added − payroll) / shipments. Percent columns are in percent; shipments in millions of dollars.

## All tables

### paper_examples.csv

| quantity | computed | paper |
|---|---|---|
| Abstract: customers the incumbent must sign (N=100, MES=15) | 86 | 86 |
| Sec. IV: monopoly profit from all customers (N*pi) | 1,000 | 1,000 |
| Sec. IV: cost of paying N* customers in full (N* X*) | 1,260 | 1,260 |
| Sec. IV: most customers worth paying in full (floor(N pi / X*)) | 71 | 71 |
| Sec. IV: cost of paying 71 customers | 994 | 994 |
| Sec. IV: sequential offers exclude? (1 = yes) | 1 | yes |
| Sec. IV: total paid under sequential offers | 0 | 0 |
| Simultaneous offers exclude for sure? (N* X* <= N pi, 1 = yes) | 0 | no (two equilibria) |
| Profit-to-loss ratio in the example (pi / X*) | 0.714286 | 10/14 |
| Profit-to-loss ratio, linear demand | 0.666667 | derived |

### profit_to_loss.csv

| monopoly_markup | profit_to_loss_ces | profit_to_loss_linear |
|---|---|---|
| 0.1 | 0.5692 | 0.6667 |
| 0.2 | 0.555 | 0.6667 |
| 0.3 | 0.5391 | 0.6667 |
| 0.4 | 0.521 | 0.6667 |
| 0.5 | 0.5 | 0.6667 |
| 0.6 | 0.4751 | 0.6667 |

### sequential_frontier.csv (reshaped)

| rival needs (customers) | max customers, r = 0.5 | at zero cost, r = 0.5 | max customers, r = 0.6667 | at zero cost, r = 0.6667 | max customers, r = 0.7143 | at zero cost, r = 0.7143 |
|---|---|---|---|---|---|---|
| 2 | 4 | 2 | 9 | 3 | 10 | 3 |
| 3 | 16 | 8 | 54 | 18 | 84 | 24 |
| 4 | 48 | 24 | 243 | 81 | 427 | 122 |
| 5 | 128 | 64 | 972 | 324 | 2,093 | 598 |
| 6 | 320 | 160 | 3,645 | 1,215 | 8,830 | 2,523 |
| 7 | 768 | 384 | 13,122 | 4,374 | 38,244 | 10,927 |
| 8 | 1,792 | 896 | 45,927 | 15,309 | 154,385 | 44,110 |
| 9 | 4,096 | 2,048 | 157,464 | 52,488 | 630,262 | 180,075 |
| 10 | 9,216 | 4,608 | 531,441 | 177,147 | 2,431,733 | 694,781 |
| 11 | 20,480 | 10,240 | 1,771,470 | 590,490 | 9,611,924 | 2,746,264 |
| 12 | 45,056 | 22,528 | 5,845,851 | 1,948,617 | 36,634,458 | 10,466,988 |
| 13 | 98,304 | 49,152 | 19,131,876 | 6,377,292 | 141,777,972 | 40,507,992 |

### summary_2022.csv

| statistic | value | unit |
|---|---|---|
| industries in sample | 333 |  |
| shipments in sample | 6.772 | trillion USD |
| median rival scale, leader plant | 1.88 | % of national shipments |
| 90th percentile rival scale, leader plant | 6.47 | % of national shipments |
| industries with rival scale >= 15% (paper's example), leader plant | 2 |  |
| industries with rival scale >= 1/3 (pays with full compensation), leader plant | 0 |  |
| industries measured, leader plant | 333 |  |
| median rival scale, midpoint plant | 0.89 | % of national shipments |
| 90th percentile rival scale, midpoint plant | 3.33 | % of national shipments |
| industries with rival scale >= 15% (paper's example), midpoint plant | 2 |  |
| industries with rival scale >= 1/3 (pays with full compensation), midpoint plant | 0 |  |
| industries measured, midpoint plant | 317 |  |
| median rival scale, largest firm, upper bound | 20.96 | % of national shipments |
| 90th percentile rival scale, largest firm, upper bound | 34.67 | % of national shipments |
| industries with rival scale >= 15% (paper's example), largest firm, upper bound | 212 |  |
| industries with rival scale >= 1/3 (pays with full compensation), largest firm, upper bound | 32 |  |
| industries measured, largest firm, upper bound | 261 |  |
| median share of demand to lock up (leader plant) | 98.1 | % |
| median customers to sign, of 100 (leader plant) | 99 |  |
| industries where lock-up share <= 40% | 0 |  |
| industries where lock-up share <= 50% | 0 |  |
| industries where exclusion pays with full compensation, linear demand | 0 |  |
| industries where exclusion pays with full compensation, CES demand at Census margin | 0 |  |
| median Census price-cost margin | 33.6 | % |
| median profit-to-loss ratio, CES at Census margin | 0.533 |  |
| median customers needed for one-at-a-time offers to exclude | 160 |  |
| 25th percentile customers needed | 82 |  |
| 75th percentile customers needed | 390 |  |
| industries needing more than 1,000 customers | 29 |  |
| shipments share needing more than 1,000 customers | 14.3 | % |
| median customers needed for one-at-a-time offers to exclude at zero cost | 213 |  |
| 25th percentile customers needed, zero cost | 109 |  |
| 75th percentile customers needed, zero cost | 488 |  |
| industries needing more than 1,000 customers, zero cost | 29 |  |

### industries_2022.csv, 20 largest rival scales

Percent columns (m_leader_plant, m_midpoint, m_largest_firm_max, pcm) are shown in percent.

| naics | label | shipments_musd | cr4 | top4_plants | m_leader_plant | m_midpoint | m_largest_firm_max | pcm | signers_of_100 | min_customers_sequential | min_customers_sequential_free |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 334112 | Computer storage device manufacturing | 4,721 | 83.6 | 5 | 16.72 | 4.04 |  | 21.11 | 84 | 12 | 12 |
| 334210 | Telephone apparatus manufacturing | 4,298 | 61.9 | 4 | 15.48 | 2.37 |  | 32 | 85 | 13 | 20 |
| 331313 | Alumina refining and primary aluminum production | 2,931 | 91.3 | 7 | 13.04 | 18.12 |  | 20.85 | 87 | 16 | 24 |
| 332215 | Metal kitchen cookware, utensil, cutlery, and flatware (except precious) manufacturing | 3,202 | 65.6 | 6 | 10.93 | 3.02 |  | 54.4 | 90 | 19 | 28 |
| 334111 | Electronic computer manufacturing | 11,778 | 60.5 | 6 | 10.08 | 2.02 |  | 22.03 | 90 | 20 | 30 |
| 332993 | Ammunition (except small arms) manufacturing | 4,174 | 87.1 | 9 | 9.68 | 6.12 |  | 50.69 | 91 | 21 | 31 |
| 325194 | Cyclic crude, intermediate, and gum and wood chemical manufacturing | 5,491 | 57.1 | 6 | 9.52 | 3.09 | 35.98 | 39.97 | 91 | 22 | 32 |
| 331410 | Nonferrous metal (except aluminum) smelting and refining | 12,286 | 56.3 | 6 | 9.38 | 2.43 | 29.7 | 20.53 | 91 | 22 | 32 |
| 336991 | Motorcycle, bicycle, and parts manufacturing | 3,800 | 65.3 | 7 | 9.33 | 1.13 |  | 45.48 | 91 | 22 | 33 |
| 335921 | Fiber optic cable manufacturing | 3,763 | 64.6 | 7 | 9.23 | 2.67 | 36.94 | 32.42 | 91 | 22 | 33 |
| 335131 | Residential electric lighting fixture manufacturing | 2,884 | 63.8 | 7 | 9.11 |  |  | 43.4 | 91 | 22 | 33 |
| 334610 | Manufacturing and reproducing magnetic and optical media | 1,614 | 54.6 | 6 | 9.1 |  |  | 33.01 | 91 | 22 | 33 |
| 339930 | Doll, toy, and game manufacturing | 1,747 | 45.5 | 5 | 9.1 | 0.51 |  | 37.36 | 91 | 22 | 33 |
| 311422 | Specialty canning | 9,844 | 68.7 | 8 | 8.59 | 4.4 |  | 51.79 | 92 | 24 | 35 |
| 332992 | Small arms ammunition manufacturing | 5,826 | 75.4 | 9 | 8.38 | 10.37 | 42.02 | 40.12 | 92 | 24 | 36 |
| 335210 | Small electrical appliance manufacturing | 3,651 | 58.6 | 7 | 8.37 | 1.92 | 33.07 | 39.96 | 92 | 24 | 36 |
| 339994 | Broom, brush, and mop manufacturing | 2,760 | 41.8 | 5 | 8.36 | 1.69 | 24.47 | 39.53 | 92 | 24 | 36 |
| 339993 | Fastener, button, needle, and pin manufacturing | 871 | 66.2 | 8 | 8.28 | 3.39 |  | 28.86 | 92 | 25 | 37 |
| 336419 | Other guided missile and space vehicle parts and auxiliary equipment manufacturing | 2,367 | 69 | 9 | 7.67 | 3.35 | 37.13 | 29.77 | 93 | 27 | 40 |
| 316110 | Leather and hide tanning and finishing | 1,148 | 60.1 | 8 | 7.51 | 2.46 | 33.99 | 24.18 | 93 | 27 | 40 |

### cases.csv

| case | decided_or_filed | seller_naics | seller_cr4 | rival_scale_leader_plant_pct | rival_scale_percentile | lock_up_share_pct | min_customers_sequential | buyers_in_record | rival_must_need_simultaneous | rival_must_need_sequential |
|---|---|---|---|---|---|---|---|---|---|---|
| Dentsply (artificial teeth) | 2,005 | 339114 | 45.1 | 3.01 | 68.2 | 97 | 100 | 23 | 9 | 3 |
| McWane (domestic pipe fittings) | 2,015 | 331511 | 41.4 | 1.97 | 51.1 | 98 | 153 |  |  |  |
| Eaton (heavy truck transmissions) | 2,012 | 336350 | 39.5 | 1.41 | 39.9 | 98.6 | 284 | 4 | 3 | 2 |
| Syngenta and Corteva (crop protection) | 2,022 | 325320 | 59.6 | 5.42 | 87.4 | 94.6 | 56 |  |  |  |

| case | incumbent_share | rival_shares | lock_up | payment_to_buyers |
|---|---|---|---|---|
| Dentsply (artificial teeth) | 75-80% of revenue | Ivoclar 5%, Vita 3% | dealers barred from adding rival tooth lines (Dealer Criterion 6, 1993) | none; threat of losing the Dentsply line |
| McWane (domestic pipe fittings) | 100% of domestic-only fittings, 2006-09; about 90% in 2011 | Star about 5% (2010), just under 10% (2011) | rebates withheld from distributors buying rival domestic fittings | rebates conditioned on buying only from McWane |
| Eaton (heavy truck transmissions) | above 80%, 2000-07 | Meritor 17% (1999), 4% (2005), exit 2007 | rebates for buying 70-78% (Volvo) up to 87-97.5% (International) from Eaton | rebates; up-front payments of $2.5M (International) and $1M (PACCAR) |
| Syngenta and Corteva (crop protection) | not stated in release | generic makers of six active ingredients | distributor payments only if purchases of generics stay below a low threshold | loyalty payments (alleged; case filed with 10 states) |

| case | buyer_naics | buyer_label | buyer_firms | buyer_cr4 | buyer_cr8 |
|---|---|---|---|---|---|
| Dentsply (artificial teeth) | 423450 | Medical, dental, and hospital equipment and supplies merchant wholesalers | 7,394 | 23.9 | 40.6 |
| McWane (domestic pipe fittings) |  |  |  |  |  |
| Eaton (heavy truck transmissions) | 336120 | Heavy duty truck manufacturing | 84 | 76 | 86.2 |
| Syngenta and Corteva (crop protection) | 424910 | Farm supplies merchant wholesalers | 4,928 | 22.8 | 35.3 |

### buyers_grid.csv

| buyers | rival_must_need_simultaneous | simultaneous_share_pct | rival_must_need_sequential | sequential_share_pct | no_natural_monopoly_ok |
|---|---|---|---|---|---|
| 2 | 2 | 100 | 2 | 100 | False |
| 3 | 2 | 66.7 | 2 | 66.67 | False |
| 4 | 3 | 75 | 2 | 50 | True |
| 6 | 3 | 50 | 2 | 33.33 | True |
| 8 | 4 | 50 | 2 | 25 | True |
| 10 | 5 | 50 | 3 | 30 | True |
| 15 | 6 | 40 | 3 | 20 | True |
| 23 | 9 | 39.1 | 3 | 13.04 | True |
| 50 | 18 | 36 | 3 | 6 | True |
| 100 | 35 | 35 | 4 | 4 | True |
| 1,000 | 335 | 33.5 | 6 | 0.6 | True |
| 4,928 | 1,644 | 33.4 | 7 | 0.14 | True |

### cases_rank_test.csv

| cases | mean_percentile | mean_percentile_if_random | p_value_one_sided | draws | eaton_open_share_2003_pct | eaton_industry_lock_up_needed_pct |
|---|---|---|---|---|---|---|
| 4 | 61.6 | 50.1 | 0.218 | 200,000 | 15 | 98.6 |

The full list of 333 industries is in [industries_2022.csv](industries_2022.csv). Figures:
[rival_scale_2022.png](rival_scale_2022.png) and [customers_needed_sequential.png](customers_needed_sequential.png).
