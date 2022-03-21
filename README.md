# PLUS Explorer

This is the source repository for the code used to make the materials referred to in this
[blog post](https://www.lovelawrobots.com/evaluating-legislation-for-readability-exploring-plus/).

## Introduction

On 31 December 2021,
the [Attorney General Chambers of Singapore completed a universal revision of Singapore's Acts of Parliament](https://www.agc.gov.sg/our-roles/drafter-of-laws/legislation-and-revisions)
. Among other changes implemented, **"Plain English is used as much as possible"**. A list of the types of changes made
can be
found [here](https://www-agc-gov-sg-admin.cwp.sg/docs/default-source/our-roles-documents/drafter-of-laws/list-of-standard-revision-changes.pdf)
.

**PLUS Explorer** aims to explore the following issues:

* What are the changes made and how do they look like in a broad spectrum of clauses?
* Do they make legislation more readable?

To view and explore the data, visit:

* [Section Explorer](https://share.streamlit.io/houfu/plus-explorer/main/explorer.py)
* [Graph Explorer](https://share.streamlit.io/houfu/plus-explorer/main/graphs.py)

_A note on the selection of sections_

I manually and randomly selected 150 sections from Statutes Singapore Online and picked the latest 2020 Rev Edn version
and compared it with the _immediately preceding_ version.

By random, I mean that I went through a list of legislation, picked one that seems interesting and then picked a section
which sounded interesting, keeping in mind that I would like a variety of clauses in the dataset. Some sections
experienced _no changes at all_, I left them inside the dataset as it was important to show that not all sections are
affected by changes.

## Contents

| File                     | Description                                               |
|--------------------------|-----------------------------------------------------------|
| `explorer.py`            | Section Explorer Source code                              | 
| `graphs.py`              | Graph explorer source code                                |
| `data.csv.gz`            | Source data in GZIP CSV format                            |
| `vega_source\`           | Directory containing source files of compiled vega charts |
| `ipynb\data_input.ipynb` | Jupyter notebook used to initially compile data CSV       |

_NB_: I initally compiled most of the data in the notebook but added more columns by using map functions.

The columns in the CSV file are

| Column header                  | Description                                                            |
|--------------------------------|------------------------------------------------------------------------| 
| 'act_name'                     | Name of act of Parliament                                              |
| 'previous'                     | Content of section as of immediately prior to 2020 Rev Edn             | 
| 'previous_link'                | Link to SSO of section immediately prior to 2020 Rev Edn               |
| 'previous_len'                 | Length / No of characters of section immediately prior to 2020 Rev Edn |
| 'previous_flesch_reading_ease' | FRE score of section immediately prior to 2020 Rev Edn                 |
| 'previous_gunning_fog'         | FOG score of section immediately prior to 2020 Rev Edn                 |
| 'previous_ari'                 | ARI score of section immediately prior to 2020 Rev Edn                 |
| 'previous_dale-chall'          | DC Score of section immediately prior to 2020 Rev Edn                  |
| 'previous_sentence_count'      | Number of sentences of section immediately prior to 2020 Rev Edn       |
| 'previous_lexicon_count'       | Number of words of section immediately prior to 2020 Rev Edn           |
| 'current'                      | Content of section as of 2020 Rev Edn                                  |
| 'current_link'                 | Link to SSO of section as of 2020 Rev Edn                              | 
| 'current_len'                  | Length / No of characters of section as of 2020 Rev Edn                |
| 'current_gunning_fog'          | FOG score of section as of 2020 Rev Edn                                |
| 'current_ari'                  | ARI score of section as of 2020 Rev Edn                                |
| 'current_sentence_count'       | Number of sentences of section as of 2020 Rev Edn                      |
| 'current_lexicon_count'        | Number of words of section as of 2020 Rev Edn                          |
| 'current_dale-chall'           | DC score of section as of 2020 Rev Edn                                 |
| 'current_flesch_reading_ease'  | FRE score of section as of 2020 Rev Edn                                |
| 'url'                          | Link to section explorer page for this section                         |
| 'index'                        | Index to the data comprises of the Act Name and Section number         | 

## License

MIT License Copyright (c) 2022 Ang Hou Fu