# World Cup 2026 — Opening Matches (Jun 28–Jul 03)

Model-based forecasts for the next round of group matches (16 fixtures), generated from **current Elo** (all played matches through 2026-06-27). The Dixon-Coles Poisson model is the one validated on the 2018 & 2022 backtests; its coefficients are frozen at the 2022-11-19 fit, only the ratings are current.

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
| Egypt v Iran | 1-1 (draw) | 32/30/39 | 39/36/25 | market |
| New Zealand v Belgium | 1-5 (away) | 15/24/61 | 7/12/81 | market |
| Cape Verde v Saudi Arabia | 0-0 (draw) | 34/30/36 | 36/29/35 | model |
| Uruguay v Spain | 0-1 (away) | 12/22/66 | 15/26/59 | model |
| Norway v France | 1-4 (away) | 22/27/50 | 21/21/58 | market |
| Senegal v Iraq | 5-0 (home) | 54/26/20 | 78/14/8 | market |
| Algeria v Austria | 3-3 (draw) | 34/30/37 | 23/45/32 | market |
| Jordan v Argentina | 1-3 (away) | 3/10/88 | 6/11/83 | model |
| Colombia v Portugal | 0-0 (draw) | 38/30/32 | 28/25/48 | model |
| DR Congo v Uzbekistan | 3-1 (home) | 35/30/36 | 60/23/17 | market |
| Panama v England | 0-2 (away) | 10/20/70 | 6/11/83 | market |
| Croatia v Ghana | 2-1 (home) | 66/22/12 | 50/31/19 | model |

**Running RPS over 72 match(es): model 0.1677 vs market nan — level.** (Tiny sample — a smoke signal, not a verdict.)

![overview](figures/wc2026/overview.png)

## All fixtures

| Date | Match | Venue | xG (H–A) | Our H/D/A | Market H/D/A | Edge | Top score |
|---|---|---|---|---|---|---|---|
| Jun 28 | South Africa v Canada | neutral | 0.87–1.53 | 21/27/52 | 16/26/58 | 6pp | 0-1 |
| Jun 29 | Brazil v Japan | neutral | 1.40–0.95 | 47/28/25 | 56/25/18 | 9pp | 1-1 |
| Jun 29 | Germany v Paraguay | neutral | 1.37–0.97 | 46/29/26 | 70/19/11 | 25pp | 1-1 |
| Jun 29 | Netherlands v Morocco | neutral | 1.21–1.10 | 38/30/33 | 45/30/26 | 7pp | 1-1 |
| Jun 30 | Ivory Coast v Norway | neutral | 0.90–1.48 | 22/28/50 | 26/27/47 | 4pp | 0-1 |
| Jun 30 | France v Sweden | neutral | 2.38–0.56 | 78/16/7 | 75/16/9 | 3pp | 2-0 |
| Jun 30 | Mexico v Ecuador | Mexico (H) | 1.57–1.09 | 48/26/26 | 43/31/25 | 5pp | 1-1 |
| Jul 01 | England v DR Congo | neutral | 2.03–0.66 | 69/20/11 | 75/17/8 | 6pp | 2-0 |
| Jul 01 | Belgium v Senegal | neutral | 1.27–1.05 | 41/29/30 | 45/29/26 | 4pp | 1-1 |
| Jul 01 | United States v Bosnia and Herzegovina | United States (H) | 2.14–0.80 | 68/20/12 | 70/19/11 | 2pp | 2-0 |
| Jul 02 | Spain v Austria | neutral | 2.11–0.63 | 71/19/9 | 75/18/7 | 3pp | 2-0 |
| Jul 02 | Portugal v Croatia | neutral | 1.38–0.97 | 46/29/26 | 52/28/20 | 6pp | 1-1 |
| Jul 02 | Switzerland v Algeria | neutral | 1.38–0.96 | 46/28/26 | 50/27/23 | 5pp | 1-1 |
| Jul 03 | Australia v Egypt | neutral | 1.29–1.04 | 42/29/29 | 29/33/38 | 12pp | 1-1 |
| Jul 03 | Argentina v Cape Verde | neutral | 3.16–0.42 | 89/8/2 | 83/12/5 | 6pp | 3-0 |
| Jul 03 | Colombia v Ghana | neutral | 2.50–0.53 | 80/14/6 | 59/26/15 | 21pp | 2-0 |

## Where we disagree with the market

The model is independent of the odds, so these gaps are where our Elo-Poisson view parts from the bookmaker — and they cluster on the model's known soft spots (host-advantage calibration; less boldness on big favourites).

| Match | Our H/D/A | Market H/D/A | Edge | Lean |
|---|---|---|---|---|
| Germany v Paraguay | 46/29/26 | 70/19/11 | 25pp | model lower on Germany |
| Colombia v Ghana | 80/14/6 | 59/26/15 | 21pp | model higher on Colombia |
| Australia v Egypt | 42/29/29 | 29/33/38 | 12pp | model higher on Australia |

## Match-by-match

### Sunday, June 28

**South Africa vs Canada** — _neutral venue_  
Elo South Africa 1714 · Canada 1862  |  expected goals **0.87 – 1.53**  
- **1X2:** South Africa 21% · Draw 27% · Canada 52%   _(market 16/26/58)_
- **Goals:** Over 2.5 43% · BTTS 46%
- **Likeliest scores:** 0-1 13% · 1-1 13% · 0-2 11% · 0-0 10% · 1-2 9%
- Canada favoured (52%); in line with the market.

### Monday, June 29

**Brazil vs Japan** — _neutral venue_  
Elo Brazil 2099 · Japan 1998  |  expected goals **1.40 – 0.95**  
- **1X2:** Brazil 47% · Draw 28% · Japan 25%   _(market 56/25/18)_
- **Goals:** Over 2.5 42% · BTTS 47%
- **Likeliest scores:** 1-1 13% · 1-0 13% · 0-0 10% · 2-0 9% · 2-1 9%
- Brazil favoured (47%); in line with the market.

**Germany vs Paraguay** — _neutral venue_  
Elo Germany 1997 · Paraguay 1906  |  expected goals **1.37 – 0.97**  
- **1X2:** Germany 46% · Draw 29% · Paraguay 26%   _(market 70/19/11)_
- **Goals:** Over 2.5 42% · BTTS 47%
- **Likeliest scores:** 1-1 13% · 1-0 13% · 0-0 10% · 2-0 9% · 2-1 9%
- Germany favoured (46%); **model lower than the market on Germany** (Δ25pp).

**Netherlands vs Morocco** — _neutral venue_  
Elo Netherlands 2050 · Morocco 2025  |  expected goals **1.21 – 1.10**  
- **1X2:** Netherlands 38% · Draw 30% · Morocco 33%   _(market 45/30/26)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 11% · 0-0 11% · 0-1 10% · 2-1 8%
- Netherlands favoured (38%); in line with the market.

### Tuesday, June 30

**France vs Sweden** — _neutral venue_  
Elo France 2193 · Sweden 1815  |  expected goals **2.38 – 0.56**  
- **1X2:** France 78% · Draw 16% · Sweden 7%   _(market 75/16/9)_
- **Goals:** Over 2.5 56% · BTTS 39%
- **Likeliest scores:** 2-0 15% · 1-0 12% · 3-0 12% · 2-1 8% · 1-1 7%
- France favoured (78%); in line with the market.

**Ivory Coast vs Norway** — _neutral venue_  
Elo Ivory Coast 1864 · Norway 1994  |  expected goals **0.90 – 1.48**  
- **1X2:** Ivory Coast 22% · Draw 28% · Norway 50%   _(market 26/27/47)_
- **Goals:** Over 2.5 43% · BTTS 46%
- **Likeliest scores:** 0-1 13% · 1-1 13% · 0-2 10% · 0-0 10% · 1-2 9%
- Norway favoured (50%); in line with the market.

**Mexico vs Ecuador** — _Mexico at home_  
Elo Mexico 2025 · Ecuador 1998  |  expected goals **1.57 – 1.09**  
- **1X2:** Mexico 48% · Draw 26% · Ecuador 26%   _(market 43/31/25)_
- **Goals:** Over 2.5 50% · BTTS 53%
- **Likeliest scores:** 1-1 13% · 1-0 10% · 2-1 9% · 2-0 9% · 0-0 8%
- Mexico favoured (48%); in line with the market.

### Wednesday, July 01

**Belgium vs Senegal** — _neutral venue_  
Elo Belgium 1957 · Senegal 1907  |  expected goals **1.27 – 1.05**  
- **1X2:** Belgium 41% · Draw 29% · Senegal 30%   _(market 45/29/26)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 12% · 0-0 10% · 0-1 10% · 2-1 8%
- Belgium favoured (41%); in line with the market.

**England vs DR Congo** — _neutral venue_  
Elo England 2115 · DR Congo 1821  |  expected goals **2.03 – 0.66**  
- **1X2:** England 69% · Draw 20% · DR Congo 11%   _(market 75/17/8)_
- **Goals:** Over 2.5 50% · BTTS 42%
- **Likeliest scores:** 2-0 14% · 1-0 13% · 1-1 10% · 3-0 10% · 2-1 9%
- England favoured (69%); in line with the market.

**United States vs Bosnia and Herzegovina** — _United States at home_  
Elo United States 1884 · Bosnia and Herzegovina 1694  |  expected goals **2.14 – 0.80**  
- **1X2:** United States 68% · Draw 20% · Bosnia and Herzegovina 12%   _(market 70/19/11)_
- **Goals:** Over 2.5 56% · BTTS 49%
- **Likeliest scores:** 2-0 12% · 1-0 11% · 2-1 10% · 1-1 9% · 3-0 9%
- United States favoured (68%); in line with the market.

### Thursday, July 02

**Portugal vs Croatia** — _neutral venue_  
Elo Portugal 2069 · Croatia 1977  |  expected goals **1.38 – 0.97**  
- **1X2:** Portugal 46% · Draw 29% · Croatia 26%   _(market 52/28/20)_
- **Goals:** Over 2.5 42% · BTTS 47%
- **Likeliest scores:** 1-1 13% · 1-0 13% · 0-0 10% · 2-0 9% · 2-1 9%
- Portugal favoured (46%); in line with the market.

**Spain vs Austria** — _neutral venue_  
Elo Spain 2218 · Austria 1903  |  expected goals **2.11 – 0.63**  
- **1X2:** Spain 71% · Draw 19% · Austria 9%   _(market 75/18/7)_
- **Goals:** Over 2.5 52% · BTTS 42%
- **Likeliest scores:** 2-0 14% · 1-0 13% · 3-0 10% · 2-1 9% · 1-1 9%
- Spain favoured (71%); in line with the market.

**Switzerland vs Algeria** — _neutral venue_  
Elo Switzerland 1985 · Algeria 1890  |  expected goals **1.38 – 0.96**  
- **1X2:** Switzerland 46% · Draw 28% · Algeria 26%   _(market 50/27/23)_
- **Goals:** Over 2.5 42% · BTTS 47%
- **Likeliest scores:** 1-1 13% · 1-0 13% · 0-0 10% · 2-0 9% · 2-1 9%
- Switzerland favoured (46%); in line with the market.

### Friday, July 03

**Argentina vs Cape Verde** — _neutral venue_  
Elo Argentina 2228 · Cape Verde 1702  |  expected goals **3.16 – 0.42**  
- **1X2:** Argentina 89% · Draw 8% · Cape Verde 2%   _(market 83/12/5)_
- **Goals:** Over 2.5 69% · BTTS 33%
- **Likeliest scores:** 3-0 15% · 2-0 14% · 4-0 12% · 1-0 9% · 5-0 7%
- Argentina favoured (89%); in line with the market.

**Australia vs Egypt** — _neutral venue_  
Elo Australia 1916 · Egypt 1860  |  expected goals **1.29 – 1.04**  
- **1X2:** Australia 42% · Draw 29% · Egypt 29%   _(market 29/33/38)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 12% · 0-0 10% · 0-1 10% · 2-1 8%
- Australia favoured (42%); **model higher than the market on Australia** (Δ12pp).

**Colombia vs Ghana** — _neutral venue_  
Elo Colombia 2092 · Ghana 1689  |  expected goals **2.50 – 0.53**  
- **1X2:** Colombia 80% · Draw 14% · Ghana 6%   _(market 59/26/15)_
- **Goals:** Over 2.5 58% · BTTS 38%
- **Likeliest scores:** 2-0 15% · 3-0 13% · 1-0 12% · 2-1 8% · 4-0 8%
- Colombia favoured (80%); **model higher than the market on Colombia** (Δ21pp).

---
## How to read this & caveats

- **1X2 is the trustworthy output.** Goal totals run a touch low — the model under-predicts blowouts (a known, documented bias whose fix didn't generalize across backtests), so treat Over/Under as soft.

- **Group stage only.** Knockouts (extra time / penalties) are out of scope.

- **Market is a benchmark, not an input.** Where we disagree, the market is usually the sharper number; the gaps are flagged so you can judge for yourself.

- _Generated 2026-06-28 · Elo current to 2026-06-27 · model frozen 2022-11-19._