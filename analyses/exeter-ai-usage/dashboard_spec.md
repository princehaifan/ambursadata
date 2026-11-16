# Dashboard Specification
Pipeline step: 4 of 6 — ambursaData
Date: 16 November 2026
Audience: Mixed: local organisations (University, Guild, councils, business groups) and a general/LinkedIn audience
Format: Live HTML dashboard ("How Exeter uses AI", https://claude.ai/artifact/PHntnSmJrxTKoJM1c8yeGN). Source page also saved as `dashboard/index.html`

---

## Chart List
| # | Chart type | Finding it shows | Title (the argument) | Data source |
|---|------------|------------------|----------------------|------|
| 1 | Grouped horizontal bar (3 places × 3 age groups) | F1: young population | "Two in five Exeter adults are aged 16–34, against three in ten in England" | `age_structure.csv` (Q6) |
| 2 | Horizontal bar, UK value in muted grey | F1: Exeter estimate | "Every estimation method puts Exeter above the UK's measured rate" | `adoption_estimate.csv` (Q7 + cross-check) |
| 3 | Grouped horizontal bar (3 populations × 5 purposes; "not asked" shown) | F2: tutor, not ghostwriter | "Exeter students use AI to understand concepts more often than UK undergraduates do" | `purposes.csv` (Q3) |
| 4 | Horizontal bar | F2: tool reach | "ChatGPT reaches more than twice as many Exeter students as any other tool" | `student_tools.csv` (Q2) |
| 5 | Horizontal bar | F2: trust gap | "Four in five have caught AI getting things wrong, and only half got helpful guidance even in the best faculty" | `student_trust_support.csv` (Q5/Q10) |
| 6 | Horizontal bar | F2: support demand | "Students want training, not bans" | `student_trust_support.csv` (Q10) |
| 7 | Horizontal bar | F3: Exeter barriers | "Exeter students who avoid AI mostly cite its environmental impact" | `barriers.csv` (Q4) |
| 8 | Horizontal bar | F3: UK barriers | "UK adults who don't use AI mostly say they'd rather not, or worry about privacy" | `barriers.csv` (Q4) |
| 9 | Table | Supporting: local deployments | "AI already at work in Exeter organisations" | `initiatives.csv` (Q11) |
| 10 | Table (deliberately not a chart) | Anomaly: business definitions | "Business adoption: fast in the South West, but the sources don't agree" | `business_adoption.csv` (Q8) |

Business figures are shown as a table, not a chart. Plotting Lloyds (66%) beside ONS (35%) on one axis would suggest they measure the same thing.

## KPI Cards (for executive dashboard)
| Label | Value | Comparison | Direction |
|-------|-------|------------|-----------|
| Exeter adults who have used generative AI (estimate) | 63–67% | vs 59% UK measured (DSIT 2025/26) | ▲ above the UK (modelled) |
| UoE students who have used ChatGPT | 84% | Gemini 39% · Copilot 35% | n/a (single wave) |
| UoE students who have seen AI give false information | 79% | 37% worry often about being wrongly flagged | n/a (single wave) |
| UoE students who want AI workshops or training | 55% | only 10% want AI banned | n/a (single wave) |

There are no period-on-period arrows. These are single-wave figures, so there's no earlier period to compare against, and inventing a change would mislead. Each card shows its comparison figure instead.

## Dashboard Layout
- **Top:** title, a one-sentence takeaway built from the live figures, and 4 headline cards. The main finding is visible without scrolling.
- **Middle:** three sections, one per finding, each headed with what it shows. Two charts sit side by side and stack on narrow screens.
- **Bottom:** the organisations register, the business table with a caveat, and a closed "Method, sources and caveats" panel.
- **Behaviour:** every bar prints its value and has a hover tooltip. All charts resize to the window (including a ~400px side panel). Theme colours follow light or dark mode. Every number on the page is linked to its source file, which readers can see and download as CSV from the dashboard's Sources panel.

## Files Produced
[ ] Python charts (.png files)
[x] HTML dashboard: live dashboard (above), with source `dashboard/index.html` and 9 data files in `dashboard/`
[ ] Both

## Non-Technical Test Result
PENDING: needs a person who hasn't seen the data. Built to pass: every title states its finding in plain words, values are printed on the bars, and caveats sit beside the charts they affect. The page's automatic check passed, with no code errors and every displayed number matching its source data.

---

## Pipeline Status
Step 1 ✅ data-explorer  → data_brief.md
Step 2 ✅ sql-architect  → query_library.md
Step 3 ✅ insight-hunter → findings.md
Step 4 ✅ viz-builder    → dashboard_spec.md
Step 5 ⬜ story-weaver   → data_story.md
Step 6 ⬜ action-planner → action_plan.md
