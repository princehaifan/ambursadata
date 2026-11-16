# Exeter AI Usage Dataset (v1, Nov 2026)

A compiled, source-linked dataset on how people in Exeter use AI, built for the ambursaData pipeline.

Live dashboard: https://claude.ai/artifact/PHntnSmJrxTKoJM1c8yeGN (private until shared)

## Pipeline outputs (ambursaData steps 1–6)
1. `data_brief.md`: what the data is, its quality (AMBER) and its limits
2. `query_library.md` + `sql/queries.sql`: 11 SQLite queries with real results
3. `findings.md`: the top 3 findings, anomalies and opportunities
4. `dashboard_spec.md` + `dashboard/`: the dashboard design, its page code and the data files behind each chart
5. `data_story.md`: plain-English story for the organisations involved
6. `action_plan.md`: prioritised actions, proposed owners, 30/60/90-day checks

Headline: an estimated 63–67% of Exeter adults have used generative AI (modelled), against 59% for the UK (DSIT 2025/26).

## How to rebuild
```bash
pip install pandas tabulate
python scripts/build_dataset.py        # rebuilds data/ from the source list
python scripts/run_queries.py          # runs sql/queries.sql against data/exeter_ai.db
python scripts/make_query_library.py   # regenerates query_library.md with fresh results
```
To add a source (e.g. the DSIT South West row, table E6), add rows in `build_dataset.py` and rerun all three.

## Files
- `data/exeter_ai_indicators.csv`: 167 tidy rows, one published statistic per row
- `data/exeter_ai_initiatives.csv`: 8 named AI deployments in Exeter organisations
- `data/exeter_ai.db`: SQLite copy of both files (tables `indicators`, `initiatives`)
- `scripts/build_dataset.py`: rebuilds everything from the source list

## Columns (indicators)
| column | meaning |
|---|---|
| source_id | short key for the source |
| theme | adoption, tools, academic_use, personal_use, purpose, motivation, barriers, trust, attitudes, policy, setting, frequency, business, context |
| population | who the figure describes (e.g. "University of Exeter students"). Only compare rows within the same population. |
| geo_level / geography | City (Exeter), Region (South West, London...), Country (UK, England) |
| segment_type / segment | the breakdown (age_band, tool, purpose, faculty...) and its value |
| metric | what the number measures |
| value / unit | the number (% or count) |
| period | fieldwork or publication period |
| notes | caveats and question wording |
| source_org, source_title, source_url, sample_n, method | provenance |
| quality_grade | A official statistics · B robust named survey · C self-selecting local panel · D press-reported or vendor-commissioned |

## Main limitation
There is no representative survey of Exeter residents on AI. Exeter-level usage data covers University of Exeter students (Exeter Students' Guild). City-wide adoption can only be estimated by applying national age and education gradients to Exeter's demographics.

## Sources
- DSIT Public Engagement Survey 2025/2026: https://www.gov.uk/government/statistics/dsit-public-engagement-survey-20252026/dsit-public-engagement-survey-20252026
- Exeter Students' Guild, Artificial Intelligence Report (Feb 2026): https://cdn.prod.website-files.com/61a79279a92cd67f7b6019ac/69babb71ffde303cc8f5915a_Artificial%20Intelligence.pdf
- Exeter Students' Guild survey (Wonkhe, Jun 2025): https://wonkhe.com/blogs-sus/students-views-on-ai-vary-more-than-you-think/
- HEPI Student Generative AI Survey 2026: https://www.hepi.ac.uk/2026/03/12/new-hepi-and-kortext-report-student-generative-artificial-intelligence-survey-2026/
- ONS, AI in UK businesses 2023–2026: https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/articles/artificialintelligenceinukbusinesses/2023to2026
- Lloyds Business Barometer, South West (Jun 2025): https://www.thebusinessdesk.com/south-west/news/24062-south-west-businesses-say-greater-ai-adoption-will-drive-local-growth
- Lloyds Business Barometer, South West (Mar 2026): https://businessbiscuit.com/business-news/economy-news/south-west-businesses-adopting-ai-see-strong-gains-in-productivity-and-profitability-survey/
- OpenAI SME survey: https://www.enterprisenation.com/press/uk-smes-save-over-half-a-day-a-week-with-ai/
- University of Exeter (Stoeckel), social divides in AI use: https://news.exeter.ac.uk/faculty-of-humanities-arts-and-social-sciences/research-shows-stark-social-divides-in-ai-use-in-the-workplace/
- Met Office public trust in AI forecasts: https://www.meteorologicaltechnologyinternational.com/news/artificial-intelligence/uk-public-trusts-ai-weather-forecasts-less-than-traditional-methods-study-finds.html
- ONS Census 2021, Exeter: https://www.ons.gov.uk/visualisations/censusareachanges/E07000041
- ONS mid-2024 estimate, Exeter: https://www.citypopulation.de/en/uk/england/admin/south_west_england/E07000041__exeter
- Initiative sources are listed per row in `exeter_ai_initiatives.csv`.
