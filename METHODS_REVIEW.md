# Methods review: Rasmusen, Ramseyer and Wiley (1991)

- **Paper:** Eric B. Rasmusen, J. Mark Ramseyer and John S. Wiley Jr., "Naked Exclusion," *American Economic
  Review* 81(5), December 1991, pp. 1137–1145.
- **Statistical focus:** the abstract's numerical claim (100 customers, minimum efficient scale of 15, lock up 86)
  and the Section IV numerical example (N = 100, N* = 90, per-customer profit 10, per-customer loss 14) that
  illustrates Proposition 3.
- **Review standard:** internal consistency of the formal results, explicit statement of assumptions, and the
  testability of the predictions, since the paper is a theory paper with no data.
- **What was read:** the full article text as reproduced on Eric Rasmusen's website
  (rasmusen.org/published/Rasmusen_91.AER.exclusion.htm), in which the multi-line equations are not rendered
  ("Multiple line equation cannot be represented by ASCII text"), so the exact statements of equations (1) to (8)
  were not visible; the authors' 1999 draft "Naked Exclusion: Theory and Law" on the same site; secondary
  statements of Segal and Whinston (2000) in Chen and Zápal (CERGE-EI Working Paper 741, 2022) and in the abstract of
  Landeo and Spier (NBER Working Paper 14115, 2008). The Segal and Whinston comment itself was not read.

## Methods summary

The paper builds a two-period model with N identical customers, an incumbent and one potential entrant with the
same cost function. Average cost falls until output reaches a minimum efficient scale Q* and is constant after, the
entrant must serve more than one customer to reach Q*, and the market is large enough for two firms (no natural
monopoly). In period 1 the incumbent sells at a price and offers a payment X to any customer who signs an agreement
not to buy from the rival; customers decide; the rival decides whether to enter; prices are set; customers buy.

The results are three propositions and a lemma. Proposition 1 formalizes the Director and Levi (Chicago) argument
that with no minimum efficient scale nobody signs, because each customer's loss X* exceeds the incumbent's
per-customer monopoly profit. Lemma 1 defines N*, the number of signers that deters entry. Proposition 2 shows that
with simultaneous decisions there are two kinds of pure-strategy equilibria, all sign (no entry) and none signs
(entry), and that exclusion at a zero payment is the only equilibrium when condition (3) holds. Proposition 3 shows
that when customers decide publicly in sequence, the equilibrium is unique and is exclusion or entry depending on
condition (4). Section V discusses how to choose among equilibria (offer timing, focal points, communication).

### Research design

A formal game-theoretic model solved for subgame-perfect Nash equilibria, with a short legal motivation drawn from
court records (Alcoa, Lorain Journal, United Shoe Machinery). There is no empirical design.

### Sampling strategy

Does not apply. No observations are sampled. The three court cases in the introduction are cited as examples, not
as a sample, and no selection rule is given for them.

### Sample size

Does not apply. The numerical examples use N = 100 customers, a modeling choice.

### Inclusion and exclusion criteria

Does not apply to data. The model's scope conditions play this role and are stated explicitly: identical customers
with the same individual demand, identical cost functions for incumbent and rival, a minimum efficient scale
requiring more than one customer, no natural monopoly, no discounting, price-taking customers who split evenly
between equal-priced sellers, and (for Section IV) take-it-or-leave-it offers.

### Independent and dependent variables

In model terms, the inputs are N, the minimum efficient scale Q* (through N*), per-customer monopoly profit and
per-customer loss X*, and the order of moves; the outcomes are whether customers sign, the payment X, and whether
entry occurs.

### Statistical methods

Does not apply. The "methods" are equilibrium characterization by construction and backward induction.

### Reported effect sizes

No effect sizes in the statistical sense. The closest analogues are the abstract's 86 of 100 customers and the
Section IV payments (1,260 for full payment against 1,000 of profit; 0 in the sequential equilibrium).

### Confidence intervals

Does not apply. All quantities are exact model outputs; no uncertainty is reported or needed.

### P-values, if applicable

Not applicable.

### Missing data treatment

Not applicable. No data are used.

### Stated limitations

The authors state that exclusion cannot be claimed always to work, that it is unlikely if customers can communicate
easily, that it fails with perfectly elastic demand or no minimum efficient scale, and (footnote 4) that the
sequential result depends on the incumbent holding all bargaining power. They do not discuss buyers who compete with
one another downstream, buyers of unequal size, or how to measure the model's parameters.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Customers to lock up in the abstract example | 86 of 100 customers, with minimum efficient scale of 15 customers | Abstract, p. 1137 | Signers needed so the 14 free customers fall short of the rival's scale | That locking up 86 is cheap in every equilibrium, or that real markets have a scale of 15% |
| Customers in the Section IV example | N = 100 | Section IV, numerical example | Market size for the illustration | Any empirical market size |
| Signers needed in the example | N* = 90 | Section IV | Entry deterred if at least 90 sign | How N* relates to Q* in the example (not stated) |
| Per-customer monopoly profit | 10 (no units) | Section IV | Incumbent's profit per customer per period | A calibrated demand system |
| Per-customer loss from monopoly | X* = 14 | Section IV | Surplus each customer loses at the monopoly price | The implied demand shape (ratio 10/14 = 0.714 is above the 2/3 of linear demand) |
| Cost of paying all needed customers in full | 1,260 | Section IV | N* X* | That this is the cost actually incurred |
| Monopoly profit from all customers | 1,000 | Section IV | N times per-customer profit | Discounting or multi-period profits beyond the model |
| Most customers worth paying in full | 71, at a cost of 994 | Section IV | Floor of 1,000 / 14 | The equilibrium payment |
| Payments in the sequential equilibrium | 70 customers at 14 (980) as an illustration, then 0; ultimately 0 to all | Section IV | Divide-and-conquer logic under public sequential offers | Robustness to bargaining power held by buyers (footnote 4 flags this) |
| Equilibrium count, simultaneous game | Two pure-strategy equilibria (plus mixed) | Proposition 2 | Multiplicity of outcomes | Which equilibrium real buyers play |

## Interpretation notes

- The numerical example's profit-to-loss ratio of 10/14 is more favorable to exclusion than linear demand, where a
  monopolist's profit is two-thirds of the customer's loss. The paper does not state a demand function for the
  example, so the ratio is an assumption, not a derived quantity.
- The abstract's claim ("an individual customer loses nothing by signing") holds in the all-sign equilibrium of the
  simultaneous game. Proposition 2 itself shows a none-signs equilibrium also exists unless condition (3) holds, so
  the abstract describes one equilibrium, not a unique prediction. This is a matter of emphasis in the abstract, not
  an error in the proposition.
- The sequential result depends on take-it-or-leave-it offers by the incumbent and public, permanent decisions; the
  paper says so in footnote 4.
- Segal and Whinston (2000) published a comment that, by its own description, corrects the paper's
  characterization of when exclusion is likely and what it costs, and analyzes discriminatory offers. That is a
  documented correction of characterization in the published literature. I did not read the comment and do not
  describe its specific claims beyond the secondary summaries named above.
- The proof of Proposition 3 states that the benefit from exclusion falls as more customers sign, "because those S
  customers are not free to go to the entrant anyway", and the numerical example counts further profits of "10 each
  from the 30 remaining consumers" after 70 have signed. The incumbent's budget at any point is therefore the profit
  from customers not yet signed, including those who refused, not only from customers still to be asked.
- A backward-induction solution of the sequential game written for this repository, using that budget, reproduces
  the Section IV outcome (exclusion at zero total payment), which supports the internal consistency of that example. This is a
  check of the arithmetic, not a reproduction of any data result.

## Unanswered questions

- The exact statements of Lemma 1 and conditions (3), (4) and (6) to (8) could not be read in the available text,
  so whether the Section IV example satisfies condition (4) with the stated numbers could be confirmed only by
  solving the game independently.
- How N* = 90 in the example maps to a minimum efficient scale Q* and individual demand is not stated.
- The paper offers no guidance on measuring the minimum efficient scale, the number of independent buyers, or the
  profit-to-loss ratio in real markets, which are the quantities its predictions turn on.
- The selection discussion in Section V (offer timing, focal points, forward induction) is informal; no
  equilibrium-selection criterion is applied formally.

## Items requiring expert verification

- The full typeset statements of equations (1) to (8), from the published AER version, to confirm the conditions
  used here (N* X* no greater than N times profit for uniqueness in the simultaneous game).
- Whether the recursion used in this repository for the sequential frontier, M(d) = floor(((j − d) r + 1 + M(d − 1))/(1 − r))
  with F(j) = M(j), matches the paper's typeset conditions (4) to (8) and Segal and Whinston's sequential cutoff for
  equal buyers. It was derived from the proof's verbal argument and checked only against brute-force backward
  induction of the same game.
- Whether the paper's condition (4), which the proof derives for a game with one refusal to spare (S = 0,
  T = N* + 1) and extends "a fortiori", is also meant as a necessary condition when the rival can lose several
  customers. The typeset condition could not be read, so this repository does not compare it with the brute-force
  solution.
- Whether the plant-share measure of minimum efficient scale used in the modern rerun is an acceptable stand-in for
  the paper's Q*, given that the paper's Q* is a property of the cost function, not of observed plants.
- The modern rerun in this repository does not reproduce the paper, which has no data. It takes the paper's
  conditions to 2022 Census data and asks where they could hold, and its results should be read as a measurement
  of the theory's preconditions, not as a test of whether exclusion occurs.
