import altair as alt
import pandas as pd
import streamlit as st

st.title('PLUS Explorer - Graphs')

with st.expander('Introduction'):
    st.write("""
    On 31 December 2021, the [Attorney General Chambers of Singapore completed a universal revision of 
Singapore's Acts of Parliament](https://www.agc.gov.sg/our-roles/drafter-of-laws/legislation-and-revisions).
Among other changes implemented, **"Plain English is used as much as possible"**. 
A list of the types of changes made can be found [here](https://www-agc-gov-sg-admin.cwp.sg/docs/default-source/our-roles-documents/drafter-of-laws/list-of-standard-revision-changes.pdf).

Let's visualise how much the changes affected readability using common readability tests.
    
To do this, we bunch up a selection of random clauses so that we can see two things:
* Whether the change improved or worsened the readability of the section. 
    * A Red circle represents the original readability score.
    * A Blue circle represents the new readability score.
    * A red line between them shows the change worsened the readability score.
    * A blue line between them shows the change improved the readability score.
* How much the change improved or worsened the readability of the section.
    * This is shown by the distance between the circle.


_A note on the selection of sections_

I manually and randomly selected 150 sections from Statutes Singapore Online and picked the latest 2020 Rev Edn version
and compared it with the _immediately preceding_ version. 

By random, 
I mean that I went through a list of legislation, 
picked one that seems interesting 
and then picked a section which sounded interesting, 
keeping in mind that I would like a variety of clauses in the dataset. 
Some sections experienced _no changes at all_, 
I left them inside the dataset as it was important to show that not all sections are affected by changes. 
  
    """)

# Load data

dataset = pd.read_csv("data.csv.gz", index_col=0)

# Readability Score selector

st.write("## Select a readability score")

selected = st.selectbox("Readability Score",
                        ["Flesch Reading Ease", "Gunning FOG", "Automated Readability Index", "Dale-Chall",
                         "Word Count"])

# Containers to (1) Introduce score, (2) display graph
score_intro = st.container()
score_display = st.container()

if selected == "Word Count":
    score_intro.write("""
    ### Word Count
    
    The number of words in the section. 
    Note that the wordier a section is, it is harder to read.
    However small changes to the number of words alone is neutral IMO.
    """)

    word_count_view = dataset[["previous_lexicon_count", "current_lexicon_count"]].reset_index()
    word_count_view['diff'] = word_count_view.index.map(
        lambda x: word_count_view["current_lexicon_count"][x] - word_count_view['previous_lexicon_count'][x])

    base = alt.Chart(word_count_view)

    heatmap = base.mark_rect().encode(
        x=alt.X('current_lexicon_count:O', title='2020 Word Count', bin=alt.BinParams(step=100)),
        y=alt.Y('diff:O', title='Change in Word Count'),
        color="count()"
    )

    st.altair_chart(heatmap)

if selected == "Flesch Reading Ease":
    score_intro.write("""
    ### Flesch reading ease
    
    Using word length and sentence length,
    outputs the readability of the text.
    [[Wiki]](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch_reading_ease) 

    The higher, the more easy to read:
    * Score of 60: 9th Grade level. Some jurisdiction mandate this score for readability of legal documents.
    * Score of 10 to 30: Reading level of a University graduates. 
    * Score of less than 10: Reading level of a professional
    * Negative scores are possible under the formula.
    """)

if selected == "Gunning FOG":
    score_intro.write("""
    ### Gunning Fog index
    
    Using the number of complex words per sentence and words per sentence,
    outputs the readability of the text in terms of US Grade Level
    (roughly number of years of formal schooling).
    [[Wiki]](https://en.wikipedia.org/wiki/Gunning_fog_index) 

    The higher the score, the less readable. 
    Texts for a wide audience generally need a fog index less than 12. 
    Texts requiring near-universal understanding generally need an index less than 8. 

    """)

if selected == "Automated Readability Index":
    score_intro.write("""
    ### Automated Readability Index
    
    Using the number of words per sentence and the number of characters per word,
    outputs the readability of the text in terms of US Grade Level
    (roughly number of years of formal schooling).
    [[Wiki]](https://en.wikipedia.org/wiki/Automated_readability_index) 

    The higher the score, the less readable.

    """)

if selected == "Dale-Chall":
    score_intro.write("""
    ### Dale-Chall Readability Score
    
    The Dale–Chall readability formula is a readability test 
    that provides a numeric gauge of the comprehension difficulty 
    that readers come upon when reading a text. 
    It uses a list of 3000 words that groups of fourth-grade American students 
    could reliably understand, considering any word not on that list to be difficult.
    [[Wiki]](https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula) 
    
    The higher the score, the less readable.
    Scores of 9 to 9.9 are considered easily understood by an average 13th to 15th-grade (college) student.
    """)
