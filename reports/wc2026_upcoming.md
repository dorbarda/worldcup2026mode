# World Cup 2026 — Opening Matches (Jun 13–Jun 18)

Model-based forecasts for the next round of group matches (22 fixtures), generated from **current Elo** (all played matches through 2026-06-12). The Dixon-Coles Poisson model is the one validated on the 2018 & 2022 backtests; its coefficients are frozen at the 2022-11-19 fit, only the ratings are current.

De-vigged bookmaker odds are shown for comparison only — they do **not** feed the model. `Edge` = largest gap between our probability and the market on any outcome.

## Results so far

How the pre-match forecasts have fared, model vs de-vigged market (this is the B2 baseline, scored live going forward):

| Match | Result | Our call (H/D/A) | Market (H/D/A) | Winner |
|---|---|---|---|---|
| Mexico v South Africa | 2-0 (home) | 80/14/6 | 69/21/10 | model |
| South Korea v Czech Republic | 2-1 (home) | 42/31/27 | 37/30/33 | model |
| Canada v Bosnia and Herzegovina | 1-1 (draw) | 72/18/9 | 53/26/21 | market |
| United States v Paraguay | 4-1 (home) | 33/29/38 | 49/28/23 | market |

**Running RPS over 4 match(es): model 0.1973 vs market 0.1573 — market ahead.** (Tiny sample — a smoke signal, not a verdict.)

![overview](figures/wc2026/overview.png)

## All fixtures

| Date | Match | Venue | xG (H–A) | Our H/D/A | Market H/D/A | Edge | Top score |
|---|---|---|---|---|---|---|---|
| Jun 13 | Qatar v Switzerland | neutral | 0.50–2.20 | 7/17/76 | 7/14/80 | 3pp | 0-2 |
| Jun 13 | Brazil v Morocco | neutral | 1.24–0.89 | 44/30/26 | 57/26/17 | 13pp | 1-0 |
| Jun 13 | Haiti v Scotland | neutral | 0.81–1.35 | 22/29/49 | 17/22/62 | 13pp | 0-1 |
| Jun 13 | Australia v Turkey | neutral | 0.91–1.21 | 27/31/42 | 18/25/56 | 14pp | 0-1 |
| Jun 14 | Germany v Curaçao | neutral | 2.20–0.50 | 76/17/7 | 92/6/2 | 16pp | 2-0 |
| Jun 14 | Ivory Coast v Ecuador | neutral | 0.69–1.59 | 15/26/59 | 26/34/40 | 19pp | 0-1 |
| Jun 14 | Netherlands v Japan | neutral | 1.08–1.02 | 36/31/33 | 48/27/25 | 12pp | 1-1 |
| Jun 14 | Sweden v Tunisia | neutral | 1.13–0.97 | 39/31/30 | 50/28/22 | 12pp | 1-1 |
| Jun 15 | Belgium v Egypt | neutral | 1.37–0.81 | 49/29/21 | 59/24/17 | 10pp | 1-0 |
| Jun 15 | Iran v New Zealand | neutral | 1.43–0.77 | 52/28/20 | 52/28/20 | 1pp | 1-0 |
| Jun 15 | Spain v Cape Verde | neutral | 3.16–0.35 | 91/8/2 | 88/8/4 | 2pp | 3-0 |
| Jun 15 | Saudi Arabia v Uruguay | neutral | 0.61–1.80 | 11/23/66 | 12/22/67 | 1pp | 0-1 |
| Jun 16 | France v Senegal | neutral | 1.60–0.69 | 59/26/15 | 65/22/13 | 6pp | 1-0 |
| Jun 16 | Iraq v Norway | neutral | 0.65–1.68 | 14/25/62 | 7/14/80 | 18pp | 0-1 |
| Jun 16 | Argentina v Algeria | neutral | 1.90–0.58 | 69/21/10 | 68/21/11 | 1pp | 1-0 |
| Jun 16 | Austria v Jordan | neutral | 1.30–0.85 | 46/30/24 | 72/17/11 | 26pp | 1-0 |
| Jun 17 | Portugal v DR Congo | neutral | 1.87–0.59 | 68/22/11 | 74/17/9 | 7pp | 1-0 |
| Jun 17 | Uzbekistan v Colombia | neutral | 0.65–1.68 | 14/25/62 | 11/20/69 | 7pp | 0-1 |
| Jun 17 | England v Croatia | neutral | 1.32–0.83 | 48/30/23 | 56/25/19 | 8pp | 1-0 |
| Jun 17 | Ghana v Panama | neutral | 0.66–1.66 | 14/25/61 | 44/28/28 | 33pp | 0-1 |
| Jun 18 | Czech Republic v South Africa | neutral | 1.35–0.82 | 49/29/22 | 55/25/20 | 6pp | 1-0 |
| Jun 18 | Mexico v South Korea | Mexico (H) | 1.61–0.88 | 54/26/20 | 47/29/24 | 6pp | 1-0 |

## Where we disagree with the market

The model is independent of the odds, so these gaps are where our Elo-Poisson view parts from the bookmaker — and they cluster on the model's known soft spots (host-advantage calibration; less boldness on big favourites).

| Match | Our H/D/A | Market H/D/A | Edge | Lean |
|---|---|---|---|---|
| Ghana v Panama | 14/25/61 | 44/28/28 | 33pp | model lower on Ghana |
| Austria v Jordan | 46/30/24 | 72/17/11 | 26pp | model lower on Austria |
| Ivory Coast v Ecuador | 15/26/59 | 26/34/40 | 19pp | model lower on Ivory Coast |
| Iraq v Norway | 14/25/62 | 7/14/80 | 18pp | model higher on Iraq |
| Germany v Curaçao | 76/17/7 | 92/6/2 | 16pp | model lower on Germany |
| Australia v Turkey | 27/31/42 | 18/25/56 | 14pp | model higher on Australia |
| Brazil v Morocco | 44/30/26 | 57/26/17 | 13pp | model lower on Brazil |
| Haiti v Scotland | 22/29/49 | 17/22/62 | 13pp | model higher on Haiti |
| Netherlands v Japan | 36/31/33 | 48/27/25 | 12pp | model lower on Netherlands |
| Sweden v Tunisia | 39/31/30 | 50/28/22 | 12pp | model lower on Sweden |

## Match-by-match

### Saturday, June 13

**Australia vs Turkey** — _neutral venue_  
Elo Australia 1905 · Turkey 1978  |  expected goals **0.91 – 1.21**  
- **1X2:** Australia 27% · Draw 31% · Turkey 42%   _(market 18/25/56)_
- **Goals:** Over 2.5 36% · BTTS 43%
- **Likeliest scores:** 0-1 14% · 1-1 14% · 0-0 13% · 1-0 10% · 0-2 9%
- Turkey favoured (42%); **model higher than the market on Australia** (Δ14pp).

**Brazil vs Morocco** — _neutral venue_  
Elo Brazil 2072 · Morocco 1985  |  expected goals **1.24 – 0.89**  
- **1X2:** Brazil 44% · Draw 30% · Morocco 26%   _(market 57/26/17)_
- **Goals:** Over 2.5 36% · BTTS 42%
- **Likeliest scores:** 1-0 14% · 1-1 14% · 0-0 13% · 0-1 10% · 2-0 9%
- Brazil favoured (44%); **model lower than the market on Brazil** (Δ13pp).

**Haiti vs Scotland** — _neutral venue_  
Elo Haiti 1723 · Scotland 1855  |  expected goals **0.81 – 1.35**  
- **1X2:** Haiti 22% · Draw 29% · Scotland 49%   _(market 17/22/62)_
- **Goals:** Over 2.5 37% · BTTS 42%
- **Likeliest scores:** 0-1 15% · 1-1 13% · 0-0 12% · 0-2 10% · 1-0 9%
- Scotland favoured (49%); **model higher than the market on Haiti** (Δ13pp).

**Qatar vs Switzerland** — _neutral venue_  
Elo Qatar 1568 · Switzerland 1955  |  expected goals **0.50 – 2.20**  
- **1X2:** Qatar 7% · Draw 17% · Switzerland 76%   _(market 7/14/80)_
- **Goals:** Over 2.5 51% · BTTS 35%
- **Likeliest scores:** 0-2 16% · 0-1 14% · 0-3 12% · 1-2 8% · 1-1 8%
- Switzerland favoured (76%); in line with the market.

### Sunday, June 14

**Germany vs Curaçao** — _neutral venue_  
Elo Germany 2003 · Curaçao 1617  |  expected goals **2.20 – 0.50**  
- **1X2:** Germany 76% · Draw 17% · Curaçao 7%   _(market 92/6/2)_
- **Goals:** Over 2.5 51% · BTTS 35%
- **Likeliest scores:** 2-0 16% · 1-0 14% · 3-0 12% · 2-1 8% · 1-1 8%
- Germany favoured (76%); **model lower than the market on Germany** (Δ16pp).

**Ivory Coast vs Ecuador** — _neutral venue_  
Elo Ivory Coast 1815 · Ecuador 2032  |  expected goals **0.69 – 1.59**  
- **1X2:** Ivory Coast 15% · Draw 26% · Ecuador 59%   _(market 26/34/40)_
- **Goals:** Over 2.5 40% · BTTS 40%
- **Likeliest scores:** 0-1 16% · 0-2 13% · 1-1 12% · 0-0 11% · 1-2 9%
- Ecuador favoured (59%); **model lower than the market on Ivory Coast** (Δ19pp).

**Netherlands vs Japan** — _neutral venue_  
Elo Netherlands 2012 · Japan 1996  |  expected goals **1.08 – 1.02**  
- **1X2:** Netherlands 36% · Draw 31% · Japan 33%   _(market 48/27/25)_
- **Goals:** Over 2.5 35% · BTTS 43%
- **Likeliest scores:** 1-1 14% · 0-0 13% · 1-0 13% · 0-1 12% · 2-1 7%
- Netherlands favoured (36%); **model lower than the market on Netherlands** (Δ12pp).

**Sweden vs Tunisia** — _neutral venue_  
Elo Sweden 1778 · Tunisia 1738  |  expected goals **1.13 – 0.97**  
- **1X2:** Sweden 39% · Draw 31% · Tunisia 30%   _(market 50/28/22)_
- **Goals:** Over 2.5 35% · BTTS 43%
- **Likeliest scores:** 1-1 14% · 1-0 13% · 0-0 13% · 0-1 11% · 2-0 8%
- Sweden favoured (39%); **model lower than the market on Sweden** (Δ12pp).

### Monday, June 15

**Belgium vs Egypt** — _neutral venue_  
Elo Belgium 1948 · Egypt 1810  |  expected goals **1.37 – 0.81**  
- **1X2:** Belgium 49% · Draw 29% · Egypt 21%   _(market 59/24/17)_
- **Goals:** Over 2.5 37% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 11% · 0-1 9%
- Belgium favoured (49%); in line with the market.

**Iran vs New Zealand** — _neutral venue_  
Elo Iran 1898 · New Zealand 1736  |  expected goals **1.43 – 0.77**  
- **1X2:** Iran 52% · Draw 28% · New Zealand 20%   _(market 52/28/20)_
- **Goals:** Over 2.5 38% · BTTS 41%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 11% · 2-1 9%
- Iran favoured (52%); in line with the market.

**Saudi Arabia vs Uruguay** — _neutral venue_  
Elo Saudi Arabia 1697 · Uruguay 1979  |  expected goals **0.61 – 1.80**  
- **1X2:** Saudi Arabia 11% · Draw 23% · Uruguay 66%   _(market 12/22/67)_
- **Goals:** Over 2.5 43% · BTTS 39%
- **Likeliest scores:** 0-1 16% · 0-2 15% · 1-1 10% · 0-0 9% · 1-2 9%
- Uruguay favoured (66%); in line with the market.

**Spain vs Cape Verde** — _neutral venue_  
Elo Spain 2229 · Cape Verde 1654  |  expected goals **3.16 – 0.35**  
- **1X2:** Spain 91% · Draw 8% · Cape Verde 2%   _(market 88/8/4)_
- **Goals:** Over 2.5 68% · BTTS 28%
- **Likeliest scores:** 3-0 16% · 2-0 15% · 4-0 12% · 1-0 9% · 5-0 8%
- Spain favoured (91%); in line with the market.

### Tuesday, June 16

**Argentina vs Algeria** — _neutral venue_  
Elo Argentina 2193 · Algeria 1885  |  expected goals **1.90 – 0.58**  
- **1X2:** Argentina 69% · Draw 21% · Algeria 10%   _(market 68/21/11)_
- **Goals:** Over 2.5 45% · BTTS 38%
- **Likeliest scores:** 1-0 15% · 2-0 15% · 1-1 10% · 3-0 10% · 0-0 9%
- Argentina favoured (69%); in line with the market.

**Austria vs Jordan** — _neutral venue_  
Elo Austria 1888 · Jordan 1778  |  expected goals **1.30 – 0.85**  
- **1X2:** Austria 46% · Draw 30% · Jordan 24%   _(market 72/17/11)_
- **Goals:** Over 2.5 36% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 10% · 0-1 9%
- Austria favoured (46%); **model lower than the market on Austria** (Δ26pp).

**France vs Senegal** — _neutral venue_  
Elo France 2132 · Senegal 1913  |  expected goals **1.60 – 0.69**  
- **1X2:** France 59% · Draw 26% · Senegal 15%   _(market 65/22/13)_
- **Goals:** Over 2.5 40% · BTTS 40%
- **Likeliest scores:** 1-0 16% · 2-0 13% · 1-1 12% · 0-0 11% · 2-1 9%
- France favoured (59%); in line with the market.

**Iraq vs Norway** — _neutral venue_  
Elo Iraq 1740 · Norway 1987  |  expected goals **0.65 – 1.68**  
- **1X2:** Iraq 14% · Draw 25% · Norway 62%   _(market 7/14/80)_
- **Goals:** Over 2.5 41% · BTTS 40%
- **Likeliest scores:** 0-1 16% · 0-2 14% · 1-1 11% · 0-0 10% · 1-2 9%
- Norway favoured (62%); **model higher than the market on Iraq** (Δ18pp).

### Wednesday, June 17

**England vs Croatia** — _neutral venue_  
Elo England 2098 · Croatia 1977  |  expected goals **1.32 – 0.83**  
- **1X2:** England 48% · Draw 30% · Croatia 23%   _(market 56/25/19)_
- **Goals:** Over 2.5 37% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 10% · 0-1 9%
- England favoured (48%); in line with the market.

**Ghana vs Panama** — _neutral venue_  
Elo Ghana 1626 · Panama 1864  |  expected goals **0.66 – 1.66**  
- **1X2:** Ghana 14% · Draw 25% · Panama 61%   _(market 44/28/28)_
- **Goals:** Over 2.5 41% · BTTS 40%
- **Likeliest scores:** 0-1 16% · 0-2 13% · 1-1 11% · 0-0 10% · 1-2 9%
- Panama favoured (61%); **model lower than the market on Ghana** (Δ33pp).

**Portugal vs DR Congo** — _neutral venue_  
Elo Portugal 2063 · DR Congo 1763  |  expected goals **1.87 – 0.59**  
- **1X2:** Portugal 68% · Draw 22% · DR Congo 11%   _(market 74/17/9)_
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

**Czech Republic vs South Africa** — _neutral venue_  
Elo Czech Republic 1786 · South Africa 1656  |  expected goals **1.35 – 0.82**  
- **1X2:** Czech Republic 49% · Draw 29% · South Africa 22%   _(market 55/25/20)_
- **Goals:** Over 2.5 37% · BTTS 42%
- **Likeliest scores:** 1-0 15% · 1-1 13% · 0-0 12% · 2-0 10% · 0-1 9%
- Czech Republic favoured (49%); in line with the market.

**Mexico vs South Korea** — _Mexico at home_  
Elo Mexico 1997 · South Korea 1907  |  expected goals **1.61 – 0.88**  
- **1X2:** Mexico 54% · Draw 26% · South Korea 20%   _(market 47/29/24)_
- **Goals:** Over 2.5 45% · BTTS 47%
- **Likeliest scores:** 1-0 13% · 1-1 12% · 2-0 11% · 2-1 9% · 0-0 9%
- Mexico favoured (54%); in line with the market.

---
## How to read this & caveats

- **1X2 is the trustworthy output.** Goal totals run a touch low — the model under-predicts blowouts (a known, documented bias whose fix didn't generalize across backtests), so treat Over/Under as soft.

- **Group stage only.** Knockouts (extra time / penalties) are out of scope.

- **Market is a benchmark, not an input.** Where we disagree, the market is usually the sharper number; the gaps are flagged so you can judge for yourself.

- _Generated 2026-06-13 · Elo current to 2026-06-12 · model frozen 2022-11-19._