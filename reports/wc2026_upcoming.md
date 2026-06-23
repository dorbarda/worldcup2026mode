# World Cup 2026 — Opening Matches (Jun 23–Jun 27)

Model-based forecasts for the next round of group matches (24 fixtures), generated from **current Elo** (all played matches through 2026-06-22). The Dixon-Coles Poisson model is the one validated on the 2018 & 2022 backtests; its coefficients are frozen at the 2022-11-19 fit, only the ratings are current.

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

**Running RPS over 44 match(es): model 0.1756 vs market 0.1531 — market ahead.** (Tiny sample — a smoke signal, not a verdict.)

![overview](figures/wc2026/overview.png)

## All fixtures

| Date | Match | Venue | xG (H–A) | Our H/D/A | Market H/D/A | Edge | Top score |
|---|---|---|---|---|---|---|---|
| Jun 23 | Portugal v Uzbekistan | neutral | 1.82–0.73 | 63/23/14 | 84/11/5 | 21pp | 1-0 |
| Jun 23 | Colombia v DR Congo | neutral | 2.06–0.65 | 70/20/10 | 62/24/15 | 8pp | 2-0 |
| Jun 23 | England v Ghana | neutral | 2.76–0.48 | 84/12/4 | 80/14/6 | 4pp | 2-0 |
| Jun 23 | Panama v Croatia | neutral | 0.90–1.48 | 22/28/50 | 14/22/64 | 14pp | 0-1 |
| Jun 24 | Mexico v Czech Republic | Mexico (H) | 2.34–0.73 | 73/17/10 | — | — | 2-0 |
| Jun 24 | South Africa v South Korea | neutral | 0.75–1.78 | 15/24/61 | 18/25/57 | 4pp | 0-1 |
| Jun 24 | Canada v Switzerland | Canada (H) | 1.34–1.28 | 38/27/35 | — | — | 1-1 |
| Jun 24 | Bosnia and Herzegovina v Qatar | neutral | 1.34–0.99 | 44/29/27 | 69/19/13 | 24pp | 1-1 |
| Jun 24 | Scotland v Brazil | neutral | 0.75–1.77 | 15/24/61 | 12/18/70 | 9pp | 0-1 |
| Jun 24 | Morocco v Haiti | neutral | 2.14–0.62 | 72/19/9 | 81/13/6 | 9pp | 2-0 |
| Jun 25 | United States v Turkey | United States (H) | 1.59–1.08 | 49/26/25 | — | — | 1-1 |
| Jun 25 | Paraguay v Australia | neutral | 1.13–1.18 | 34/30/37 | 33/42/24 | 13pp | 1-1 |
| Jun 25 | Curaçao v Ivory Coast | neutral | 0.76–1.74 | 16/24/60 | 5/12/83 | 23pp | 0-1 |
| Jun 25 | Ecuador v Germany | neutral | 1.00–1.32 | 28/29/43 | 26/24/50 | 7pp | 1-1 |
| Jun 25 | Japan v Sweden | neutral | 1.74–0.76 | 60/24/15 | 49/28/23 | 11pp | 1-0 |
| Jun 25 | Tunisia v Netherlands | neutral | 0.57–2.34 | 7/16/77 | 5/11/85 | 8pp | 0-2 |
| Jun 26 | Egypt v Iran | neutral | 1.08–1.23 | 32/29/39 | 39/35/26 | 13pp | 1-1 |
| Jun 26 | New Zealand v Belgium | neutral | 0.76–1.76 | 15/24/61 | 7/14/80 | 19pp | 0-1 |
| Jun 26 | Cape Verde v Saudi Arabia | neutral | 1.13–1.17 | 34/30/36 | 41/27/32 | 6pp | 1-1 |
| Jun 26 | Uruguay v Spain | neutral | 0.69–1.93 | 12/22/66 | 14/22/64 | 2pp | 0-1 |
| Jun 26 | Norway v France | neutral | 0.89–1.49 | 22/27/50 | 20/23/57 | 7pp | 0-1 |
| Jun 26 | Senegal v Iraq | neutral | 1.57–0.85 | 54/26/20 | 77/15/8 | 23pp | 1-0 |
| Jun 27 | Algeria v Austria | neutral | 1.12–1.19 | 34/30/37 | 25/41/34 | 11pp | 1-1 |
| Jun 27 | Jordan v Argentina | neutral | 0.45–2.99 | 3/10/87 | 7/14/79 | 8pp | 0-2 |

## Where we disagree with the market

The model is independent of the odds, so these gaps are where our Elo-Poisson view parts from the bookmaker — and they cluster on the model's known soft spots (host-advantage calibration; less boldness on big favourites).

| Match | Our H/D/A | Market H/D/A | Edge | Lean |
|---|---|---|---|---|
| Bosnia and Herzegovina v Qatar | 44/29/27 | 69/19/13 | 24pp | model lower on Bosnia and Herzegovina |
| Senegal v Iraq | 54/26/20 | 77/15/8 | 23pp | model lower on Senegal |
| Curaçao v Ivory Coast | 16/24/60 | 5/12/83 | 23pp | model higher on Curaçao |
| Portugal v Uzbekistan | 63/23/14 | 84/11/5 | 21pp | model lower on Portugal |
| New Zealand v Belgium | 15/24/61 | 7/14/80 | 19pp | model higher on New Zealand |
| Panama v Croatia | 22/28/50 | 14/22/64 | 14pp | model higher on Panama |
| Egypt v Iran | 32/29/39 | 39/35/26 | 13pp | model lower on Egypt |
| Paraguay v Australia | 34/30/37 | 33/42/24 | 13pp | model higher on Paraguay |
| Algeria v Austria | 34/30/37 | 25/41/34 | 11pp | model higher on Algeria |
| Japan v Sweden | 60/24/15 | 49/28/23 | 11pp | model higher on Japan |

## Match-by-match

### Tuesday, June 23

**Colombia vs DR Congo** — _neutral venue_  
Elo Colombia 2085 · DR Congo 1784  |  expected goals **2.06 – 0.65**  
- **1X2:** Colombia 70% · Draw 20% · DR Congo 10%   _(market 62/24/15)_
- **Goals:** Over 2.5 51% · BTTS 42%
- **Likeliest scores:** 2-0 14% · 1-0 13% · 3-0 10% · 1-1 9% · 2-1 9%
- Colombia favoured (70%); in line with the market.

**England vs Ghana** — _neutral venue_  
Elo England 2128 · Ghana 1673  |  expected goals **2.76 – 0.48**  
- **1X2:** England 84% · Draw 12% · Ghana 4%   _(market 80/14/6)_
- **Goals:** Over 2.5 63% · BTTS 36%
- **Likeliest scores:** 2-0 15% · 3-0 14% · 1-0 11% · 4-0 9% · 2-1 7%
- England favoured (84%); in line with the market.

**Panama vs Croatia** — _neutral venue_  
Elo Panama 1816 · Croatia 1947  |  expected goals **0.90 – 1.48**  
- **1X2:** Panama 22% · Draw 28% · Croatia 50%   _(market 14/22/64)_
- **Goals:** Over 2.5 43% · BTTS 46%
- **Likeliest scores:** 0-1 13% · 1-1 13% · 0-2 10% · 0-0 10% · 1-2 9%
- Croatia favoured (50%); **model higher than the market on Panama** (Δ14pp).

**Portugal vs Uzbekistan** — _neutral venue_  
Elo Portugal 2042 · Uzbekistan 1805  |  expected goals **1.82 – 0.73**  
- **1X2:** Portugal 63% · Draw 23% · Uzbekistan 14%   _(market 84/11/5)_
- **Goals:** Over 2.5 47% · BTTS 44%
- **Likeliest scores:** 1-0 14% · 2-0 13% · 1-1 11% · 2-1 9% · 0-0 8%
- Portugal favoured (63%); **model lower than the market on Portugal** (Δ21pp).

### Wednesday, June 24

**Bosnia and Herzegovina vs Qatar** — _neutral venue_  
Elo Bosnia and Herzegovina 1659 · Qatar 1580  |  expected goals **1.34 – 0.99**  
- **1X2:** Bosnia and Herzegovina 44% · Draw 29% · Qatar 27%   _(market 69/19/13)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 12% · 0-0 10% · 0-1 9% · 2-0 9%
- Bosnia and Herzegovina favoured (44%); **model lower than the market on Bosnia and Herzegovina** (Δ24pp).

**Canada vs Switzerland** — _Canada at home_  
Elo Canada 1896 · Switzerland 1951  |  expected goals **1.34 – 1.28**  
- **1X2:** Canada 38% · Draw 27% · Switzerland 35%
- **Goals:** Over 2.5 49% · BTTS 54%
- **Likeliest scores:** 1-1 13% · 1-0 9% · 0-1 9% · 2-1 8% · 1-2 8%
- Canada favoured (38%).

**Mexico vs Czech Republic** — _Mexico at home_  
Elo Mexico 2012 · Czech Republic 1775  |  expected goals **2.34 – 0.73**  
- **1X2:** Mexico 73% · Draw 17% · Czech Republic 10%
- **Goals:** Over 2.5 59% · BTTS 47%
- **Likeliest scores:** 2-0 13% · 1-0 10% · 3-0 10% · 2-1 9% · 1-1 8%
- Mexico favoured (73%).

**Morocco vs Haiti** — _neutral venue_  
Elo Morocco 2013 · Haiti 1692  |  expected goals **2.14 – 0.62**  
- **1X2:** Morocco 72% · Draw 19% · Haiti 9%   _(market 81/13/6)_
- **Goals:** Over 2.5 52% · BTTS 41%
- **Likeliest scores:** 2-0 14% · 1-0 13% · 3-0 10% · 2-1 9% · 1-1 9%
- Morocco favoured (72%); in line with the market.

**Scotland vs Brazil** — _neutral venue_  
Elo Scotland 1854 · Brazil 2076  |  expected goals **0.75 – 1.77**  
- **1X2:** Scotland 15% · Draw 24% · Brazil 61%   _(market 12/18/70)_
- **Goals:** Over 2.5 46% · BTTS 44%
- **Likeliest scores:** 0-1 14% · 0-2 13% · 1-1 11% · 1-2 9% · 0-0 9%
- Brazil favoured (61%); in line with the market.

**South Africa vs South Korea** — _neutral venue_  
Elo South Africa 1667 · South Korea 1892  |  expected goals **0.75 – 1.78**  
- **1X2:** South Africa 15% · Draw 24% · South Korea 61%   _(market 18/25/57)_
- **Goals:** Over 2.5 46% · BTTS 44%
- **Likeliest scores:** 0-1 14% · 0-2 13% · 1-1 11% · 1-2 9% · 0-0 8%
- South Korea favoured (61%); in line with the market.

### Thursday, June 25

**Curaçao vs Ivory Coast** — _neutral venue_  
Elo Curaçao 1629 · Ivory Coast 1844  |  expected goals **0.76 – 1.74**  
- **1X2:** Curaçao 16% · Draw 24% · Ivory Coast 60%   _(market 5/12/83)_
- **Goals:** Over 2.5 46% · BTTS 45%
- **Likeliest scores:** 0-1 14% · 0-2 12% · 1-1 11% · 1-2 9% · 0-0 9%
- Ivory Coast favoured (60%); **model higher than the market on Curaçao** (Δ23pp).

**Ecuador vs Germany** — _neutral venue_  
Elo Ecuador 1961 · Germany 2033  |  expected goals **1.00 – 1.32**  
- **1X2:** Ecuador 28% · Draw 29% · Germany 43%   _(market 26/24/50)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 12% · 0-0 10% · 1-0 9% · 1-2 9%
- Germany favoured (43%); in line with the market.

**Japan vs Sweden** — _neutral venue_  
Elo Japan 2014 · Sweden 1799  |  expected goals **1.74 – 0.76**  
- **1X2:** Japan 60% · Draw 24% · Sweden 15%   _(market 49/28/23)_
- **Goals:** Over 2.5 46% · BTTS 45%
- **Likeliest scores:** 1-0 14% · 2-0 12% · 1-1 11% · 2-1 9% · 0-0 9%
- Japan favoured (60%); **model higher than the market on Japan** (Δ11pp).

**Paraguay vs Australia** — _neutral venue_  
Elo Paraguay 1905 · Australia 1917  |  expected goals **1.13 – 1.18**  
- **1X2:** Paraguay 34% · Draw 30% · Australia 37%   _(market 33/42/24)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 11% · 1-0 11% · 0-0 11% · 1-2 8%
- Australia favoured (37%); **model higher than the market on Paraguay** (Δ13pp).

**Tunisia vs Netherlands** — _neutral venue_  
Elo Tunisia 1672 · Netherlands 2040  |  expected goals **0.57 – 2.34**  
- **1X2:** Tunisia 7% · Draw 16% · Netherlands 77%   _(market 5/11/85)_
- **Goals:** Over 2.5 56% · BTTS 40%
- **Likeliest scores:** 0-2 15% · 0-1 12% · 0-3 12% · 1-2 8% · 1-1 8%
- Netherlands favoured (77%); in line with the market.

**United States vs Turkey** — _United States at home_  
Elo United States 1925 · Turkey 1889  |  expected goals **1.59 – 1.08**  
- **1X2:** United States 49% · Draw 26% · Turkey 25%
- **Goals:** Over 2.5 50% · BTTS 53%
- **Likeliest scores:** 1-1 12% · 1-0 10% · 2-1 9% · 2-0 9% · 0-0 7%
- United States favoured (49%).

### Friday, June 26

**Cape Verde vs Saudi Arabia** — _neutral venue_  
Elo Cape Verde 1701 · Saudi Arabia 1710  |  expected goals **1.13 – 1.17**  
- **1X2:** Cape Verde 34% · Draw 30% · Saudi Arabia 36%   _(market 41/27/32)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 11% · 1-0 11% · 0-0 11% · 1-2 8%
- Saudi Arabia favoured (36%); in line with the market.

**Egypt vs Iran** — _neutral venue_  
Elo Egypt 1857 · Iran 1889  |  expected goals **1.08 – 1.23**  
- **1X2:** Egypt 32% · Draw 29% · Iran 39%   _(market 39/35/26)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 12% · 0-0 11% · 1-0 10% · 1-2 8%
- Iran favoured (39%); **model lower than the market on Egypt** (Δ13pp).

**New Zealand vs Belgium** — _neutral venue_  
Elo New Zealand 1713 · Belgium 1932  |  expected goals **0.76 – 1.76**  
- **1X2:** New Zealand 15% · Draw 24% · Belgium 61%   _(market 7/14/80)_
- **Goals:** Over 2.5 46% · BTTS 44%
- **Likeliest scores:** 0-1 14% · 0-2 12% · 1-1 11% · 1-2 9% · 0-0 9%
- Belgium favoured (61%); **model higher than the market on New Zealand** (Δ19pp).

**Norway vs France** — _neutral venue_  
Elo Norway 2028 · France 2160  |  expected goals **0.89 – 1.49**  
- **1X2:** Norway 22% · Draw 27% · France 50%   _(market 20/23/57)_
- **Goals:** Over 2.5 43% · BTTS 46%
- **Likeliest scores:** 0-1 13% · 1-1 13% · 0-2 10% · 0-0 10% · 1-2 9%
- France favoured (50%); in line with the market.

**Senegal vs Iraq** — _neutral venue_  
Elo Senegal 1873 · Iraq 1712  |  expected goals **1.57 – 0.85**  
- **1X2:** Senegal 54% · Draw 26% · Iraq 20%   _(market 77/15/8)_
- **Goals:** Over 2.5 44% · BTTS 46%
- **Likeliest scores:** 1-0 13% · 1-1 12% · 2-0 11% · 0-0 9% · 2-1 9%
- Senegal favoured (54%); **model lower than the market on Senegal** (Δ23pp).

**Uruguay vs Spain** — _neutral venue_  
Elo Uruguay 1939 · Spain 2207  |  expected goals **0.69 – 1.93**  
- **1X2:** Uruguay 12% · Draw 22% · Spain 66%   _(market 14/22/64)_
- **Goals:** Over 2.5 49% · BTTS 43%
- **Likeliest scores:** 0-1 14% · 0-2 14% · 1-1 10% · 1-2 9% · 0-3 9%
- Spain favoured (66%); in line with the market.

### Saturday, June 27

**Algeria vs Austria** — _neutral venue_  
Elo Algeria 1889 · Austria 1905  |  expected goals **1.12 – 1.19**  
- **1X2:** Algeria 34% · Draw 30% · Austria 37%   _(market 25/41/34)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 11% · 0-0 11% · 1-0 10% · 1-2 8%
- Austria favoured (37%); **model higher than the market on Algeria** (Δ11pp).

**Jordan vs Argentina** — _neutral venue_  
Elo Jordan 1727 · Argentina 2223  |  expected goals **0.45 – 2.99**  
- **1X2:** Jordan 3% · Draw 10% · Argentina 87%   _(market 7/14/79)_
- **Goals:** Over 2.5 67% · BTTS 34%
- **Likeliest scores:** 0-2 14% · 0-3 14% · 0-4 11% · 0-1 9% · 0-5 6%
- Argentina favoured (87%); in line with the market.

---
## How to read this & caveats

- **1X2 is the trustworthy output.** Goal totals run a touch low — the model under-predicts blowouts (a known, documented bias whose fix didn't generalize across backtests), so treat Over/Under as soft.

- **Group stage only.** Knockouts (extra time / penalties) are out of scope.

- **Market is a benchmark, not an input.** Where we disagree, the market is usually the sharper number; the gaps are flagged so you can judge for yourself.

- _Generated 2026-06-23 · Elo current to 2026-06-22 · model frozen 2022-11-19._