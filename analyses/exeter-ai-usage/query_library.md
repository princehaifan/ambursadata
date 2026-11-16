# Query Library
Pipeline step: 2 of 6 — ambursaData
Date: 16 November 2026
Dataset: Exeter AI Usage Dataset v1 (tables `indicators`, `initiatives` in `data/exeter_ai.db`)
Dialect: SQLite 3 (portable to PostgreSQL/DuckDB; only `GROUP_CONCAT` → `STRING_AGG` needs changing)

---

## Query Index
| # | Query Name | Business Question Answered |
|---|------------|---------------------------|
| 1 | q01_source_coverage | How much of the evidence is truly about Exeter, and how reliable is each slice? |
| 2 | q02_exeter_tool_share | Which AI tools have University of Exeter students used? |
| 3 | q03_purpose_comparison | Do Exeter students use AI for the same things as UK undergraduates and UK adult users? |
| 4 | q04_barriers_comparison | Why do people who avoid AI avoid it: Exeter students or UK adults? |
| 5 | q05_trust_and_anxiety | How much do people trust AI output, and how anxious are they about it? |
| 6 | q06_age_structure | How young is Exeter's adult (16+) population compared with the South West and England? |
| 7 | q07_exeter_adoption_estimate | If Exeter adults used AI at national rates for their age, what share would have used generative AI? |
| 8 | q08_business_adoption | How fast are businesses adopting AI, regionally and nationally? |
| 9 | q09_personal_use | Beyond study, what personal uses do Exeter students make of AI, compared with UK adult users? |
| 10 | q10_support_demand | What help do Exeter students say they want, and where does guidance fall short? |
| 11 | q11_local_initiatives | Which Exeter organisations are deploying AI, and in which sectors? |

All 11 queries were executed against the database. The sample results below are real output, not illustrative.

---

## Query 1: q01_source_coverage

**Business Question:** How much of the evidence is truly about Exeter, and how reliable is each slice?

**Plain-English Explanation:**
This query counts indicator rows and distinct sources from the `indicators` table, grouped by geography level, place and quality grade. It shows one row per place and quality grade.

**Assumptions:** None. All 167 rows are included.
**Limitations:** Row counts measure how much evidence exists, not how important it is.

**SQL:**
```sql
-- @name: q01_source_coverage
-- How much of the evidence is truly about Exeter, and how reliable is each slice?
SELECT
    geo_level,
    geography,
    quality_grade,
    COUNT(*)                   AS n_rows,
    COUNT(DISTINCT source_id)  AS n_sources
FROM indicators
GROUP BY geo_level, geography, quality_grade
ORDER BY CASE geo_level WHEN 'City' THEN 1 WHEN 'Region' THEN 2 ELSE 3 END, n_rows DESC;
```

**Result (11 rows, first 8 shown):**

| geo_level   | geography   | quality_grade   |   n_rows |   n_sources |
|:------------|:------------|:----------------|---------:|------------:|
| City        | Exeter      | C               |       55 |           2 |
| City        | Exeter      | A               |       10 |           2 |
| Region      | South West  | A               |        9 |           1 |
| Region      | South West  | D               |        6 |           3 |
| Region      | London      | A               |        1 |           1 |
| Region      | London      | D               |        1 |           1 |
| Region      | North East  | A               |        1 |           1 |
| Country     | UK          | A               |       47 |           2 |

---

## Query 2: q02_exeter_tool_share

**Business Question:** Which AI tools have University of Exeter students used?

**Plain-English Explanation:**
This query takes the Guild Feb 2026 tool question, ranks the tools by the share of students who have used each, and expresses each as a fraction of ChatGPT's reach. It shows one row per tool.

**Assumptions:** Multi-select question, so shares don't add up to 100%.
**Limitations:** 'Ever used' says nothing about how often. The panel is self-selecting (grade C).

**SQL:**
```sql
-- @name: q02_exeter_tool_share
-- Which AI tools have University of Exeter students used?
SELECT
    segment                                   AS tool,
    value                                     AS pct_students_used,
    ROUND(value * 1.0 / MAX(value) OVER (), 2) AS share_of_chatgpt_reach
FROM indicators
WHERE source_id = 'GUILD_26'
  AND metric = 'pct_ever_used_tool'
ORDER BY value DESC;
```

**Result (6 rows):**

| tool              |   pct_students_used |   share_of_chatgpt_reach |
|:------------------|--------------------:|-------------------------:|
| ChatGPT           |                  84 |                     1    |
| Google Gemini     |                  39 |                     0.46 |
| Microsoft Copilot |                  35 |                     0.42 |
| Canva             |                  29 |                     0.35 |
| Character.ai      |                   4 |                     0.05 |
| DALL-E            |                   3 |                     0.04 |

---

## Query 3: q03_purpose_comparison

**Business Question:** Do Exeter students use AI for the same things as UK undergraduates and UK adult users?

**Plain-English Explanation:**
This query maps differently worded purpose questions from three surveys (Guild, HEPI, DSIT) onto five common purpose groups, places the populations side by side, and calculates the Exeter-minus-UK-undergraduate gap in percentage points. It shows one row per purpose group.

**Assumptions:** Where one survey has two items in a group (e.g. grammar and draft feedback), MAX takes the highest. HEPI items refer to assessed work.
**Limitations:** Question wording and bases differ, so gaps are directional, not statistically tested. Missing cells mean that survey didn't ask the question.

**SQL:**
```sql
-- @name: q03_purpose_comparison
-- Do Exeter students use AI for the same things as UK undergraduates and UK adult users?
WITH mapped AS (
    SELECT
        CASE
            WHEN segment IN ('Understanding a concept','Explaining concepts')            THEN 'Understand / explain concepts'
            WHEN segment IN ('Summarising readings','Summarising articles')              THEN 'Summarise reading'
            WHEN segment IN ('Research assistance','Research ideas')                     THEN 'Research help / ideas'
            WHEN segment IN ('Correcting grammar','Feedback on a draft',
                             'Writing/editing documents')                                THEN 'Writing & editing'
            WHEN segment IN ('Advice on a personal issue','Emotional or relationship issues') THEN 'Personal / emotional issues'
        END AS purpose_group,
        CASE source_id WHEN 'GUILD_26' THEN 'Exeter students'
                       WHEN 'HEPI_26'  THEN 'UK undergraduates'
                       WHEN 'DSIT_PES' THEN 'UK adult genAI users' END AS population_label,
        value
    FROM indicators
    WHERE metric = 'pct_used_for_purpose'
)
SELECT
    purpose_group,
    MAX(CASE WHEN population_label = 'Exeter students'      THEN value END) AS exeter_students,
    MAX(CASE WHEN population_label = 'UK undergraduates'    THEN value END) AS uk_undergrads,
    MAX(CASE WHEN population_label = 'UK adult genAI users' THEN value END) AS uk_adult_users,
    MAX(CASE WHEN population_label = 'Exeter students' THEN value END)
      - MAX(CASE WHEN population_label = 'UK undergraduates' THEN value END) AS gap_vs_uk_undergrads_pts
FROM mapped
WHERE purpose_group IS NOT NULL
GROUP BY purpose_group
ORDER BY exeter_students DESC;
```

**Result (5 rows):**

| purpose_group                 |   exeter_students | uk_undergrads   | uk_adult_users   | gap_vs_uk_undergrads_pts   |
|:------------------------------|------------------:|:----------------|:-----------------|:---------------------------|
| Understand / explain concepts |                71 | 61.0            | —                | 10.0                       |
| Writing & editing             |                46 | —               | 58.0             | —                          |
| Research help / ideas         |                45 | 40.0            | —                | 5.0                        |
| Summarise reading             |                43 | 49.0            | —                | -6.0                       |
| Personal / emotional issues   |                18 | —               | 10.0             | —                          |

---

## Query 4: q04_barriers_comparison

**Business Question:** Why do people who avoid AI avoid it: Exeter students or UK adults?

**Plain-English Explanation:**
This query pulls every 'reason for not using AI' row and ranks the reasons within each population. It shows one row per population and reason.

**Assumptions:** The bases are non-users only: Exeter students who choose not to use AI, and UK adult non-users in DSIT's online sample.
**Limitations:** The two surveys offered different answer lists, so a reason missing from one list doesn't mean nobody holds it.

**SQL:**
```sql
-- @name: q04_barriers_comparison
-- Why do people who avoid AI avoid it — Exeter students vs UK adults?
SELECT
    CASE source_id WHEN 'GUILD_26' THEN 'Exeter student non-users'
                   ELSE 'UK adult non-users' END AS population_label,
    segment AS reason,
    value   AS pct,
    RANK() OVER (PARTITION BY source_id ORDER BY value DESC) AS rank_within_population
FROM indicators
WHERE metric = 'pct_reason_non_use'
ORDER BY population_label, rank_within_population;
```

**Result (7 rows):**

| population_label         | reason                      |   pct |   rank_within_population |
|:-------------------------|:----------------------------|------:|-------------------------:|
| Exeter student non-users | Environmental impact        |    58 |                        1 |
| Exeter student non-users | Self-reliance               |    20 |                        2 |
| Exeter student non-users | Ethical concerns            |    11 |                        3 |
| UK adult non-users       | Prefer not to use AI        |    44 |                        1 |
| UK adult non-users       | Privacy or security worries |    33 |                        2 |
| UK adult non-users       | Don't know enough           |    32 |                        3 |
| UK adult non-users       | Worried about accuracy      |    31 |                        4 |

---

## Query 5: q05_trust_and_anxiety

**Business Question:** How much do people trust AI output, and how anxious are they about it?

**Plain-English Explanation:**
This query selects the headline trust, risk and anxiety measures for Exeter students (Guild 2025/26), UK adults (DSIT) and the Met Office forecast-trust study, keeping only the 'yes/concerned' side of each question. It shows one row per measure.

**Assumptions:** Negative or neutral response options are excluded to keep one headline value per question.
**Limitations:** The measures aren't the same question across populations. Read them as context, not as like-for-like comparisons.

**SQL:**
```sql
-- @name: q05_trust_and_anxiety
-- How much do people trust AI output, and how anxious are they about it?
SELECT population, geography, metric, segment, value AS pct, quality_grade
FROM indicators
WHERE theme IN ('trust','attitudes')
  AND (   (source_id = 'GUILD_26' AND metric IN ('pct_noticed_false_info','pct_worry_flagged_penalised','pct_ai_skills_important_to_education'))
       OR (source_id = 'GUILD_25' AND metric = 'pct_concerned_ai_data_privacy')
       OR (source_id = 'DSIT_PES' AND segment IN ('Information may be inaccurate','Privacy and security','Harm to creative/critical thinking'))
       OR (source_id = 'METOFFICE_TRUST'))
  AND segment NOT IN ('Rarely or never','Unsure','Do not think about it very often','Rarely or never think about it','Disagree')
ORDER BY geography, value DESC;
```

**Result (11 rows, first 8 shown):**

| population                    | geography   | metric                               | segment                         |   pct | quality_grade   |
|:------------------------------|:------------|:-------------------------------------|:--------------------------------|------:|:----------------|
| University of Exeter students | Exeter      | pct_noticed_false_info               | Have received false information |    79 | C               |
| University of Exeter students | Exeter      | pct_concerned_ai_data_privacy        | All                             |    68 | C               |
| University of Exeter students | Exeter      | pct_ai_skills_important_to_education | Agree                           |    60 | C               |
| University of Exeter students | Exeter      | pct_worry_flagged_penalised          | Worry fairly to very often      |    37 | C               |
| UK adults                     | UK          | pct_would_trust_for_decisions        | Physics-based forecasts         |    80 | B               |
| UK adults                     | UK          | pct_rate_forecast_accurate           | Physics-based forecasts         |    78 | B               |
| UK adults 16+                 | UK          | pct_perceived_risk                   | Information may be inaccurate   |    74 | A               |
| UK adults 16+                 | UK          | pct_perceived_risk                   | Privacy and security            |    69 | A               |

---

## Query 6: q06_age_structure

**Business Question:** How young is Exeter's adult (16+) population compared with the South West and England?

**Plain-English Explanation:**
This query rescales Census 2021 age bands to shares of adults aged 16+ and sums them into three groups (16–34, 35–64, 65+). It shows one row per place.

**Assumptions:** Under-16s are excluded so the figures match survey populations.
**Limitations:** These are 2021 figures; the 2024 estimate shows Exeter is still the county's youngest district (median age 35).

**SQL:**
```sql
-- @name: q06_age_structure
-- How young is Exeter's adult (16+) population compared with the South West and England?
WITH adults AS (
    SELECT geography, segment AS age_band, value
    FROM indicators
    WHERE source_id = 'ONS_CENSUS' AND segment_type = 'age_band'
),
shares AS (
    SELECT geography, age_band,
           100.0 * value / SUM(value) OVER (PARTITION BY geography) AS pct_of_adults
    FROM adults
)
SELECT
    geography,
    ROUND(SUM(CASE WHEN age_band IN ('16-19','20-24','25-34') THEN pct_of_adults END), 1) AS pct_aged_16_34,
    ROUND(SUM(CASE WHEN age_band IN ('35-49','50-64')         THEN pct_of_adults END), 1) AS pct_aged_35_64,
    ROUND(SUM(CASE WHEN age_band IN ('65-74','75-84','85+')   THEN pct_of_adults END), 1) AS pct_aged_65_plus
FROM shares
GROUP BY geography
ORDER BY pct_aged_16_34 DESC;
```

**Result (3 rows):**

| geography   |   pct_aged_16_34 |   pct_aged_35_64 |   pct_aged_65_plus |
|:------------|-----------------:|-----------------:|-------------------:|
| Exeter      |             40.3 |             40.1 |               19.6 |
| England     |             29.8 |             47.7 |               22.5 |
| South West  |             26.9 |             46.1 |               27   |

---

## Query 7: q07_exeter_adoption_estimate

**Business Question:** If Exeter adults used AI at national rates for their age, what share would have used generative AI?

**Plain-English Explanation:**
This query age-standardises national generative AI use by age (100 − non-use, University of Exeter/YouGov, March 2025) to the Census 2021 age profiles of Exeter and England. It takes Exeter's ratio to England as an index and applies that to DSIT's UK figure of 59%. The 25–34 band is split three ways as a sensitivity test. It shows one row per sensitivity scenario.

**Assumptions:** England is used as a proxy for the UK baseline. Using the ratio carries the 2025 age gradient forward to the 2025/26 level of use.
**Limitations:** Age only: it ignores Exeter's high share of students and graduates, so the true figure is probably **higher**. It's a modelled estimate, not a measurement.

**SQL:**
```sql
-- @name: q07_exeter_adoption_estimate
-- If Exeter adults used AI at national rates for their age, how would Exeter compare with England and the UK's 59%?
-- Method: age-standardisation. National usage by age = 100 - non-use (Stoeckel/YouGov, Mar 2025).
-- Census bands mapped to survey bands. 25-34 straddles 18-29 and 30-49: the share assigned to 18-29
-- is varied (0.0 / 0.5 / 1.0) as a sensitivity test. The Exeter/England ratio is applied to DSIT's UK 59%.
WITH use_by_band AS (
    SELECT segment AS survey_band, 100 - value AS pct_use
    FROM indicators
    WHERE source_id = 'UOE_STOECKEL' AND metric = 'pct_non_users_genai' AND segment_type = 'age_band'
),
census AS (
    SELECT geography, segment AS age_band, value AS pct_pop
    FROM indicators
    WHERE source_id = 'ONS_CENSUS' AND segment_type = 'age_band' AND geography IN ('Exeter','England')
),
splits(split_25_34) AS (VALUES (0.0), (0.5), (1.0)),
mapped AS (
    SELECT s.split_25_34, c.geography,
           CASE WHEN c.age_band IN ('16-19','20-24') THEN '18-29'
                WHEN c.age_band = '35-49'            THEN '30-49'
                WHEN c.age_band = '50-64'            THEN '50-64'
                ELSE '65+' END AS survey_band,
           c.pct_pop AS weight
    FROM census c CROSS JOIN splits s WHERE c.age_band <> '25-34'
    UNION ALL
    SELECT s.split_25_34, c.geography, '18-29', c.pct_pop * s.split_25_34
    FROM census c CROSS JOIN splits s WHERE c.age_band = '25-34'
    UNION ALL
    SELECT s.split_25_34, c.geography, '30-49', c.pct_pop * (1 - s.split_25_34)
    FROM census c CROSS JOIN splits s WHERE c.age_band = '25-34'
),
weighted AS (
    SELECT m.split_25_34, m.geography,
           SUM(m.weight * u.pct_use) / SUM(m.weight) AS age_std_use
    FROM mapped m JOIN use_by_band u USING (survey_band)
    GROUP BY m.split_25_34, m.geography
),
uk AS (
    SELECT value AS uk_rate FROM indicators
    WHERE source_id = 'DSIT_PES' AND metric = 'pct_used_genai_last_3m'
      AND geography = 'UK' AND segment_type = 'all'
)
SELECT
    x.split_25_34                                       AS share_of_25_34_treated_as_18_29,
    ROUND(x.age_std_use, 1)                             AS exeter_rate_2025_levels,
    ROUND(e.age_std_use, 1)                             AS england_rate_2025_levels,
    ROUND(x.age_std_use / e.age_std_use, 3)             AS exeter_index_vs_england,
    ROUND(uk.uk_rate * x.age_std_use / e.age_std_use)   AS est_exeter_pct_used_genai_2025_26
FROM weighted x
JOIN weighted e ON e.split_25_34 = x.split_25_34 AND e.geography = 'England'
CROSS JOIN uk
WHERE x.geography = 'Exeter'
ORDER BY x.split_25_34;
```

**Result (3 rows):**

|   share_of_25_34_treated_as_18_29 |   exeter_rate_2025_levels |   england_rate_2025_levels |   exeter_index_vs_england |   est_exeter_pct_used_genai_2025_26 |
|----------------------------------:|--------------------------:|---------------------------:|--------------------------:|------------------------------------:|
|                               0   |                      34.9 |                       30.6 |                     1.143 |                                  67 |
|                               0.5 |                      37.1 |                       32.8 |                     1.131 |                                  67 |
|                               1   |                      39.3 |                       35.1 |                     1.12  |                                  66 |

---

## Query 8: q08_business_adoption

**Business Question:** How fast are businesses adopting AI, regionally and nationally?

**Plain-English Explanation:**
This query lists every business-adoption figure with its source, period, definition note and quality grade. It shows one row per published figure.

**Assumptions:** None. Definitions are kept visible on purpose.
**Limitations:** The sources define 'using AI' differently and sample different firms. **Don't plot them on one axis.** There are no Exeter-only business figures.

**SQL:**
```sql
-- @name: q08_business_adoption
-- How fast are businesses adopting AI, regionally and nationally? (definitions differ — do not overlay)
SELECT source_id, geography, population, period, metric, value AS pct, quality_grade, notes
FROM indicators
WHERE metric IN ('pct_businesses_using_ai','pct_using_ai','pct_not_using_ai')
ORDER BY source_id, period;
```

**Result (7 rows):**

| source_id   | geography   | population                  | period   | metric                  |   pct | quality_grade   | notes                              |
|:------------|:------------|:----------------------------|:---------|:------------------------|------:|:----------------|:-----------------------------------|
| LLOYDS_25   | South West  | South West businesses       | 2025-06  | pct_businesses_using_ai |    50 | D               | Different definition from ONS BICS |
| LLOYDS_26   | South West  | South West businesses       | 2026-03  | pct_businesses_using_ai |    66 | D               |                                    |
| ONS_BICS    | UK          | UK businesses 10+ employees | 2023-09  | pct_businesses_using_ai |    12 | A               | Approximate; 18 Sep-1 Oct 2023     |
| ONS_BICS    | UK          | UK businesses 10+ employees | 2026-06  | pct_businesses_using_ai |    35 | A               | Approximate; BICS wave 159         |
| OPENAI_SME  | South West  | SMEs                        | 2026     | pct_not_using_ai        |    28 | D               |                                    |
| OPENAI_SME  | London      | SMEs                        | 2026     | pct_using_ai            |    93 | D               |                                    |
| OPENAI_SME  | UK          | SMEs                        | 2026     | pct_not_using_ai        |    19 | D               |                                    |

---

## Query 9: q09_personal_use

**Business Question:** Beyond study, what personal uses do Exeter students make of AI, compared with UK adult users?

**Plain-English Explanation:**
This query lists the Guild's non-academic use items, alongside the closest DSIT items for UK adult users. It shows one row per population and use.

**Assumptions:** DSIT 'companionship' is a reason for using AI rather than a use, but it's included as the nearest comparator.
**Limitations:** The items aren't matched one-to-one. Sensitive uses (depression, loneliness) come from small subgroups and are indicative only.

**SQL:**
```sql
-- @name: q09_personal_use
-- Beyond study, what personal uses do Exeter students make of AI, vs UK adult users?
SELECT
    CASE source_id WHEN 'GUILD_26' THEN 'Exeter students' ELSE 'UK adult genAI users' END AS population_label,
    segment AS use_case,
    value   AS pct
FROM indicators
WHERE (source_id = 'GUILD_26' AND theme = 'personal_use')
   OR (source_id = 'DSIT_PES' AND metric IN ('pct_used_for_purpose','pct_reason_for_use')
       AND segment IN ('Emotional or relationship issues','Legal or financial issues','Companionship'))
ORDER BY population_label, pct DESC;
```

**Result (10 rows, first 8 shown):**

| population_label     | use_case                             |   pct |
|:---------------------|:-------------------------------------|------:|
| Exeter students      | None of the listed non-academic uses |    39 |
| Exeter students      | Advice on a personal issue           |    18 |
| Exeter students      | Understanding medical symptoms       |    18 |
| Exeter students      | Insight into emotions                |     9 |
| Exeter students      | Feeling less alone                   |     4 |
| Exeter students      | Help with depression                 |     4 |
| Exeter students      | Increase happiness                   |     3 |
| UK adult genAI users | Legal or financial issues            |    16 |

---

## Query 10: q10_support_demand

**Business Question:** What help do Exeter students say they want, and where does guidance fall short?

**Plain-English Explanation:**
This query returns the Guild's items on desired course changes, support wanted, and the best-performing faculty's guidance score. It shows one row per item.

**Assumptions:** We store 19% for clearer guidelines (the report also prints 9%).
**Limitations:** Faculty breakdowns are only partly published. Only HLS has a numeric 'helpful guidance' score.

**SQL:**
```sql
-- @name: q10_support_demand
-- What help do Exeter students say they want, and where does guidance fall short?
SELECT metric, segment, value AS pct
FROM indicators
WHERE source_id = 'GUILD_26'
  AND metric IN ('pct_support_wanted','pct_desired_course_change','pct_received_helpful_guidance')
ORDER BY metric, value DESC;
```

**Result (11 rows, first 8 shown):**

| metric                        | segment                             |   pct |
|:------------------------------|:------------------------------------|------:|
| pct_desired_course_change     | Would change nothing                |    33 |
| pct_desired_course_change     | Need clearer guidelines             |    13 |
| pct_desired_course_change     | Ban AI or make it harder to use     |     6 |
| pct_desired_course_change     | Change how AI is taught             |     5 |
| pct_received_helpful_guidance | HLS                                 |    50 |
| pct_support_wanted            | Workshops or training               |    55 |
| pct_support_wanted            | Clearer faculty-specific guidelines |    19 |
| pct_support_wanted            | Ban AI at university                |    10 |

---

## Query 11: q11_local_initiatives

**Business Question:** Which Exeter organisations are deploying AI, and in which sectors?

**Plain-English Explanation:**
This query groups the initiatives register by sector, counting initiatives and listing the organisations. It shows one row per sector.

**Assumptions:** Only initiatives with a published source are included.
**Limitations:** This is a register, not a census: absence from the list doesn't mean an organisation isn't using AI.

**SQL:**
```sql
-- @name: q11_local_initiatives
-- Which Exeter organisations are deploying AI, in which sectors?
SELECT sector, COUNT(*) AS n_initiatives, GROUP_CONCAT(organisation, ' | ') AS organisations
FROM initiatives
GROUP BY sector
ORDER BY n_initiatives DESC, sector;
```

**Result (6 rows):**

| sector            |   n_initiatives | organisations                                                              |
|:------------------|----------------:|:---------------------------------------------------------------------------|
| Health            |               2 | Royal Devon University Healthcare NHS FT | Royal Devon / NIHR HRC / Sanome |
| Local government  |               2 | Devon County Council (County Hall, Exeter) | East Devon District Council   |
| Charity           |               1 | Age UK Exeter                                                              |
| Education         |               1 | University of Exeter                                                       |
| Health research   |               1 | University of Exeter / Royal Devon / PenARC                                |
| Science & weather |               1 | Met Office (Exeter HQ) / Alan Turing Institute                             |

---

## Combined Dataset
Queries 6 and 7 chain together. Q6's age shares feed Q7's age-standardisation, which joins census age bands to the University of Exeter/YouGov usage-by-age figures and the DSIT UK baseline. Q7's output (an estimated **66–67%** of Exeter adults having used generative AI in 2025/26, against 59% for the UK) is the main modelled number going into Step 3. Queries 2–5, 9 and 10 give the Exeter student profile, and Q8 and Q11 give the organisational picture.

## Data Quality Notes Applied
- **Population mixing (brief flag 1):** every comparison query labels populations explicitly. Q3, Q4 and Q9 keep Exeter students, UK undergraduates and UK adults in separate columns, and none adds them together.
- **Missing DSIT South West row (flag 3):** Q7 substitutes a transparent age-standardised estimate, with the method and sensitivity test written into the SQL.
- **Conflicting business definitions (flag 4):** Q8 lists sources separately, with definition notes and quality grades. There's no aggregation across sources.
- **Guild 19% vs 9% inconsistency (flag 5):** stored as 19% and flagged in Q10.
- **Bug found and fixed during QA:** the first version of Q7 matched three rows as the 'UK' baseline (the London and North East rows also have `segment = 'All'`), which tripled its output. Fixed by filtering `geography = 'UK'`. It now returns one row per scenario.
- **Approximate values ('around', 'about'):** kept as published. The notes column travels with Q8.

---

## Pipeline Status
Step 1 ✅ data-explorer  → data_brief.md
Step 2 ✅ sql-architect  → query_library.md
Step 3 ⬜ insight-hunter → findings.md
Step 4 ⬜ viz-builder    → dashboard_spec.md
Step 5 ⬜ story-weaver   → data_story.md
Step 6 ⬜ action-planner → action_plan.md
