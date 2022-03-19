import pandas as pd
import streamlit as st
from redlines import Redlines

st.title('PLUS Explorer')
with st.expander('Introduction'):
    st.write('''
On 31 December 2021, the [Attorney General Chambers of Singapore completed a universal revision of 
Singapore's Acts of Parliament](https://www.agc.gov.sg/our-roles/drafter-of-laws/legislation-and-revisions).
Among other changes implemented, **"Plain English is used as much as possible"**. 
A list of the types of changes made can be found 
[here](https://www-agc-gov-sg-admin.cwp.sg/docs/default-source/our-roles-documents/drafter-of-laws/list-of-standard-revision-changes.pdf).

**PLUS Explorer** aims to explore the following issues: 
* What are the changes made and how do they look like in a broad spectrum of clauses?
* Do they make legislation more readable?   

In order to do this, a random selection of clauses in legislation are analysed using common readability tests.

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

''')

# Load data

dataset = pd.read_csv("data.csv.gz", index_col=0)


# Section Explorer

def random_button_clicked():
    return random.choice(dataset.index.to_list())


def on_select():
    st.experimental_set_query_params(section=st.session_state.selectbox)


with st.container():
    st.write("## Section Explorer")

    selected = st.selectbox("Select a Section to explore", dataset.index, on_change=on_select, key='selectbox')
    section_explorer_select = dataset.index.get_loc(selected)
    st.write(f'Total number of records: {dataset.index.size}')
    if st.button("Random"):
        import random

        random_select = random.choice(range(dataset.index.size))
        st.experimental_set_query_params(section=dataset.index[random_select])

    query_params = st.experimental_get_query_params()
    if "section" in query_params:
        section_explorer_select = query_params.get("section")[0]
    else:
        section_explorer_select = 'Civil Law Act 1909 Section 6'

    st.header(section_explorer_select)
    st.subheader('Mark Changes')
    diff = Redlines(dataset['previous'][section_explorer_select], dataset['current'][section_explorer_select])
    st.markdown(diff.output_markdown, unsafe_allow_html=True)
    st.caption("**NB:** If there are no marked changes, the text is the same.")

    st.subheader('Readability Statistics')
    flesch, fog, ari = st.columns(3)
    flesch.metric("Flesch Reading Ease", dataset["current_flesch_kincaid_grade"][section_explorer_select],
                  dataset["current_flesch_kincaid_grade"][section_explorer_select] -
                  dataset["previous_flesch_reading_ease"][section_explorer_select])
    fog.metric("Fog Scale", dataset["current_gunning_fog"][section_explorer_select],
               dataset["current_gunning_fog"][section_explorer_select] -
               dataset["previous_gunning_fog"][section_explorer_select], delta_color="inverse")
    ari.metric("Automated Readability Index", dataset["current_ari"][section_explorer_select],
               dataset["current_ari"][section_explorer_select] -
               dataset["previous_ari"][section_explorer_select], delta_color="inverse")
    dale, _, _ = st.columns(3)
    dale.metric("Dale-Chall Readability Score", dataset["current_dale-chall"][section_explorer_select],
                dataset["current_dale-chall"][section_explorer_select] -
                dataset["previous_dale-chall"][section_explorer_select], delta_color="inverse")
    length, words, sentences = st.columns(3)
    length.metric("Length of Section (Characters)", dataset["current_len"][section_explorer_select],
                  dataset["current_len"][section_explorer_select] -
                  dataset["previous_len"][section_explorer_select], delta_color="off")
    sentences.metric("No of Sentences", dataset["current_sentence_count"][section_explorer_select],
                     dataset["current_sentence_count"][section_explorer_select] -
                     dataset["previous_sentence_count"][section_explorer_select], delta_color="off")
    words.metric("No of Words", dataset["current_lexicon_count"][section_explorer_select],
                 dataset["current_lexicon_count"][section_explorer_select] -
                 dataset["previous_lexicon_count"][section_explorer_select], delta_color="off")

    st.subheader('Text comparison')
    previous, current = st.columns(2)

    previous.caption(f"Previous Text [Link]({dataset['previous_link'][section_explorer_select]})")
    previous.write(dataset['previous'][section_explorer_select])

    current.caption(f"2020 Rev Edn Text [Link]({dataset['current_link'][section_explorer_select]})")
    current.write(dataset['current'][section_explorer_select])
