# World Cup 2026 — Opening Matches (Jun 16–Jun 21)

Model-based forecasts for the next round of group matches (24 fixtures), generated from **current Elo** (all played matches through 2026-06-15). The Dixon-Coles Poisson model is the one validated on the 2018 & 2022 backtests; its coefficients are frozen at the 2022-11-19 fit, only the ratings are current.

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

**Running RPS over 16 match(es): model 0.2230 vs market 0.2067 — market ahead.** (Tiny sample — a smoke signal, not a verdict.)

![overview](figures/wc2026/overview.png)

## All fixtures

| Date | Match | Venue | xG (H–A) | Our H/D/A | Market H/D/A | Edge | Top score |
|---|---|---|---|---|---|---|---|
| Jun 16 | France v Senegal | neutral | 1.60–0.69 | 59/26/15 | 65/21/13 | 7pp | 1-0 |
| Jun 16 | Iraq v Norway | neutral | 0.65–1.68 | 14/25/62 | 7/14/79 | 17pp | 0-1 |
| Jun 16 | Argentina v Algeria | neutral | 1.90–0.58 | 69/21/10 | 66/21/13 | 3pp | 1-0 |
| Jun 16 | Austria v Jordan | neutral | 1.30–0.85 | 46/30/24 | 70/19/11 | 24pp | 1-0 |
| Jun 17 | Portugal v DR Congo | neutral | 1.87–0.59 | 68/22/11 | 75/17/9 | 7pp | 1-0 |
| Jun 17 | Uzbekistan v Colombia | neutral | 0.65–1.68 | 14/25/62 | 11/20/69 | 7pp | 0-1 |
| Jun 17 | England v Croatia | neutral | 1.32–0.83 | 48/30/23 | 55/26/19 | 8pp | 1-0 |
| Jun 17 | Ghana v Panama | neutral | 0.66–1.66 | 14/25/61 | 43/29/28 | 33pp | 0-1 |
| Jun 18 | Czech Republic v South Africa | neutral | 1.35–0.82 | 49/29/22 | 54/25/20 | 6pp | 1-0 |
| Jun 18 | Mexico v South Korea | Mexico (H) | 1.61–0.88 | 54/26/20 | 47/29/24 | 6pp | 1-0 |
| Jun 18 | Switzerland v Bosnia and Herzegovina | neutral | 1.70–0.65 | 62/24/13 | 61/24/15 | 2pp | 1-0 |
| Jun 18 | Canada v Qatar | Canada (H) | 2.37–0.60 | 77/16/7 | 75/17/8 | 1pp | 2-0 |
| Jun 19 | Scotland v Morocco | neutral | 0.84–1.32 | 23/30/47 | 18/26/55 | 8pp | 0-1 |
| Jun 19 | Brazil v Haiti | neutral | 2.10–0.52 | 74/19/8 | 87/9/4 | 13pp | 2-0 |
| Jun 19 | United States v Australia | United States (H) | 1.17–1.21 | 34/29/37 | 59/23/18 | 25pp | 1-1 |
| Jun 19 | Turkey v Paraguay | neutral | 1.16–0.95 | 40/31/29 | 47/28/24 | 7pp | 1-1 |
| Jun 20 | Germany v Ivory Coast | neutral | 1.41–0.78 | 51/28/20 | 62/22/16 | 10pp | 1-0 |
| Jun 20 | Ecuador v Curaçao | neutral | 2.18–0.51 | 76/17/7 | 87/9/4 | 12pp | 2-0 |
| Jun 20 | Netherlands v Sweden | neutral | 1.49–0.74 | 55/27/18 | 57/24/19 | 3pp | 1-0 |
| Jun 20 | Tunisia v Japan | neutral | 0.58–1.90 | 10/21/69 | 14/24/63 | 6pp | 0-1 |
| Jun 21 | Belgium v Iran | neutral | 1.16–0.95 | 40/31/29 | 67/20/12 | 28pp | 1-1 |
| Jun 21 | New Zealand v Egypt | neutral | 0.91–1.21 | 27/31/42 | 17/24/59 | 17pp | 0-1 |
| Jun 21 | Spain v Saudi Arabia | neutral | 2.66–0.41 | 85/12/4 | 87/10/4 | 2pp | 2-0 |
| Jun 21 | Uruguay v Cape Verde | neutral | 1.79–0.62 | 65/23/12 | 64/23/13 | 2pp | 1-0 |

## Where we disagree with the market

The model is independent of the odds, so these gaps are where our Elo-Poisson view parts from the bookmaker — and they cluster on the model's known soft spots (host-advantage calibration; less boldness on big favourites).

| Match | Our H/D/A | Market H/D/A | Edge | Lean |
|---|---|---|---|---|
| Ghana v Panama | 14/25/61 | 43/29/28 | 33pp | model lower on Ghana |
| Belgium v Iran | 40/31/29 | 67/20/12 | 28pp | model lower on Belgium |
| United States v Australia | 34/29/37 | 59/23/18 | 25pp | model lower on United States |
| Austria v Jordan | 46/30/24 | 70/19/11 | 24pp | model lower on Austria |
| Iraq v Norway | 14/25/62 | 7/14/79 | 17pp | model higher on Iraq |
| New Zealand v Egypt | 27/31/42 | 17/24/59 | 17pp | model higher on New Zealand |
| Brazil v Haiti | 74/19/8 | 87/9/4 | 13pp | model lower on Brazil |
| Ecuador v Curaçao | 76/17/7 | 87/9/4 | 12pp | model lower on Ecuador |
| Germany v Ivory Coast | 51/28/20 | 62/22/16 | 10pp | model lower on Germany |

## Match-by-match

### Tuesday, June 16

**Argentina vs Algeria** — _neutral venue_  
Elo Argentina 2193 · Algeria 1885  |  expected goals **1.90 – 0.58**  
- **1X2:** Argentina 69% · Draw 21% · Algeria 10%   _(market 66/21/13)_
- **Goals:** Over 2.5 45% · BTTS 38%
- **Likeliest scores:** 1-0 15% · 2-0 15% · 1-1 10% · 3-0 10% · 0-0 9%
- Argentina favoured (69%); in line with the market.

**Austria vs Jordan** — _neutral venue_  
Elo Austria 1888 · Jordan 1778  |  expected goals **1.30 – 0.85**  
- **1X2:** Austria 46% · Draw 30% · Jordan 24%   _(market 70/19/11)_
- **Goals:** Over 2.5 36% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 10% · 0-1 9%
- Austria favoured (46%); **model lower than the market on Austria** (Δ24pp).

**France vs Senegal** — _neutral venue_  
Elo France 2132 · Senegal 1913  |  expected goals **1.60 – 0.69**  
- **1X2:** France 59% · Draw 26% · Senegal 15%   _(market 65/21/13)_
- **Goals:** Over 2.5 40% · BTTS 40%
- **Likeliest scores:** 1-0 16% · 2-0 13% · 1-1 12% · 0-0 11% · 2-1 9%
- France favoured (59%); in line with the market.

**Iraq vs Norway** — _neutral venue_  
Elo Iraq 1740 · Norway 1987  |  expected goals **0.65 – 1.68**  
- **1X2:** Iraq 14% · Draw 25% · Norway 62%   _(market 7/14/79)_
- **Goals:** Over 2.5 41% · BTTS 40%
- **Likeliest scores:** 0-1 16% · 0-2 14% · 1-1 11% · 0-0 10% · 1-2 9%
- Norway favoured (62%); **model higher than the market on Iraq** (Δ17pp).

### Wednesday, June 17

**England vs Croatia** — _neutral venue_  
Elo England 2098 · Croatia 1977  |  expected goals **1.32 – 0.83**  
- **1X2:** England 48% · Draw 30% · Croatia 23%   _(market 55/26/19)_
- **Goals:** Over 2.5 37% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 10% · 0-1 9%
- England favoured (48%); in line with the market.

**Ghana vs Panama** — _neutral venue_  
Elo Ghana 1626 · Panama 1864  |  expected goals **0.66 – 1.66**  
- **1X2:** Ghana 14% · Draw 25% · Panama 61%   _(market 43/29/28)_
- **Goals:** Over 2.5 41% · BTTS 40%
- **Likeliest scores:** 0-1 16% · 0-2 13% · 1-1 11% · 0-0 10% · 1-2 9%
- Panama favoured (61%); **model lower than the market on Ghana** (Δ33pp).

**Portugal vs DR Congo** — _neutral venue_  
Elo Portugal 2063 · DR Congo 1763  |  expected goals **1.87 – 0.59**  
- **1X2:** Portugal 68% · Draw 22% · DR Congo 11%   _(market 75/17/9)_
- **Goals:** Over 2.5 44% · BTTS 38%
- **Likeliest scores:** 1-0 16% · 2-0 15% · 1-1 10% · 3-0 9% · 0-0 9%
- Portugal favoured (68%); in line with the market.

**Uzbekistan vs Colombia** — _neutral venue_  
Elo Uzbekistan 1822 · Colombia 2068  |  expected goals **0.65 – 1.68**  
- **1X2:** Uzbekistan 14% · Draw 25% · Colombia 62%   _(market 11/20/69)_
- **Goals:** Over 2.5 41% · BTTS 40%
- **Likeliest scores:** 0-1 16% · 0-2 14% · 1-1 11% · 0-0 10% · 1-2 9%
- Colombia favoured (62%); in line with the market.

### Thursday, June 18

**Canada vs Qatar** — _Canada at home_  
Elo Canada 1884 · Qatar 1592  |  expected goals **2.37 – 0.60**  
- **1X2:** Canada 77% · Draw 16% · Qatar 7%   _(market 75/17/8)_
- **Goals:** Over 2.5 57% · BTTS 41%
- **Likeliest scores:** 2-0 14% · 1-0 12% · 3-0 11% · 2-1 9% · 1-1 8%
- Canada favoured (77%); in line with the market.

**Czech Republic vs South Africa** — _neutral venue_  
Elo Czech Republic 1786 · South Africa 1656  |  expected goals **1.35 – 0.82**  
- **1X2:** Czech Republic 49% · Draw 29% · South Africa 22%   _(market 54/25/20)_
- **Goals:** Over 2.5 37% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 10% · 0-1 9%
- Czech Republic favoured (49%); in line with the market.

**Mexico vs South Korea** — _Mexico at home_  
Elo Mexico 1997 · South Korea 1907  |  expected goals **1.61 – 0.88**  
- **1X2:** Mexico 54% · Draw 26% · South Korea 20%   _(market 47/29/24)_
- **Goals:** Over 2.5 45% · BTTS 47%
- **Likeliest scores:** 1-0 13% · 1-1 12% · 2-0 11% · 2-1 9% · 0-0 9%
- Mexico favoured (54%); in line with the market.

**Switzerland vs Bosnia and Herzegovina** — _neutral venue_  
Elo Switzerland 1931 · Bosnia and Herzegovina 1679  |  expected goals **1.70 – 0.65**  
- **1X2:** Switzerland 62% · Draw 24% · Bosnia and Herzegovina 13%   _(market 61/24/15)_
- **Goals:** Over 2.5 42% · BTTS 39%
- **Likeliest scores:** 1-0 16% · 2-0 14% · 1-1 11% · 0-0 10% · 2-1 9%
- Switzerland favoured (62%); in line with the market.

### Friday, June 19

**Brazil vs Haiti** — _neutral venue_  
Elo Brazil 2065 · Haiti 1704  |  expected goals **2.10 – 0.52**  
- **1X2:** Brazil 74% · Draw 19% · Haiti 8%   _(market 87/9/4)_
- **Goals:** Over 2.5 49% · BTTS 36%
- **Likeliest scores:** 2-0 16% · 1-0 15% · 3-0 11% · 2-1 8% · 1-1 8%
- Brazil favoured (74%); **model lower than the market on Brazil** (Δ13pp).

**Scotland vs Morocco** — _neutral venue_  
Elo Scotland 1874 · Morocco 1993  |  expected goals **0.84 – 1.32**  
- **1X2:** Scotland 23% · Draw 30% · Morocco 47%   _(market 18/26/55)_
- **Goals:** Over 2.5 36% · BTTS 42%
- **Likeliest scores:** 0-1 15% · 1-1 13% · 0-0 12% · 0-2 10% · 1-0 9%
- Morocco favoured (47%); in line with the market.

**Turkey vs Paraguay** — _neutral venue_  
Elo Turkey 1923 · Paraguay 1871  |  expected goals **1.16 – 0.95**  
- **1X2:** Turkey 40% · Draw 31% · Paraguay 29%   _(market 47/28/24)_
- **Goals:** Over 2.5 35% · BTTS 43%
- **Likeliest scores:** 1-1 14% · 1-0 13% · 0-0 13% · 0-1 11% · 2-0 8%
- Turkey favoured (40%); in line with the market.

**United States vs Australia** — _United States at home_  
Elo United States 1883 · Australia 1959  |  expected goals **1.17 – 1.21**  
- **1X2:** United States 34% · Draw 29% · Australia 37%   _(market 59/23/18)_
- **Goals:** Over 2.5 43% · BTTS 49%
- **Likeliest scores:** 1-1 14% · 0-1 11% · 1-0 10% · 0-0 10% · 1-2 8%
- Australia favoured (37%); **model lower than the market on United States** (Δ25pp).

### Saturday, June 20

**Ecuador vs Curaçao** — _neutral venue_  
Elo Ecuador 1985 · Curaçao 1605  |  expected goals **2.18 – 0.51**  
- **1X2:** Ecuador 76% · Draw 17% · Curaçao 7%   _(market 87/9/4)_
- **Goals:** Over 2.5 50% · BTTS 36%
- **Likeliest scores:** 2-0 16% · 1-0 15% · 3-0 12% · 2-1 8% · 1-1 8%
- Ecuador favoured (76%); **model lower than the market on Ecuador** (Δ12pp).

**Germany vs Ivory Coast** — _neutral venue_  
Elo Germany 2016 · Ivory Coast 1861  |  expected goals **1.41 – 0.78**  
- **1X2:** Germany 51% · Draw 28% · Ivory Coast 20%   _(market 62/22/16)_
- **Goals:** Over 2.5 37% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 11% · 2-1 9%
- Germany favoured (51%); **model lower than the market on Germany** (Δ10pp).

**Netherlands vs Sweden** — _neutral venue_  
Elo Netherlands 2011 · Sweden 1828  |  expected goals **1.49 – 0.74**  
- **1X2:** Netherlands 55% · Draw 27% · Sweden 18%   _(market 57/24/19)_
- **Goals:** Over 2.5 38% · BTTS 41%
- **Likeliest scores:** 1-0 15% · 1-1 12% · 2-0 12% · 0-0 11% · 2-1 9%
- Netherlands favoured (55%); in line with the market.

**Tunisia vs Japan** — _neutral venue_  
Elo Tunisia 1688 · Japan 1998  |  expected goals **0.58 – 1.90**  
- **1X2:** Tunisia 10% · Draw 21% · Japan 69%   _(market 14/24/63)_
- **Goals:** Over 2.5 45% · BTTS 38%
- **Likeliest scores:** 0-1 15% · 0-2 15% · 1-1 10% · 0-3 10% · 0-0 9%
- Japan favoured (69%); in line with the market.

### Sunday, June 21

**Belgium vs Iran** — _neutral venue_  
Elo Belgium 1936 · Iran 1885  |  expected goals **1.16 – 0.95**  
- **1X2:** Belgium 40% · Draw 31% · Iran 29%   _(market 67/20/12)_
- **Goals:** Over 2.5 35% · BTTS 43%
- **Likeliest scores:** 1-1 14% · 1-0 13% · 0-0 13% · 0-1 11% · 2-0 8%
- Belgium favoured (40%); **model lower than the market on Belgium** (Δ28pp).

**New Zealand vs Egypt** — _neutral venue_  
Elo New Zealand 1749 · Egypt 1821  |  expected goals **0.91 – 1.21**  
- **1X2:** New Zealand 27% · Draw 31% · Egypt 42%   _(market 17/24/59)_
- **Goals:** Over 2.5 36% · BTTS 43%
- **Likeliest scores:** 0-1 14% · 1-1 14% · 0-0 13% · 1-0 10% · 0-2 9%
- Egypt favoured (42%); **model higher than the market on New Zealand** (Δ17pp).

**Spain vs Saudi Arabia** — _neutral venue_  
Elo Spain 2201 · Saudi Arabia 1717  |  expected goals **2.66 – 0.41**  
- **1X2:** Spain 85% · Draw 12% · Saudi Arabia 4%   _(market 87/10/4)_
- **Goals:** Over 2.5 59% · BTTS 32%
- **Likeliest scores:** 2-0 16% · 3-0 14% · 1-0 12% · 4-0 10% · 2-1 7%
- Spain favoured (85%); in line with the market.

**Uruguay vs Cape Verde** — _neutral venue_  
Elo Uruguay 1959 · Cape Verde 1681  |  expected goals **1.79 – 0.62**  
- **1X2:** Uruguay 65% · Draw 23% · Cape Verde 12%   _(market 64/23/13)_
- **Goals:** Over 2.5 43% · BTTS 39%
- **Likeliest scores:** 1-0 16% · 2-0 14% · 1-1 10% · 0-0 10% · 2-1 9%
- Uruguay favoured (65%); in line with the market.

---
## How to read this & caveats

- **1X2 is the trustworthy output.** Goal totals run a touch low — the model under-predicts blowouts (a known, documented bias whose fix didn't generalize across backtests), so treat Over/Under as soft.

- **Group stage only.** Knockouts (extra time / penalties) are out of scope.

- **Market is a benchmark, not an input.** Where we disagree, the market is usually the sharper number; the gaps are flagged so you can judge for yourself.

- _Generated 2026-06-16 · Elo current to 2026-06-15 · model frozen 2022-11-19._