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

-- @name: q08_business_adoption
-- How fast are businesses adopting AI, regionally and nationally? (definitions differ — do not overlay)
SELECT source_id, geography, population, period, metric, value AS pct, quality_grade, notes
FROM indicators
WHERE metric IN ('pct_businesses_using_ai','pct_using_ai','pct_not_using_ai')
ORDER BY source_id, period;

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

-- @name: q10_support_demand
-- What help do Exeter students say they want, and where does guidance fall short?
SELECT metric, segment, value AS pct
FROM indicators
WHERE source_id = 'GUILD_26'
  AND metric IN ('pct_support_wanted','pct_desired_course_change','pct_received_helpful_guidance')
ORDER BY metric, value DESC;

-- @name: q11_local_initiatives
-- Which Exeter organisations are deploying AI, in which sectors?
SELECT sector, COUNT(*) AS n_initiatives, GROUP_CONCAT(organisation, ' | ') AS organisations
FROM initiatives
GROUP BY sector
ORDER BY n_initiatives DESC, sector;
