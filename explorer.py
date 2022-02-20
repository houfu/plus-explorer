import re

import pandas as pd
import redlines
import streamlit as st

data = pd.read_csv('data.csv.gz')

st.title('PLUS Explorer')
st.sidebar.write('''
## Intro 

On 31 December 2021, the [Attorney General Chambers of Singapore completed a universal revision of 
Singapore's Acts of Parliament](https://www.agc.gov.sg/our-roles/drafter-of-laws/legislation-and-revisions).
Among other changes implemented, **"Plain English is used as much as possible"**. 
A list of the types of changes made can be found [here](https://www-agc-gov-sg-admin.cwp.sg/docs/default-source/our-roles-documents/drafter-of-laws/list-of-standard-revision-changes.pdf).

**PLUS Explorer** aims to explore the following issues: 
* What are the changes made and how do they look like in a broad spectrum of clauses?
* Do they make legislation more readable?   

In order to do this, a random selection of clauses in legislation are analysed using standard readability tests.

### Select an App below to explore PLUS. 
''')

st.sidebar.radio('Select App', ["Section Explorer", "Stat Explorer"])

# Load data

dataset = pd.read_csv("data.csv.gz")


# Section Explorer

def map_index(i):
    match = re.search(r"pr(\w*)", dataset["current_link"][i])
    return f"{dataset['act_name'][i]} Section {match.group(1) if match else ''}"


section_explorer_select_index = dataset.index.map(map_index)


def random_button_clicked():
    return random.choice(section_explorer_select_index.to_list())


with st.container():
    st.write("## Section Explorer")

    selected = st.selectbox("Select a Section to explore", section_explorer_select_index)
    section_explorer_select = section_explorer_select_index.get_loc(selected)
    if st.button("Random"):
        import random

        section_explorer_select = random.choice(range(section_explorer_select_index.size))

    st.header(section_explorer_select_index[section_explorer_select])
    st.subheader('Text comparison')
    previous, current = st.columns(2)

    previous.caption(f"Previous Text [Link]({dataset['previous_link'][section_explorer_select]})")
    previous.write(dataset['previous'][section_explorer_select])

    current.caption(f"2020 Rev Edn Text [Link]({dataset['current_link'][section_explorer_select]})")
    current.write(dataset['current'][section_explorer_select])

    st.subheader('Mark Changes')
    diff = redlines.Redlines(dataset['previous'][section_explorer_select], dataset['current'][section_explorer_select])
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
