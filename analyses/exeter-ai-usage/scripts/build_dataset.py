"""Build the Exeter AI-usage dataset (tidy, one row per indicator value)."""
import csv, sqlite3, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "data"

SRC = {
 "DSIT_PES": ("DSIT", "DSIT Public Engagement Survey 2025/2026 (Official Statistics)",
              "https://www.gov.uk/government/statistics/dsit-public-engagement-survey-20252026/dsit-public-engagement-survey-20252026",
              30698, "Address-based push-to-web probability survey, UK adults 16+, Nov 2025-Mar 2026", "A"),
 "GUILD_26": ("Exeter Students' Guild", "Artificial Intelligence Report (Feb 2026)",
              "https://cdn.prod.website-files.com/61a79279a92cd67f7b6019ac/69babb71ffde303cc8f5915a_Artificial%20Intelligence.pdf",
              None, "Guild student panel (~1,000 volunteers, described as representative of UoE); respondent n not published", "C"),
 "GUILD_25": ("Exeter Students' Guild", "Monthly student survey on AI (reported on Wonkhe, 3 Jun 2025)",
              "https://wonkhe.com/blogs-sus/students-views-on-ai-vary-more-than-you-think/",
              800, "Paid monthly Guild survey, 'nearly 800' responses", "C"),
 "HEPI_26": ("HEPI / Kortext", "Student Generative AI Survey 2026 (HEPI Report 199)",
             "https://www.hepi.ac.uk/2026/03/12/new-hepi-and-kortext-report-student-generative-artificial-intelligence-survey-2026/",
             1054, "Savanta online survey of UK full-time undergraduates, Dec 2025", "B"),
 "ONS_BICS": ("ONS", "Artificial intelligence in UK businesses: 2023 to 2026",
              "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/articles/artificialintelligenceinukbusinesses/2023to2026",
              None, "Business Insights and Conditions Survey (BICS), businesses with 10+ employees unless stated", "A"),
 "LLOYDS_25": ("Lloyds Business Barometer (via TheBusinessDesk)", "South West businesses say greater AI adoption will drive local growth",
               "https://www.thebusinessdesk.com/south-west/news/24062-south-west-businesses-say-greater-ai-adoption-will-drive-local-growth",
               None, "Business panel survey, press-reported (published 24 Jun 2025)", "D"),
 "LLOYDS_26": ("Lloyds Business Barometer (via Business Biscuit)", "South West businesses adopting AI see strong gains in productivity and profitability",
               "https://businessbiscuit.com/business-news/economy-news/south-west-businesses-adopting-ai-see-strong-gains-in-productivity-and-profitability-survey/",
               None, "Business panel survey, press-reported (published 12 Mar 2026)", "D"),
 "OPENAI_SME": ("OpenAI (via Enterprise Nation)", "UK SMEs save over half a day a week with AI",
                "https://www.enterprisenation.com/press/uk-smes-save-over-half-a-day-a-week-with-ai/",
                1000, "Survey of 1,000 UK SME decision-makers; vendor-commissioned", "D"),
 "UOE_STOECKEL": ("University of Exeter (Prof. F. Stoeckel) / YouGov", "Research shows stark social divides in AI use in the workplace",
                  "https://news.exeter.ac.uk/faculty-of-humanities-arts-and-social-sciences/research-shows-stark-social-divides-in-ai-use-in-the-workplace/",
                  1061, "YouGov online survey, March 2025", "B"),
 "METOFFICE_TRUST": ("Met Office (via Meteorological Technology International)", "UK public trusts AI weather forecasts less than traditional methods",
                     "https://www.meteorologicaltechnologyinternational.com/news/artificial-intelligence/uk-public-trusts-ai-weather-forecasts-less-than-traditional-methods-study-finds.html",
                     6000, "Survey of 6,000+ UK adults; article 24 Aug 2026", "B"),
 "ONS_CENSUS": ("ONS", "How life has changed in Exeter: Census 2021",
                "https://www.ons.gov.uk/visualisations/censusareachanges/E07000041",
                None, "Census 2021, usual residents", "A"),
 "ONS_MYE24": ("ONS (via citypopulation.de)", "Mid-2024 population estimates, Exeter (E07000041)",
               "https://www.citypopulation.de/en/uk/england/admin/south_west_england/E07000041__exeter",
               None, "ONS mid-year estimate, 30 Jun 2024", "A"),
}

# (source, theme, population, geo_level, geography, segment_type, segment, metric, value, unit, period, notes)
R = []
def add(*row): R.append(row)

# ---------- Exeter: University of Exeter students (Guild, Feb 2026) ----------
G = ("GUILD_26", None, "University of Exeter students", "City", "Exeter")
for tool, v in [("ChatGPT",84),("Google Gemini",39),("Microsoft Copilot",35),("Canva",29),("Character.ai",4),("DALL-E",3)]:
    add(G[0],"tools",G[2],G[3],G[4],"tool",tool,"pct_ever_used_tool",v,"%","2026-02","Q: Which AI tools have you used?")
for use, v in [("Understanding a concept",71),("Correcting grammar",46),("Feedback on a draft",45),("Research assistance",45),("Summarising readings",43),("Never used AI for academic work",8)]:
    add(G[0],"academic_use",G[2],G[3],G[4],"purpose",use,"pct_used_for_purpose",v,"%","2026-02","Q: What have you used AI for during your studies so far? (multi-select)")
for use, v in [("Advice on a personal issue",18),("Understanding medical symptoms",18),("Insight into emotions",9),("Feeling less alone",4),("Help with depression",4),("Increase happiness",3),("None of the listed non-academic uses",39)]:
    add(G[0],"personal_use",G[2],G[3],G[4],"purpose",use,"pct_used_for_purpose",v,"%","2026-02","Q11 non-academic uses (multi-select)")
for r, v in [("Fast and easy option",31),("Academic purposes",28)]:
    add(G[0],"motivation",G[2],G[3],G[4],"reason",r,"pct_reason_first_use",v,"%","2026-02","Q: What motivated you to first use AI tools?")
for r, v in [("Environmental impact",58),("Self-reliance",20),("Ethical concerns",11)]:
    add(G[0],"barriers",G[2],G[3],G[4],"reason",r,"pct_reason_non_use",v,"%","2026-02","Base: students who choose not to use AI")
for r, v in [("Have received false information",79),("Rarely or never",11),("Unsure",10)]:
    add(G[0],"trust",G[2],G[3],G[4],"response",r,"pct_noticed_false_info",v,"%","2026-02","Q8: How often have you noticed AI giving you false information?")
for r, v in [("Worry fairly to very often",37),("Do not think about it very often",26),("Rarely or never think about it",37)]:
    add(G[0],"attitudes",G[2],G[3],G[4],"response",r,"pct_worry_flagged_penalised",v,"%","2026-02","Q9: worry about work being flagged/penalised for AI use")
for r, v in [("Agree",60),("Disagree",24)]:
    add(G[0],"attitudes",G[2],G[3],G[4],"response",r,"pct_ai_skills_important_to_education",v,"%","2026-02","Q7b")
for fac, v in [("HASS",75),("ESE",60),("HLS",58)]:
    add(G[0],"attitudes",G[2],G[3],G[4],"faculty",fac,"pct_agree_ai_replaces_critical_thinking",v,"%","2026-02","Q7c, somewhat-to-completely agree")
for r, v in [("Would change nothing",33),("Need clearer guidelines",13),("Ban AI or make it harder to use",6),("Change how AI is taught",5)]:
    add(G[0],"policy",G[2],G[3],G[4],"response",r,"pct_desired_course_change",v,"%","2026-02","Q10")
for r, v in [("Workshops or training",55),("Clearer faculty-specific guidelines",19),("Ban AI at university",10),("Education on environmental impact",10),("Education on AI dangers",9),("Support on false accusations",9)]:
    add(G[0],"policy",G[2],G[3],G[4],"response",r,"pct_support_wanted",v,"%","2026-02","Q13; report also prints 9% for clearer guidelines elsewhere (inconsistency)")
for r, v in [("No prior experience",60),("Small amount",18),("Quite a lot",5)]:
    add(G[0],"adoption",G[2],G[3],G[4],"response",r,"pct_prior_ai_in_learning_setting",v,"%","2026-02","Q5 prior AI experience in a learning setting")
add(G[0],"policy",G[2],G[3],G[4],"faculty","HLS","pct_received_helpful_guidance",50,"%","2026-02","Fig 9")

# ---------- Exeter: Guild monthly survey 2025 ----------
for r, v in [("Curious",50),("Concerned",40),("No feelings / don't know",8)]:
    add("GUILD_25","attitudes","University of Exeter students","City","Exeter","feeling",r,"pct_feeling_about_ai",v,"%","2025","Nearly 800 responses")
add("GUILD_25","attitudes","University of Exeter students","City","Exeter","all","All","pct_concerned_ai_data_privacy",68,"%","2025","")
add("GUILD_25","policy","University of Exeter PGR students","City","Exeter","response","Agree","pct_support_stricter_ai_policies",58,"%","2025","18% disagree")
add("GUILD_25","policy","University of Exeter PGR students","City","Exeter","response","Disagree","pct_support_stricter_ai_policies",18,"%","2025","")

# ---------- Exeter: demographic context ----------
for band, ex, sw, en in [("16-19",8.1,4.4,4.6),("20-24",12.5,5.8,6.0),("25-34",13.8,12.1,13.6),("35-49",17.7,17.9,19.4),
                         ("50-64",16.5,20.4,19.4),("65-74",8.6,11.7,9.8),("75-84",5.6,7.6,6.1),("85+",2.5,3.1,2.4)]:
    add("ONS_CENSUS","context","All usual residents","City","Exeter","age_band",band,"pct_population",ex,"%","2021","Census 2021")
    add("ONS_CENSUS","context","All usual residents","Region","South West","age_band",band,"pct_population",sw,"%","2021","Census 2021")
    add("ONS_CENSUS","context","All usual residents","Country","England","age_band",band,"pct_population",en,"%","2021","Census 2021")
for geo, lvl, v in [("Exeter","City",15.8),("South West","Region",5.0),("England","Country",5.6)]:
    add("ONS_CENSUS","context","Usual residents aged 16+",lvl,geo,"economic_status","Economically inactive: student","pct_population",v,"%","2021","Census 2021")
add("ONS_MYE24","context","All usual residents","City","Exeter","all","All","population",138399,"count","2024-06","Up ~2% on 2023; median age 35")

# ---------- UK adults benchmark (DSIT PES 2025/26) ----------
D = ("DSIT_PES","UK adults 16+","Country","UK")
add(D[0],"adoption",D[1],D[2],D[3],"all","All","pct_used_genai_last_3m",59,"%","2025/26","")
add(D[0],"adoption",D[1],D[2],D[3],"all","All","pct_aware_of_ai",97,"%","2025/26","")
for t, v in [("Human-like text/speech AI",56),("AI digital assistants",54),("Image/video/music creation",32),("Workplace AI systems",19),("Robotic AI technology",14)]:
    add(D[0],"tools",D[1],D[2],D[3],"ai_type",t,"pct_used_last_3m",v,"%","2025/26","")
for q, v in [("Degree level or above",75),("Other qualifications",48),("No qualifications",19)]:
    add(D[0],"adoption",D[1],D[2],D[3],"qualification",q,"pct_used_genai_last_3m",v,"%","2025/26","")
for a, v in [("Under 45 (each band)",75),("75-84",18),("85+",8)]:
    add(D[0],"adoption",D[1],D[2],D[3],"age_band",a,"pct_used_genai_last_3m",v,"%","2025/26","Under-45 value is a floor ('75% or over'); 45-74 bands only in table E5")
for g, lvl, v in [("London","Region",69),("North East","Region",51)]:
    add(D[0],"adoption",D[1],lvl,g,"all","All","pct_used_genai_last_3m",v,"%","2025/26","Highest/lowest ITL1; South West value in table E6 (not retrieved)")
DU = ("DSIT_PES","UK adult genAI users (online)","Country","UK")
for s, v in [("Personal",83),("Work",54),("Education/study",27)]:
    add(DU[0],"setting",DU[1],DU[2],DU[3],"setting",s,"pct_users_by_setting",v,"%","2025/26","")
for f, v in [("At least weekly",75),("At least daily",35)]:
    add(DU[0],"frequency",DU[1],DU[2],DU[3],"frequency",f,"pct_users",v,"%","2025/26","")
for a, v in [("Writing/editing documents",58),("Work purposes",46),("Editing images/video/sound",40),("Legal or financial issues",16),("Applying for jobs",14),("Emotional or relationship issues",10)]:
    add(DU[0],"purpose",DU[1],DU[2],DU[3],"purpose",a,"pct_used_for_purpose",v,"%","2025/26","")
for r, v in [("Saving time",65),("Generating ideas",55),("Summarising or explaining",48),("Companionship",3)]:
    add(DU[0],"motivation",DU[1],DU[2],DU[3],"reason",r,"pct_reason_for_use",v,"%","2025/26","")
DN = ("DSIT_PES","UK adult non-users (online)","Country","UK")
for r, v in [("Prefer not to use AI",44),("Privacy or security worries",33),("Don't know enough",32),("Worried about accuracy",31)]:
    add(DN[0],"barriers",DN[1],DN[2],DN[3],"reason",r,"pct_reason_non_use",v,"%","2025/26","")
for r, v in [("Information may be inaccurate",74),("Privacy and security",69),("Spreading false information",64),("Job losses",63),("Misleading images or videos",62),("Harm to creative/critical thinking",57),("No concerns",3)]:
    add(D[0],"trust",D[1],D[2],D[3],"risk",r,"pct_perceived_risk",v,"%","2025/26","")

# ---------- UK undergraduates (HEPI 2026) ----------
H = ("HEPI_26","UK full-time undergraduates","Country","UK")
add(H[0],"adoption",H[1],H[2],H[3],"all","All","pct_use_ai_any_form",95,"%","2025-12","66% in 2024, 92% in 2025")
add(H[0],"adoption",H[1],H[2],H[3],"year","2024","pct_use_ai_any_form",66,"%","2024","")
add(H[0],"adoption",H[1],H[2],H[3],"year","2025","pct_use_ai_any_form",92,"%","2025","")
add(H[0],"academic_use",H[1],H[2],H[3],"all","All","pct_use_genai_for_assessed_work",94,"%","2025-12","")
for u, v in [("Explaining concepts",61),("Summarising articles",49),("Research ideas",40),("Structuring thoughts",39),("Searching the internet",36)]:
    add(H[0],"academic_use",H[1],H[2],H[3],"purpose",u,"pct_used_for_purpose",v,"%","2025-12","Assessed-work uses")
for y, v in [("2024",3),("2025",8),("2026",12)]:
    add(H[0],"academic_use",H[1],H[2],H[3],"year",y,"pct_include_ai_text_in_assessed_work",v,"%",y,"")
add(H[0],"attitudes",H[1],H[2],H[3],"all","All","pct_ai_improved_student_experience",49,"%","2025-12","16% worsened, 35% no change")

# ---------- Exeter-led national study ----------
S = ("UOE_STOECKEL","UK adults (YouGov)","Country","UK")
for a, v in [("18-29",37),("30-49",64),("50-64",78),("65+",89)]:
    add(S[0],"adoption",S[1],S[2],S[3],"age_band",a,"pct_non_users_genai",v,"%","2025-03","")
for g, v in [("Men",65),("Women",73)]:
    add(S[0],"adoption",S[1],S[2],S[3],"sex",g,"pct_non_users_genai",v,"%","2025-03","")
for o, op, th in [("Professional/managerial",41,24),("Admin/sales/service",25,39)]:
    add(S[0],"attitudes",S[1],S[2],S[3],"occupation",o,"pct_see_genai_as_job_opportunity",op,"%","2025-03","")
    add(S[0],"attitudes",S[1],S[2],S[3],"occupation",o,"pct_see_genai_as_job_threat",th,"%","2025-03","")

# ---------- Met Office (Exeter-HQ) public trust ----------
M = ("METOFFICE_TRUST","UK adults","Country","UK")
for m, v in [("Physics-based forecasts",78),("AI-generated forecasts",45)]:
    add(M[0],"trust",M[1],M[2],M[3],"forecast_type",m,"pct_rate_forecast_accurate",v,"%","2026","Approximate ('around')")
for m, v in [("Physics-based forecasts",80),("AI-generated forecasts",40)]:
    add(M[0],"trust",M[1],M[2],M[3],"forecast_type",m,"pct_would_trust_for_decisions",v,"%","2026","Approximate ('about')")

# ---------- Businesses ----------
add("ONS_BICS","business","UK businesses 10+ employees","Country","UK","year","2023","pct_businesses_using_ai",12,"%","2023-09","Approximate; 18 Sep-1 Oct 2023")
add("ONS_BICS","business","UK businesses 10+ employees","Country","UK","year","2026","pct_businesses_using_ai",35,"%","2026-06","Approximate; BICS wave 159")
for t, v in [("Large language models",18),("Visual content creation",16),("ML data processing",12),("ML image processing",6),("Robotics",2)]:
    add("ONS_BICS","business","UK businesses 10+ employees","Country","UK","ai_type",t,"pct_businesses_using",v,"%","2026-06","")
add("ONS_BICS","business","UK businesses 10+ employees","Country","UK","all","All","pct_no_barriers_to_adoption",41,"%","2026-06","")
add("LLOYDS_25","business","South West businesses","Region","South West","all","All","pct_businesses_using_ai",50,"%","2025-06","Different definition from ONS BICS")
add("LLOYDS_26","business","South West businesses","Region","South West","all","All","pct_businesses_using_ai",66,"%","2026-03","")
add("LLOYDS_26","business","South West businesses","Region","South West","all","All","pct_invested_in_ai",58,"%","2026-03","")
add("LLOYDS_26","business","South West businesses integrating AI","Region","South West","all","All","pct_increased_productivity",70,"%","2026-03","")
add("LLOYDS_26","business","South West businesses","Region","South West","all","All","pct_higher_profits_12m",42,"%","2026-03","")
add("OPENAI_SME","business","SMEs","Region","South West","all","All","pct_not_using_ai",28,"%","2026","")
add("OPENAI_SME","business","SMEs","Region","London","all","All","pct_using_ai",93,"%","2026","")
add("OPENAI_SME","business","SMEs","Country","UK","all","All","pct_not_using_ai",19,"%","2026","")

COLS = ["row_id","source_id","theme","population","geo_level","geography","segment_type","segment","metric","value","unit","period",
        "notes","source_org","source_title","source_url","sample_n","method","quality_grade"]
rows = []
for i, r in enumerate(R, 1):
    s = SRC[r[0]]
    rows.append([i, *r, s[0], s[1], s[2], s[3], s[4], s[5]])

# Institutional use cases in Exeter (qualitative register)
INIT = [
 ("Royal Devon University Healthcare NHS FT","Health","Ambient voice technology (AI scribe) in Epic EPR; ED pilot","Live outpatient use; 12-month ED pilot from Jan 2026","2,700+ outpatient consultations; up to ~15,000 extra appointments/yr projected at full rollout","https://www.digitalhealth.net/?p=260341"),
 ("Royal Devon / NIHR HRC / Sanome","Health","MEMORI AI early detection of hospital-acquired infections","Ward trials; £300k+ Innovate UK grant (Feb 2026)","Evaluation data expected 2026","https://www.bio-itworld.com/news/2026/02/09/innovate-uk-awards-over-300k-smart-grant-to-exeter-healthtech-research-centre-and-sanome-to-advance-ai-enabled-early-detection-of-hospital-acquired-infections"),
 ("University of Exeter / Royal Devon / PenARC","Health research","SAMueL-2 machine learning to personalise stroke care","Research project","National data on ~250,000 stroke cases","https://www.digitalhealth.net/?p=226341"),
 ("Met Office (Exeter HQ) / Alan Turing Institute","Science & weather","FastNet ML weather prediction model; ML in IMPROVER forecast blend","Experimental; not solely-AI operational forecasts","Comparable to Met Office Global Model on RMSE","https://www.metoffice.gov.uk/about-us/news-and-media/media-centre/weather-and-climate-news/2026/new-research-shows-ai-can-produce-trustworthy-physically-realistic-weather-forecasts-"),
 ("University of Exeter","Education","Enabling AI strategy, AI policy, approved tool catalogue (Copilot, Amazon Quick, Gemini) for staff and students","Live","Assessments split into four AI-use categories","https://www.exeter.ac.uk/ai-catalogue/student/"),
 ("Devon County Council (County Hall, Exeter)","Local government","Microsoft Copilot Chat and licensed M365 Copilot for drafting, summarising, research","Live (policy page published Apr 2026)","AI does not make decisions; no personal data without approval","https://www.devon.gov.uk/?p=14078"),
 ("East Devon District Council","Local government","Copilot used to summarise 1.1m+ words of consultation feedback on new town east of Exeter","Used for planning consultation","~21,000 homes proposed","https://www.devonairradio.com/news/exeter-and-east-devon/east-devon-harnesses-ai-for-million-word-feedback"),
 ("Age UK Exeter","Charity","AI in the Workplace Policy","Approved Dec 2025","Policy governs staff use of AI tools","https://www.ageuk.org.uk/bp-assets/globalassets/exeter/2024-policies/2025-policies/2026-policies/auke-ai-in-the-workplace-policy-v1.pdf"),
]
ICOLS = ["organisation","sector","use_case","status","scale_or_detail","source_url"]

OUT.mkdir(parents=True, exist_ok=True)
with open(OUT/"exeter_ai_indicators.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
with open(OUT/"exeter_ai_initiatives.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(ICOLS); w.writerows(INIT)
db = OUT/"exeter_ai.db"
if db.exists(): db.unlink()
con = sqlite3.connect(db)
con.execute(f"CREATE TABLE indicators ({', '.join(c + (' REAL' if c in ('value','sample_n') else ' INTEGER' if c=='row_id' else ' TEXT') for c in COLS)})")
con.executemany(f"INSERT INTO indicators VALUES ({','.join('?'*len(COLS))})", rows)
con.execute(f"CREATE TABLE initiatives ({', '.join(c+' TEXT' for c in ICOLS)})")
con.executemany(f"INSERT INTO initiatives VALUES ({','.join('?'*len(ICOLS))})", INIT)
con.commit(); con.close()
print(len(rows), "indicator rows;", len(INIT), "initiatives")
