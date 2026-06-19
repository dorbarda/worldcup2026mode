# World Cup 2026 — Opening Matches (Jun 19–Jun 24)

Model-based forecasts for the next round of group matches (24 fixtures), generated from **current Elo** (all played matches through 2026-06-18). The Dixon-Coles Poisson model is the one validated on the 2018 & 2022 backtests; its coefficients are frozen at the 2022-11-19 fit, only the ratings are current.

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

**Running RPS over 28 match(es): model 0.1920 vs market 0.1635 — market ahead.** (Tiny sample — a smoke signal, not a verdict.)

![overview](figures/wc2026/overview.png)

## All fixtures

| Date | Match | Venue | xG (H–A) | Our H/D/A | Market H/D/A | Edge | Top score |
|---|---|---|---|---|---|---|---|
| Jun 19 | Scotland v Morocco | neutral | 0.92–1.45 | 23/28/49 | 17/27/56 | 7pp | 1-1 |
| Jun 19 | Brazil v Haiti | neutral | 2.31–0.58 | 76/17/7 | 87/9/4 | 11pp | 2-0 |
| Jun 19 | United States v Australia | United States (H) | 1.29–1.33 | 35/27/37 | 60/22/18 | 25pp | 1-1 |
| Jun 19 | Turkey v Paraguay | neutral | 1.28–1.04 | 41/29/30 | 47/28/25 | 6pp | 1-1 |
| Jun 20 | Germany v Ivory Coast | neutral | 1.55–0.86 | 53/27/20 | 62/21/17 | 9pp | 1-0 |
| Jun 20 | Ecuador v Curaçao | neutral | 2.40–0.56 | 78/16/6 | 86/10/4 | 8pp | 2-0 |
| Jun 20 | Netherlands v Sweden | neutral | 1.64–0.81 | 56/26/18 | 55/25/20 | 3pp | 1-0 |
| Jun 20 | Tunisia v Japan | neutral | 0.64–2.09 | 10/19/71 | 14/23/63 | 8pp | 0-2 |
| Jun 21 | Belgium v Iran | neutral | 1.27–1.04 | 41/29/30 | 67/20/12 | 26pp | 1-1 |
| Jun 21 | New Zealand v Egypt | neutral | 1.00–1.33 | 28/29/43 | 17/24/59 | 16pp | 1-1 |
| Jun 21 | Spain v Saudi Arabia | neutral | 2.92–0.46 | 87/10/3 | 87/10/4 | 1pp | 2-0 |
| Jun 21 | Uruguay v Cape Verde | neutral | 1.96–0.68 | 67/21/11 | 66/23/12 | 2pp | 2-0 |
| Jun 22 | France v Iraq | neutral | 2.65–0.50 | 83/13/5 | 88/9/3 | 5pp | 2-0 |
| Jun 22 | Norway v Senegal | neutral | 1.44–0.93 | 48/28/24 | 41/27/32 | 8pp | 1-1 |
| Jun 22 | Argentina v Austria | neutral | 2.01–0.66 | 69/21/11 | 60/24/16 | 9pp | 2-0 |
| Jun 22 | Jordan v Algeria | neutral | 0.91–1.46 | 23/28/49 | 16/23/61 | 11pp | 0-1 |
| Jun 23 | Portugal v Uzbekistan | neutral | 1.82–0.73 | 63/23/14 | 80/14/6 | 17pp | 1-0 |
| Jun 23 | Colombia v DR Congo | neutral | 2.06–0.65 | 70/20/10 | 63/23/14 | 7pp | 2-0 |
| Jun 23 | England v Ghana | neutral | 2.76–0.48 | 84/12/4 | 78/15/7 | 6pp | 2-0 |
| Jun 23 | Panama v Croatia | neutral | 0.90–1.48 | 22/28/50 | 14/24/62 | 12pp | 0-1 |
| Jun 24 | Mexico v Czech Republic | Mexico (H) | 2.34–0.73 | 73/17/10 | — | — | 2-0 |
| Jun 24 | South Africa v South Korea | neutral | 0.75–1.78 | 15/24/61 | 17/25/58 | 3pp | 0-1 |
| Jun 24 | Canada v Switzerland | Canada (H) | 1.34–1.28 | 38/27/35 | — | — | 1-1 |
| Jun 24 | Bosnia and Herzegovina v Qatar | neutral | 1.34–0.99 | 44/29/27 | 67/19/14 | 23pp | 1-1 |

## Where we disagree with the market

The model is independent of the odds, so these gaps are where our Elo-Poisson view parts from the bookmaker — and they cluster on the model's known soft spots (host-advantage calibration; less boldness on big favourites).

| Match | Our H/D/A | Market H/D/A | Edge | Lean |
|---|---|---|---|---|
| Belgium v Iran | 41/29/30 | 67/20/12 | 26pp | model lower on Belgium |
| United States v Australia | 35/27/37 | 60/22/18 | 25pp | model lower on United States |
| Bosnia and Herzegovina v Qatar | 44/29/27 | 67/19/14 | 23pp | model lower on Bosnia and Herzegovina |
| Portugal v Uzbekistan | 63/23/14 | 80/14/6 | 17pp | model lower on Portugal |
| New Zealand v Egypt | 28/29/43 | 17/24/59 | 16pp | model higher on New Zealand |
| Panama v Croatia | 22/28/50 | 14/24/62 | 12pp | model higher on Panama |
| Jordan v Algeria | 23/28/49 | 16/23/61 | 11pp | model higher on Jordan |
| Brazil v Haiti | 76/17/7 | 87/9/4 | 11pp | model lower on Brazil |

## Match-by-match

### Friday, June 19

**Brazil vs Haiti** — _neutral venue_  
Elo Brazil 2065 · Haiti 1704  |  expected goals **2.31 – 0.58**  
- **1X2:** Brazil 76% · Draw 17% · Haiti 7%   _(market 87/9/4)_
- **Goals:** Over 2.5 55% · BTTS 40%
- **Likeliest scores:** 2-0 15% · 1-0 13% · 3-0 11% · 2-1 9% · 1-1 8%
- Brazil favoured (76%); **model lower than the market on Brazil** (Δ11pp).

**Scotland vs Morocco** — _neutral venue_  
Elo Scotland 1874 · Morocco 1993  |  expected goals **0.92 – 1.45**  
- **1X2:** Scotland 23% · Draw 28% · Morocco 49%   _(market 17/27/56)_
- **Goals:** Over 2.5 42% · BTTS 47%
- **Likeliest scores:** 1-1 13% · 0-1 13% · 0-0 10% · 0-2 10% · 1-2 9%
- Morocco favoured (49%); in line with the market.

**Turkey vs Paraguay** — _neutral venue_  
Elo Turkey 1923 · Paraguay 1871  |  expected goals **1.28 – 1.04**  
- **1X2:** Turkey 41% · Draw 29% · Paraguay 30%   _(market 47/28/25)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 12% · 0-0 10% · 0-1 10% · 2-1 8%
- Turkey favoured (41%); in line with the market.

**United States vs Australia** — _United States at home_  
Elo United States 1883 · Australia 1959  |  expected goals **1.29 – 1.33**  
- **1X2:** United States 35% · Draw 27% · Australia 37%   _(market 60/22/18)_
- **Goals:** Over 2.5 49% · BTTS 54%
- **Likeliest scores:** 1-1 13% · 0-1 9% · 1-0 9% · 1-2 8% · 2-1 8%
- Australia favoured (37%); **model lower than the market on United States** (Δ25pp).

### Saturday, June 20

**Ecuador vs Curaçao** — _neutral venue_  
Elo Ecuador 1985 · Curaçao 1605  |  expected goals **2.40 – 0.56**  
- **1X2:** Ecuador 78% · Draw 16% · Curaçao 6%   _(market 86/10/4)_
- **Goals:** Over 2.5 57% · BTTS 39%
- **Likeliest scores:** 2-0 15% · 1-0 12% · 3-0 12% · 2-1 8% · 1-1 7%
- Ecuador favoured (78%); in line with the market.

**Germany vs Ivory Coast** — _neutral venue_  
Elo Germany 2016 · Ivory Coast 1861  |  expected goals **1.55 – 0.86**  
- **1X2:** Germany 53% · Draw 27% · Ivory Coast 20%   _(market 62/21/17)_
- **Goals:** Over 2.5 43% · BTTS 46%
- **Likeliest scores:** 1-0 13% · 1-1 13% · 2-0 11% · 0-0 10% · 2-1 9%
- Germany favoured (53%); in line with the market.

**Netherlands vs Sweden** — _neutral venue_  
Elo Netherlands 2011 · Sweden 1828  |  expected goals **1.64 – 0.81**  
- **1X2:** Netherlands 56% · Draw 26% · Sweden 18%   _(market 55/25/20)_
- **Goals:** Over 2.5 44% · BTTS 45%
- **Likeliest scores:** 1-0 14% · 1-1 12% · 2-0 12% · 2-1 9% · 0-0 9%
- Netherlands favoured (56%); in line with the market.

**Tunisia vs Japan** — _neutral venue_  
Elo Tunisia 1688 · Japan 1998  |  expected goals **0.64 – 2.09**  
- **1X2:** Tunisia 10% · Draw 19% · Japan 71%   _(market 14/23/63)_
- **Goals:** Over 2.5 51% · BTTS 42%
- **Likeliest scores:** 0-2 14% · 0-1 13% · 0-3 10% · 1-1 9% · 1-2 9%
- Japan favoured (71%); in line with the market.

### Sunday, June 21

**Belgium vs Iran** — _neutral venue_  
Elo Belgium 1936 · Iran 1885  |  expected goals **1.27 – 1.04**  
- **1X2:** Belgium 41% · Draw 29% · Iran 30%   _(market 67/20/12)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 12% · 0-0 10% · 0-1 10% · 2-1 8%
- Belgium favoured (41%); **model lower than the market on Belgium** (Δ26pp).

**New Zealand vs Egypt** — _neutral venue_  
Elo New Zealand 1749 · Egypt 1821  |  expected goals **1.00 – 1.33**  
- **1X2:** New Zealand 28% · Draw 29% · Egypt 43%   _(market 17/24/59)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 0-1 12% · 0-0 10% · 1-0 9% · 1-2 9%
- Egypt favoured (43%); **model higher than the market on New Zealand** (Δ16pp).

**Spain vs Saudi Arabia** — _neutral venue_  
Elo Spain 2201 · Saudi Arabia 1717  |  expected goals **2.92 – 0.46**  
- **1X2:** Spain 87% · Draw 10% · Saudi Arabia 3%   _(market 87/10/4)_
- **Goals:** Over 2.5 66% · BTTS 35%
- **Likeliest scores:** 2-0 15% · 3-0 14% · 4-0 10% · 1-0 10% · 2-1 7%
- Spain favoured (87%); in line with the market.

**Uruguay vs Cape Verde** — _neutral venue_  
Elo Uruguay 1959 · Cape Verde 1681  |  expected goals **1.96 – 0.68**  
- **1X2:** Uruguay 67% · Draw 21% · Cape Verde 11%   _(market 66/23/12)_
- **Goals:** Over 2.5 49% · BTTS 43%
- **Likeliest scores:** 2-0 14% · 1-0 14% · 1-1 10% · 2-1 9% · 3-0 9%
- Uruguay favoured (67%); in line with the market.

### Monday, June 22

**Argentina vs Austria** — _neutral venue_  
Elo Argentina 2208 · Austria 1919  |  expected goals **2.01 – 0.66**  
- **1X2:** Argentina 69% · Draw 21% · Austria 11%   _(market 60/24/16)_
- **Goals:** Over 2.5 50% · BTTS 42%
- **Likeliest scores:** 2-0 14% · 1-0 13% · 1-1 10% · 3-0 9% · 2-1 9%
- Argentina favoured (69%); in line with the market.

**France vs Iraq** — _neutral venue_  
Elo France 2152 · Iraq 1720  |  expected goals **2.65 – 0.50**  
- **1X2:** France 83% · Draw 13% · Iraq 5%   _(market 88/9/3)_
- **Goals:** Over 2.5 61% · BTTS 37%
- **Likeliest scores:** 2-0 15% · 3-0 13% · 1-0 11% · 4-0 9% · 2-1 8%
- France favoured (83%); in line with the market.

**Jordan vs Algeria** — _neutral venue_  
Elo Jordan 1746 · Algeria 1869  |  expected goals **0.91 – 1.46**  
- **1X2:** Jordan 23% · Draw 28% · Algeria 49%   _(market 16/23/61)_
- **Goals:** Over 2.5 42% · BTTS 47%
- **Likeliest scores:** 0-1 13% · 1-1 13% · 0-2 10% · 0-0 10% · 1-2 9%
- Algeria favoured (49%); **model higher than the market on Jordan** (Δ11pp).

**Norway vs Senegal** — _neutral venue_  
Elo Norway 2007 · Senegal 1893  |  expected goals **1.44 – 0.93**  
- **1X2:** Norway 48% · Draw 28% · Senegal 24%   _(market 41/27/32)_
- **Goals:** Over 2.5 42% · BTTS 47%
- **Likeliest scores:** 1-1 13% · 1-0 13% · 0-0 10% · 2-0 10% · 2-1 9%
- Norway favoured (48%); in line with the market.

### Tuesday, June 23

**Colombia vs DR Congo** — _neutral venue_  
Elo Colombia 2085 · DR Congo 1784  |  expected goals **2.06 – 0.65**  
- **1X2:** Colombia 70% · Draw 20% · DR Congo 10%   _(market 63/23/14)_
- **Goals:** Over 2.5 51% · BTTS 42%
- **Likeliest scores:** 2-0 14% · 1-0 13% · 3-0 10% · 1-1 9% · 2-1 9%
- Colombia favoured (70%); in line with the market.

**England vs Ghana** — _neutral venue_  
Elo England 2128 · Ghana 1673  |  expected goals **2.76 – 0.48**  
- **1X2:** England 84% · Draw 12% · Ghana 4%   _(market 78/15/7)_
- **Goals:** Over 2.5 63% · BTTS 36%
- **Likeliest scores:** 2-0 15% · 3-0 14% · 1-0 11% · 4-0 9% · 2-1 7%
- England favoured (84%); in line with the market.

**Panama vs Croatia** — _neutral venue_  
Elo Panama 1816 · Croatia 1947  |  expected goals **0.90 – 1.48**  
- **1X2:** Panama 22% · Draw 28% · Croatia 50%   _(market 14/24/62)_
- **Goals:** Over 2.5 43% · BTTS 46%
- **Likeliest scores:** 0-1 13% · 1-1 13% · 0-2 10% · 0-0 10% · 1-2 9%
- Croatia favoured (50%); **model higher than the market on Panama** (Δ12pp).

**Portugal vs Uzbekistan** — _neutral venue_  
Elo Portugal 2042 · Uzbekistan 1805  |  expected goals **1.82 – 0.73**  
- **1X2:** Portugal 63% · Draw 23% · Uzbekistan 14%   _(market 80/14/6)_
- **Goals:** Over 2.5 47% · BTTS 44%
- **Likeliest scores:** 1-0 14% · 2-0 13% · 1-1 11% · 2-1 9% · 0-0 8%
- Portugal favoured (63%); **model lower than the market on Portugal** (Δ17pp).

### Wednesday, June 24

**Bosnia and Herzegovina vs Qatar** — _neutral venue_  
Elo Bosnia and Herzegovina 1659 · Qatar 1580  |  expected goals **1.34 – 0.99**  
- **1X2:** Bosnia and Herzegovina 44% · Draw 29% · Qatar 27%   _(market 67/19/14)_
- **Goals:** Over 2.5 41% · BTTS 47%
- **Likeliest scores:** 1-1 14% · 1-0 12% · 0-0 10% · 0-1 9% · 2-0 9%
- Bosnia and Herzegovina favoured (44%); **model lower than the market on Bosnia and Herzegovina** (Δ23pp).

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

**South Africa vs South Korea** — _neutral venue_  
Elo South Africa 1667 · South Korea 1892  |  expected goals **0.75 – 1.78**  
- **1X2:** South Africa 15% · Draw 24% · South Korea 61%   _(market 17/25/58)_
- **Goals:** Over 2.5 46% · BTTS 44%
- **Likeliest scores:** 0-1 14% · 0-2 13% · 1-1 11% · 1-2 9% · 0-0 8%
- South Korea favoured (61%); in line with the market.

---
## How to read this & caveats

- **1X2 is the trustworthy output.** Goal totals run a touch low — the model under-predicts blowouts (a known, documented bias whose fix didn't generalize across backtests), so treat Over/Under as soft.

- **Group stage only.** Knockouts (extra time / penalties) are out of scope.

- **Market is a benchmark, not an input.** Where we disagree, the market is usually the sharper number; the gaps are flagged so you can judge for yourself.

- _Generated 2026-06-19 · Elo current to 2026-06-18 · model frozen 2022-11-19._