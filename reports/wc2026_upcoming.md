# World Cup 2026 — Opening Matches (Jun 26–Jun 27)

Model-based forecasts for the next round of group matches (12 fixtures), generated from **current Elo** (all played matches through 2026-06-25). The Dixon-Coles Poisson model is the one validated on the 2018 & 2022 backtests; its coefficients are frozen at the 2022-11-19 fit, only the ratings are current.

De-vigged bookmaker odds are shown for comparison only — they do **not** feed the model. `Edge` = largest gap between our probability and the market on any outcome.

## Results so far

How the pre-match forecasts have fared, model vs de-vigged market (this is the B2 baseline, scored live going forward):

| Match | Result | Our call (H/D/A) | Market (H/D/A) | Winner |
|---|---|---|---|---|
| Mexico v South Africa | 2-0 (home) | 80/14/6 | 69/21/10 | model |
| South Korea v Czech Republic | 2-1 (home) | 42/31/27 | 37/30/33 | model |
| Canada v Bosnia and Herzegovina | 1-1 (draw) | 72/18/9 | 53/26/21 | market |
| United States v Paraguay | 4-1 (home) | 33/29/38 | 49/28/23 | market |
| Qatar v Switzerland | 1-1 (draw) | 7/17/76 | 6/14/80 | model |
| Brazil v Morocco | 1-1 (draw) | 44/30/26 | 58/24/18 | model |
| Haiti v Scotland | 0-1 (away) | 22/29/49 | 15/23/62 | market |
| Australia v Turkey | 2-0 (home) | 27/31/42 | 18/26/56 | model |
| Germany v Curaçao | 7-1 (home) | 76/17/7 | 94/5/2 | market |
| Ivory Coast v Ecuador | 1-0 (home) | 16/26/59 | 27/34/39 | market |
| Netherlands v Japan | 2-2 (draw) | 36/31/33 | 47/27/26 | model |
| Sweden v Tunisia | 5-1 (home) | 39/31/30 | 50/28/22 | market |
| Belgium v Egypt | 1-1 (draw) | 50/29/22 | 58/25/17 | model |
| Iran v New Zealand | 2-2 (draw) | 52/28/20 | 51/28/21 | market |
| Spain v Cape Verde | 0-0 (draw) | 90/8/2 | 89/8/3 | market |
| Saudi Arabia v Uruguay | 1-1 (draw) | 11/22/66 | 11/22/67 | model |
| France v Senegal | 3-1 (home) | 58/26/16 | 66/22/12 | market |
| Iraq v Norway | 1-4 (away) | 14/25/60 | 6/14/80 | market |
| Argentina v Algeria | 3-0 (home) | 70/21/10 | 70/20/10 | model |
| Austria v Jordan | 3-1 (home) | 46/30/24 | 73/17/10 | market |
| Portugal v DR Congo | 1-1 (draw) | 66/22/11 | 76/16/8 | model |
| Uzbekistan v Colombia | 1-3 (away) | 14/25/62 | 10/20/70 | market |
| England v Croatia | 4-2 (home) | 47/30/23 | 56/25/19 | market |
| Ghana v Panama | 1-0 (home) | 14/25/61 | 46/28/26 | market |
| Czech Republic v South Africa | 1-1 (draw) | 50/28/22 | 52/27/21 | model |
| Mexico v South Korea | 1-0 (home) | 56/24/20 | 46/29/24 | model |
| Switzerland v Bosnia and Herzegovina | 4-1 (home) | 64/22/13 | 62/23/15 | model |
| Canada v Qatar | 6-0 (home) | 79/14/7 | 74/17/9 | model |
| Scotland v Morocco | 0-1 (away) | 23/28/49 | 17/26/57 | market |
| Brazil v Haiti | 3-0 (home) | 76/17/7 | 87/9/4 | market |
| United States v Australia | 2-0 (home) | 35/28/37 | 60/22/18 | market |
| Turkey v Paraguay | 0-1 (away) | 41/29/30 | 46/28/25 | model |
| Germany v Ivory Coast | 2-1 (home) | 53/27/20 | 63/21/16 | market |
| Ecuador v Curaçao | 0-0 (draw) | 78/16/6 | 86/10/4 | model |
| Netherlands v Sweden | 5-1 (home) | 56/26/18 | 56/24/20 | model |
| Tunisia v Japan | 0-4 (away) | 10/19/71 | 15/24/61 | model |
| Belgium v Iran | 0-0 (draw) | 41/29/30 | 67/20/12 | model |
| New Zealand v Egypt | 1-3 (away) | 28/29/43 | 16/24/60 | market |
| Spain v Saudi Arabia | 4-0 (home) | 87/10/3 | 87/9/4 | market |
| Uruguay v Cape Verde | 2-2 (draw) | 67/21/12 | 66/23/11 | market |
| France v Iraq | 3-0 (home) | 83/13/5 | 89/8/3 | market |
| Norway v Senegal | 3-2 (home) | 48/28/24 | 44/28/29 | model |
| Argentina v Austria | 2-0 (home) | 69/20/11 | 66/22/13 | model |
| Jordan v Algeria | 1-2 (away) | 23/28/49 | 15/22/63 | market |
| Portugal v Uzbekistan | 5-0 (home) | 63/23/14 | 84/11/5 | market |
| Colombia v DR Congo | 1-0 (home) | 70/20/10 | 62/24/14 | model |
| England v Ghana | 0-0 (draw) | 84/12/4 | 81/13/6 | market |
| Panama v Croatia | 0-1 (away) | 22/28/50 | 14/22/64 | market |
| Mexico v Czech Republic | 3-0 (home) | 73/17/10 | nan/nan/nan | tie |
| South Africa v South Korea | 1-0 (home) | 15/24/62 | 17/25/58 | market |
| Canada v Switzerland | 1-2 (away) | 38/28/35 | nan/nan/nan | tie |
| Bosnia and Herzegovina v Qatar | 3-1 (home) | 44/29/27 | 69/18/13 | market |
| Scotland v Brazil | 0-3 (away) | 15/24/61 | 10/17/73 | market |
| Morocco v Haiti | 4-2 (home) | 72/19/9 | 82/13/6 | market |
| United States v Turkey | 2-3 (away) | 49/26/25 | nan/nan/nan | tie |
| Paraguay v Australia | 0-0 (draw) | 34/30/36 | 35/42/23 | market |
| Curaçao v Ivory Coast | 0-2 (away) | 16/24/60 | 6/12/82 | market |
| Ecuador v Germany | 2-1 (home) | 28/29/43 | 18/20/62 | model |
| Japan v Sweden | 1-1 (draw) | 60/24/16 | 51/27/22 | market |
| Tunisia v Netherlands | 1-3 (away) | 7/16/77 | 3/9/88 | market |

**Running RPS over 60 match(es): model 0.1792 vs market nan — level.** (Tiny sample — a smoke signal, not a verdict.)

![overview](figures/wc2026/overview.png)

## All fixtures

| Date | Match | Venue | xG (H–A) | Our H/D/A | Market H/D/A | Edge | Top score |
|---|---|---|---|---|---|---|---|
| Jun 26 | Egypt v Iran | neutral | 1.08–1.23 | 32/29/39 | 39/36/25 | 14pp | 1-1 |
| Jun 26 | New Zealand v Belgium | neutral | 0.76–1.76 | 15/24/61 | 7/12/81 | 20pp | 0-1 |
| Jun 26 | Cape Verde v Saudi Arabia | neutral | 1.13–1.17 | 34/30/36 | 36/29/35 | 2pp | 1-1 |
| Jun 26 | Uruguay v Spain | neutral | 0.69–1.93 | 12/22/66 | 15/26/59 | 7pp | 0-1 |
| Jun 26 | Norway v France | neutral | 0.89–1.49 | 22/27/50 | 21/21/58 | 8pp | 0-1 |
| Jun 26 | Senegal v Iraq | neutral | 1.57–0.85 | 54/26/20 | 78/14/8 | 24pp | 1-0 |
| Jun 27 | Algeria v Austria | neutral | 1.12–1.19 | 34/30/37 | 23/45/32 | 16pp | 1-1 |
| Jun 27 | Jordan v Argentina | neutral | 0.45–2.99 | 3/10/87 | 5/11/83 | 4pp | 0-2 |
| Jun 27 | Colombia v Portugal | neutral | 1.22–1.09 | 38/29/32 | 27/25/48 | 16pp | 1-1 |
| Jun 27 | DR Congo v Uzbekistan | neutral | 1.14–1.17 | 35/30/36 | 59/23/17 | 25pp | 1-1 |
| Jun 27 | Panama v England | neutral | 0.64–2.07 | 10/20/70 | 6/11/83 | 12pp | 0-2 |
| Jun 27 | Croatia v Ghana | neutral | 1.92–0.69 | 66/22/12 | 51/30/19 | 16pp | 1-0 |

## Where we disagree with the market

The model is independent of the odds, so these gaps are where our Elo-Poisson view parts from the bookmaker — and they cluster on the model's known soft spots (host-advantage calibration; less boldness on big favourites).

| Match | Our H/D/A | Market H/D/A | Edge | Lean |
|---|---|---|---|---|
| DR Congo v Uzbekistan | 35/30/36 | 59/23/17 | 25pp | model lower on DR Congo |
| Senegal v Iraq | 54/26/20 | 78/14/8 | 24pp | model lower on Senegal |
| New Zealand v Belgium | 15/24/61 | 7/12/81 | 20pp | model higher on New Zealand |
| Croatia v Ghana | 66/22/12 | 51/30/19 | 16pp | model higher on Croatia |
| Colombia v Portugal | 38/29/32 | 27/25/48 | 16pp | model higher on Colombia |
| Algeria v Austria | 34/30/37 | 23/45/32 | 16pp | model higher on Algeria |
| Egypt v Iran | 32/29/39 | 39/36/25 | 14pp | model lower on Egypt |
| Panama v England | 10/20/70 | 6/11/83 | 12pp | model higher on Panama |

## Match-by-match

### Friday, June 26

**Cape Verde vs Saudi Arabia** — _neutral venue_  
Elo Cape Verde 1701 · Saudi Arabia 1710  |  expected goals **1.13 – 1.17**  
- **1X2:** Cape Verde 34% · Draw 30% · Saudi Arabia 36%   _(market 36/29/35)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 11% · 1-0 11% · 0-0 11% · 1-2 8%
- Saudi Arabia favoured (36%); in line with the market.

**Egypt vs Iran** — _neutral venue_  
Elo Egypt 1857 · Iran 1889  |  expected goals **1.08 – 1.23**  
- **1X2:** Egypt 32% · Draw 29% · Iran 39%   _(market 39/36/25)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 12% · 0-0 11% · 1-0 10% · 1-2 8%
- Iran favoured (39%); **model lower than the market on Egypt** (Δ14pp).

**New Zealand vs Belgium** — _neutral venue_  
Elo New Zealand 1713 · Belgium 1932  |  expected goals **0.76 – 1.76**  
- **1X2:** New Zealand 15% · Draw 24% · Belgium 61%   _(market 7/12/81)_
- **Goals:** Over 2.5 46% · BTTS 44%
- **Likeliest scores:** 0-1 14% · 0-2 12% · 1-1 11% · 1-2 9% · 0-0 9%
- Belgium favoured (61%); **model higher than the market on New Zealand** (Δ20pp).

**Norway vs France** — _neutral venue_  
Elo Norway 2028 · France 2160  |  expected goals **0.89 – 1.49**  
- **1X2:** Norway 22% · Draw 27% · France 50%   _(market 21/21/58)_
- **Goals:** Over 2.5 43% · BTTS 46%
- **Likeliest scores:** 0-1 13% · 1-1 13% · 0-2 10% · 0-0 10% · 1-2 9%
- France favoured (50%); in line with the market.

**Senegal vs Iraq** — _neutral venue_  
Elo Senegal 1873 · Iraq 1712  |  expected goals **1.57 – 0.85**  
- **1X2:** Senegal 54% · Draw 26% · Iraq 20%   _(market 78/14/8)_
- **Goals:** Over 2.5 44% · BTTS 46%
- **Likeliest scores:** 1-0 13% · 1-1 12% · 2-0 11% · 0-0 9% · 2-1 9%
- Senegal favoured (54%); **model lower than the market on Senegal** (Δ24pp).

**Uruguay vs Spain** — _neutral venue_  
Elo Uruguay 1939 · Spain 2207  |  expected goals **0.69 – 1.93**  
- **1X2:** Uruguay 12% · Draw 22% · Spain 66%   _(market 15/26/59)_
- **Goals:** Over 2.5 49% · BTTS 43%
- **Likeliest scores:** 0-1 14% · 0-2 14% · 1-1 10% · 1-2 9% · 0-3 9%
- Spain favoured (66%); in line with the market.

### Saturday, June 27

**Algeria vs Austria** — _neutral venue_  
Elo Algeria 1889 · Austria 1905  |  expected goals **1.12 – 1.19**  
- **1X2:** Algeria 34% · Draw 30% · Austria 37%   _(market 23/45/32)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 11% · 0-0 11% · 1-0 10% · 1-2 8%
- Austria favoured (37%); **model higher than the market on Algeria** (Δ16pp).

**Colombia vs Portugal** — _neutral venue_  
Elo Colombia 2094 · Portugal 2066  |  expected goals **1.22 – 1.09**  
- **1X2:** Colombia 38% · Draw 29% · Portugal 32%   _(market 27/25/48)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 11% · 0-0 11% · 0-1 10% · 2-1 8%
- Colombia favoured (38%); **model higher than the market on Colombia** (Δ16pp).

**Croatia vs Ghana** — _neutral venue_  
Elo Croatia 1966 · Ghana 1699  |  expected goals **1.92 – 0.69**  
- **1X2:** Croatia 66% · Draw 22% · Ghana 12%   _(market 51/30/19)_
- **Goals:** Over 2.5 49% · BTTS 43%
- **Likeliest scores:** 1-0 14% · 2-0 14% · 1-1 10% · 2-1 9% · 3-0 9%
- Croatia favoured (66%); **model higher than the market on Croatia** (Δ16pp).

**DR Congo vs Uzbekistan** — _neutral venue_  
Elo DR Congo 1775 · Uzbekistan 1780  |  expected goals **1.14 – 1.17**  
- **1X2:** DR Congo 35% · Draw 30% · Uzbekistan 36%   _(market 59/23/17)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 11% · 1-0 11% · 0-0 11% · 1-2 8%
- Uzbekistan favoured (36%); **model lower than the market on DR Congo** (Δ25pp).

**Jordan vs Argentina** — _neutral venue_  
Elo Jordan 1727 · Argentina 2223  |  expected goals **0.45 – 2.99**  
- **1X2:** Jordan 3% · Draw 10% · Argentina 87%   _(market 5/11/83)_
- **Goals:** Over 2.5 67% · BTTS 34%
- **Likeliest scores:** 0-2 14% · 0-3 14% · 0-4 11% · 0-1 9% · 0-5 6%
- Argentina favoured (87%); in line with the market.

**Panama vs England** — _neutral venue_  
Elo Panama 1797 · England 2102  |  expected goals **0.64 – 2.07**  
- **1X2:** Panama 10% · Draw 20% · England 70%   _(market 6/11/83)_
- **Goals:** Over 2.5 51% · BTTS 42%
- **Likeliest scores:** 0-2 14% · 0-1 13% · 0-3 10% · 1-1 9% · 1-2 9%
- England favoured (70%); **model higher than the market on Panama** (Δ12pp).

---
## How to read this & caveats

- **1X2 is the trustworthy output.** Goal totals run a touch low — the model under-predicts blowouts (a known, documented bias whose fix didn't generalize across backtests), so treat Over/Under as soft.

- **Group stage only.** Knockouts (extra time / penalties) are out of scope.

- **Market is a benchmark, not an input.** Where we disagree, the market is usually the sharper number; the gaps are flagged so you can judge for yourself.

- _Generated 2026-06-27 · Elo current to 2026-06-25 · model frozen 2022-11-19._