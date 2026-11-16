# Data Brief
Pipeline step: 1 of 6 — ambursaData
Date: 16 November 2026
Dataset: Exeter AI Usage Dataset v1 (`data/exeter_ai_indicators.csv`, `data/exeter_ai_initiatives.csv`, `data/exeter_ai.db`)
Analyst: ambursaData

---

## In Plain English
This dataset collects every credible published number we could find on how people in and around Exeter use artificial intelligence: what tools they use, what they use them for, why some people avoid it, and what they worry about. Nobody has yet run a survey of all Exeter residents about AI, so the dataset combines three things: real Exeter data (mostly University of Exeter students), regional data for South West businesses, and national UK benchmarks that show what "typical" looks like. A second table lists eight named organisations in Exeter that are using AI in practice, such as the Royal Devon hospital and the Met Office.

## Business Context
Question we are answering : How are people in Exeter using AI, and where does Exeter differ from the UK picture?
Decision this will inform : Where AI-skills support, guidance or services in Exeter would have the most effect (for example: University guidance, council digital-inclusion work, local business support, AmbursaTech content or training)
Audience                  : Mixed: local organisations (University, Guild, councils, business groups) and a general/LinkedIn audience. Assumed; please confirm.

## Dataset Structure
Source          : Secondary data compiled from 12 published sources (ONS, DSIT, Exeter Students' Guild, HEPI, Lloyds, OpenAI, University of Exeter, Met Office), plus a register of 8 local AI initiatives
Rows            : 167 indicator rows + 8 initiative rows
Columns         : 19 (indicators) / 6 (initiatives)
Time period     : Census 2021 context; AI indicators March 2025 to August 2026 (most from Nov 2025 to Jun 2026)
Each row is     : One published statistic for one population, place and segment (for example, "% of UoE students who have used ChatGPT = 84")
Key identifiers : `source_id`, `population`, `geography`, `segment_type`, `segment`, `metric`, `period`
Key metrics     : `value` (166 percentages, 1 count), with `quality_grade` (A–D) describing how reliable each source is

Coverage by place: Exeter 65 rows (53 student rows, 12 demographic context) · South West 15 · England 9 · UK 75 · London/North East 3.

## Data Quality Assessment
Overall quality : AMBER

| Column | Type | Missing % | Issues Found |
|--------|------|-----------|--------------|
| value | number | 0% | All percentages fall between 2 and 97; no impossible values. Some sources say "around" or "about" (ONS BICS, Met Office), and these are flagged in `notes`. |
| geography | text | 0% | Exeter rows cover students and demographics only. **There is no Exeter-wide resident AI survey.** |
| population | text | 0% | 14 different populations (students, adults, users, non-users, businesses). **Never compare rows from different populations directly.** |
| sample_n | number | 54% | The Guild Feb 2026 report doesn't publish its respondent n (panel ~1,000). ONS and Lloyds n aren't in the press pages. |
| period | text | 0% | Mixed granularity (year, month, financial year). Usable for ordering but not for precise trends. |
| quality_grade | text | 0% | A = official statistics (77 rows), B = robust named survey (27), C = self-selecting local panel (55), D = press-reported or vendor-commissioned (8). |
| notes | text | 40% | Blank where there's no caveat. This is intentional. |

Quality notes (the final story must acknowledge these):
1. **No representative AI survey of Exeter residents exists.** Exeter findings describe University of Exeter students, not the whole city.
2. **The Guild report is a volunteer panel** (grade C) with no published respondent count. Treat it as indicative.
3. **The South West figure from DSIT (table E6) wasn't retrievable** because the ODS file is blocked from this workspace. Only the London (69%) and North East (51%) values are included. DSIT's age bands for 45–74 (table E5) are also missing.
4. **Business adoption figures don't agree with each other** (SW 66% Lloyds vs UK 35% ONS) because they use different definitions and samples. Don't put them on the same axis.
5. **Report inconsistency:** the Guild report prints "clearer faculty guidelines" as both 19% and 9%. We store 19% and note the discrepancy.
6. One Exeter-led figure (Stoeckel, degree vs non-degree private use) was excluded because the published direction is ambiguous.

## Column Intelligence
Dimensions (how we slice) : geography, geo_level, population, theme (14), segment_type (age band, tool, purpose, reason, faculty, occupation, sex, qualification), period, quality_grade
Metrics (what we measure) : `value` read together with `metric` (e.g. pct_ever_used_tool, pct_used_for_purpose, pct_reason_non_use, pct_used_genai_last_3m, pct_businesses_using_ai)
Most interesting combos   :
  1. **Purpose by population:** Exeter students vs UK undergraduates (HEPI) vs UK adult users (DSIT). Is Exeter using AI differently?
  2. **Barriers by population:** why Exeter students avoid AI (environmental impact 58%) vs why UK non-users avoid it (prefer not to 44%, privacy 33%)
  3. **Age structure × national age-use gradient:** Exeter's unusually young population against DSIT/Stoeckel usage by age, to estimate Exeter-wide adoption

## First Impressions (Pattern Spotting)
1. **Exeter is structurally primed for heavy AI use.** 40% of Exeter's adults (16+) are aged 16–34, against 30% in England and 27% in the South West. 16% of residents are full-time students (England 5.6%). Age is the strongest predictor of AI use nationally: non-use runs from 37% for 18–29s to 89% for 65+. So Exeter's real adoption rate is very likely above the UK's 59%. That is a hypothesis to test, not yet a finding.
2. **Exeter students mainly use AI to learn, not to write for them.** 71% have used it to understand a concept, compared with 61% of UK undergraduates using it to explain concepts for assessed work. The questions are worded differently, so this is directional only. ChatGPT dominates (84%), with Gemini (39%) and Copilot (35%) far behind. A notable minority also use it for personal issues (18%) and medical symptoms (18%).
3. **Trust is low and anxiety is high.** 79% of Exeter students have noticed AI giving them false information, and 37% worry often about being wrongly flagged for AI use. Among those who avoid AI, the top reason is environmental impact (58%), which is quite different from UK non-users, whose main reasons are preference and privacy.

## What This Data Can Answer
Can answer     :
- How University of Exeter students use AI (tools, academic and personal purposes, worries, support wanted)
- How Exeter students compare with UK undergraduates and UK adults on the same themes
- How AI is being adopted by South West businesses and by named Exeter institutions (health, weather science, councils, university)
- How Exeter's demographic profile should shift its AI adoption relative to the UK (as a modelled estimate)

Cannot answer  :
- The actual share of all Exeter residents using AI (no local resident survey; the DSIT South West row is still missing)
- AI use among Exeter's older, non-student, or digitally excluded residents
- Change over time within Exeter (only one wave of Guild data on usage)

## Recommended Next Step
Write SQL that puts Exeter students, UK undergraduates and UK adults side by side on purpose, barriers and trust, and build a bounded age-weighted estimate of Exeter-wide AI use. Before that, add the DSIT South West row (table E6) if you can download the ODS file, because it's the single most valuable missing number.

---

## Pipeline Status
Step 1 ✅ data-explorer  → data_brief.md
Step 2 ⬜ sql-architect  → query_library.md
Step 3 ⬜ insight-hunter → findings.md
Step 4 ⬜ viz-builder    → dashboard_spec.md
Step 5 ⬜ story-weaver   → data_story.md
Step 6 ⬜ action-planner → action_plan.md
