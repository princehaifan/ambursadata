import re, os, pandas as pd
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sql=open("sql/queries.sql").read()
blocks={re.match(r"-- @name: (\w+)",b).group(1):b.strip() for b in re.split(r"(?=^-- @name: )",sql,flags=re.M) if b.startswith("-- @name")}
res=pd.read_pickle("sql/results.pkl")
META = {
"q01_source_coverage": ("How much of the evidence is truly about Exeter, and how reliable is each slice?",
 "This query counts indicator rows and distinct sources from the `indicators` table, grouped by geography level, place and quality grade. It shows one row per place and quality grade.",
 "None. All 167 rows are included.", "Row counts measure how much evidence exists, not how important it is."),
"q02_exeter_tool_share": ("Which AI tools have University of Exeter students used?",
 "This query takes the Guild Feb 2026 tool question, ranks the tools by the share of students who have used each, and expresses each as a fraction of ChatGPT's reach. It shows one row per tool.",
 "Multi-select question, so shares don't add up to 100%.", "'Ever used' says nothing about how often. The panel is self-selecting (grade C)."),
"q03_purpose_comparison": ("Do Exeter students use AI for the same things as UK undergraduates and UK adult users?",
 "This query maps differently worded purpose questions from three surveys (Guild, HEPI, DSIT) onto five common purpose groups, places the populations side by side, and calculates the Exeter-minus-UK-undergraduate gap in percentage points. It shows one row per purpose group.",
 "Where one survey has two items in a group (e.g. grammar and draft feedback), MAX takes the highest. HEPI items refer to assessed work.", "Question wording and bases differ, so gaps are directional, not statistically tested. Missing cells mean that survey didn't ask the question."),
"q04_barriers_comparison": ("Why do people who avoid AI avoid it: Exeter students or UK adults?",
 "This query pulls every 'reason for not using AI' row and ranks the reasons within each population. It shows one row per population and reason.",
 "The bases are non-users only: Exeter students who choose not to use AI, and UK adult non-users in DSIT's online sample.", "The two surveys offered different answer lists, so a reason missing from one list doesn't mean nobody holds it."),
"q05_trust_and_anxiety": ("How much do people trust AI output, and how anxious are they about it?",
 "This query selects the headline trust, risk and anxiety measures for Exeter students (Guild 2025/26), UK adults (DSIT) and the Met Office forecast-trust study, keeping only the 'yes/concerned' side of each question. It shows one row per measure.",
 "Negative or neutral response options are excluded to keep one headline value per question.", "The measures aren't the same question across populations. Read them as context, not as like-for-like comparisons."),
"q06_age_structure": ("How young is Exeter's adult (16+) population compared with the South West and England?",
 "This query rescales Census 2021 age bands to shares of adults aged 16+ and sums them into three groups (16–34, 35–64, 65+). It shows one row per place.",
 "Under-16s are excluded so the figures match survey populations.", "These are 2021 figures; the 2024 estimate shows Exeter is still the county's youngest district (median age 35)."),
"q07_exeter_adoption_estimate": ("If Exeter adults used AI at national rates for their age, what share would have used generative AI?",
 "This query age-standardises national generative AI use by age (100 − non-use, University of Exeter/YouGov, March 2025) to the Census 2021 age profiles of Exeter and England. It takes Exeter's ratio to England as an index and applies that to DSIT's UK figure of 59%. The 25–34 band is split three ways as a sensitivity test. It shows one row per sensitivity scenario.",
 "England is used as a proxy for the UK baseline. Using the ratio carries the 2025 age gradient forward to the 2025/26 level of use.", "Age only: it ignores Exeter's high share of students and graduates, so the true figure is probably **higher**. It's a modelled estimate, not a measurement."),
"q08_business_adoption": ("How fast are businesses adopting AI, regionally and nationally?",
 "This query lists every business-adoption figure with its source, period, definition note and quality grade. It shows one row per published figure.",
 "None. Definitions are kept visible on purpose.", "The sources define 'using AI' differently and sample different firms. **Don't plot them on one axis.** There are no Exeter-only business figures."),
"q09_personal_use": ("Beyond study, what personal uses do Exeter students make of AI, compared with UK adult users?",
 "This query lists the Guild's non-academic use items, alongside the closest DSIT items for UK adult users. It shows one row per population and use.",
 "DSIT 'companionship' is a reason for using AI rather than a use, but it's included as the nearest comparator.", "The items aren't matched one-to-one. Sensitive uses (depression, loneliness) come from small subgroups and are indicative only."),
"q10_support_demand": ("What help do Exeter students say they want, and where does guidance fall short?",
 "This query returns the Guild's items on desired course changes, support wanted, and the best-performing faculty's guidance score. It shows one row per item.",
 "We store 19% for clearer guidelines (the report also prints 9%).", "Faculty breakdowns are only partly published. Only HLS has a numeric 'helpful guidance' score."),
"q11_local_initiatives": ("Which Exeter organisations are deploying AI, and in which sectors?",
 "This query groups the initiatives register by sector, counting initiatives and listing the organisations. It shows one row per sector.",
 "Only initiatives with a published source are included.", "This is a register, not a census: absence from the list doesn't mean an organisation isn't using AI."),
}
def md_table(df, n=8):
    df=df.head(n).copy()
    df=df.fillna("—")
    return df.to_markdown(index=False)
out=["# Query Library","Pipeline step: 2 of 6 — ambursaData","Date: 16 November 2026",
"Dataset: Exeter AI Usage Dataset v1 (tables `indicators`, `initiatives` in `data/exeter_ai.db`)",
"Dialect: SQLite 3 (portable to PostgreSQL/DuckDB; only `GROUP_CONCAT` → `STRING_AGG` needs changing)","","---","","## Query Index",
"| # | Query Name | Business Question Answered |","|---|------------|---------------------------|"]
for i,k in enumerate(blocks,1): out.append(f"| {i} | {k} | {META[k][0]} |")
out+=["","All 11 queries were executed against the database. The sample results below are real output, not illustrative.","","---",""]
for i,(k,b) in enumerate(blocks.items(),1):
    q,expl,ass,lim=META[k]
    out+=[f"## Query {i}: {k}","",f"**Business Question:** {q}","","**Plain-English Explanation:**",expl,"",
          f"**Assumptions:** {ass}",f"**Limitations:** {lim}","","**SQL:**","```sql",b,"```","",
          f"**Result ({len(res[k])} rows{', first 8 shown' if len(res[k])>8 else ''}):**","",md_table(res[k]),"","---",""]
out+=["## Combined Dataset","Queries 6 and 7 chain together. Q6's age shares feed Q7's age-standardisation, which joins census age bands to the University of Exeter/YouGov usage-by-age figures and the DSIT UK baseline. Q7's output (an estimated **66–67%** of Exeter adults having used generative AI in 2025/26, against 59% for the UK) is the main modelled number going into Step 3. Queries 2–5, 9 and 10 give the Exeter student profile, and Q8 and Q11 give the organisational picture.","",
"## Data Quality Notes Applied",
"- **Population mixing (brief flag 1):** every comparison query labels populations explicitly. Q3, Q4 and Q9 keep Exeter students, UK undergraduates and UK adults in separate columns, and none adds them together.",
"- **Missing DSIT South West row (flag 3):** Q7 substitutes a transparent age-standardised estimate, with the method and sensitivity test written into the SQL.",
"- **Conflicting business definitions (flag 4):** Q8 lists sources separately, with definition notes and quality grades. There's no aggregation across sources.",
"- **Guild 19% vs 9% inconsistency (flag 5):** stored as 19% and flagged in Q10.",
"- **Bug found and fixed during QA:** the first version of Q7 matched three rows as the 'UK' baseline (the London and North East rows also have `segment = 'All'`), which tripled its output. Fixed by filtering `geography = 'UK'`. It now returns one row per scenario.",
"- **Approximate values ('around', 'about'):** kept as published. The notes column travels with Q8.","","---","",
"## Pipeline Status","Step 1 ✅ data-explorer  → data_brief.md","Step 2 ✅ sql-architect  → query_library.md","Step 3 ⬜ insight-hunter → findings.md","Step 4 ⬜ viz-builder    → dashboard_spec.md","Step 5 ⬜ story-weaver   → data_story.md","Step 6 ⬜ action-planner → action_plan.md",""]
open("query_library.md","w").write("\n".join(out))
print("ok", sum(len(x) for x in out))
