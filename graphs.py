from urllib.parse import urlencode

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='PLUS Explorer - Graphs',
    page_icon='📊',
    menu_items={
        'About': """
        Read the [blog post](https://www.lovelawrobots.com/evaluating-legislation-for-readability-exploring-plus/).
        """
    }
)

st.title('PLUS Explorer - Graphs')

with st.expander('Introduction'):
    st.write("""
    On 31 December 2021, the [Attorney General Chambers of Singapore completed a universal revision of 
Singapore's Acts of Parliament](https://www.agc.gov.sg/our-roles/drafter-of-laws/legislation-and-revisions).
Among other changes implemented, **"Plain English is used as much as possible"**. 
A list of the types of changes made can be found [here](https://www-agc-gov-sg-admin.cwp.sg/docs/default-source/our-roles-documents/drafter-of-laws/list-of-standard-revision-changes.pdf).

Read the [blog post](https://www.lovelawrobots.com/evaluating-legislation-for-readability-exploring-plus/) on this project.


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


@st.cache
def get_url(index: str):
    return 'https://share.streamlit.io/houfu/plus-explorer/main/explorer.py?' + urlencode({'section': index})


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

    score_display.altair_chart(heatmap)

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

    fre_view = dataset[
        ['current_flesch_reading_ease', 'previous_flesch_reading_ease', 'current_lexicon_count', 'url']].reset_index()

    fre_view['diff'] = fre_view.index.map(
        lambda x: fre_view["current_flesch_reading_ease"][x] - fre_view['previous_flesch_reading_ease'][x])

    base = alt.Chart(fre_view)

    heatmap = base.mark_circle(size=100).encode(
        x=alt.X('current_lexicon_count', title='2020 Word Count'),
        y=alt.Y('diff', title='Change in FRE', sort='-y'),
        color=alt.Color('diff', scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, domainMin=-10, domainMax=10)),
        tooltip=['index', "current_flesch_reading_ease", "diff"],
        href='url:N'
    ).properties(
        width=800,
        height=800
    )

    positive_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='5'
    )
    negative_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='-5'
    )

    score_display.header('Change in FRE')

    score_display.altair_chart(positive_line + negative_line + heatmap)

    score_display.write('Red horizontal rules at Change of FRE = \u00B1 5 to show small changes.')

    bars = base.mark_bar().encode(
        x2=alt.X2('previous_flesch_reading_ease', title='Previous FRE'),
        x=alt.X('current_flesch_reading_ease', title='2020 FRE'),
        y=alt.Y('index', sort="-x", title='Section', axis=alt.Axis(labels=False)),
        color=alt.Color('diff', scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, domainMin=-10, domainMax=10),
                        title='Change in FRE'),
        tooltip=['index', "current_flesch_reading_ease", "diff"],
        href='url:N'
    ).properties(
        height=1200,
        width=800
    )

    G10_line = base.mark_rule(color='red', opacity=0.3).encode(
        x='x:Q',
    ).transform_calculate(
        x='50'
    )
    Pro_line = base.mark_rule(color='red', opacity=0.3).encode(
        x='x:Q',
    ).transform_calculate(
        x='10'
    )

    line = base.mark_line().encode(
        x=alt.X('current_flesch_reading_ease', title='2020 FRE'),
        y=alt.Y('index', sort="-x", title='Section', axis=alt.Axis(labels=False)),
    )

    score_display.header('FRE Scores of each Section (ordered)')

    score_display.altair_chart(bars + G10_line + Pro_line + line)

    score_display.write("""
    Red vertical rule at FRE = 60 to show ninth grade level.
    Red vertical rule at FRE = 10 to show professional reading level.
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

    fog_view = dataset[['current_gunning_fog', 'previous_gunning_fog', 'current_lexicon_count', 'url']] \
        .reset_index()

    fog_view['diff'] = fog_view.index.map(
        lambda x: fog_view["current_gunning_fog"][x] - fog_view['previous_gunning_fog'][x])

    base = alt.Chart(fog_view)

    heatmap = base.mark_circle(size=100).encode(
        x=alt.X('current_lexicon_count', title='2020 Word Count'),
        y=alt.Y('diff', title='Change in FOG', sort='descending'),
        color=alt.Color('diff', scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, domainMin=-2, domainMax=2,
                                                reverse=True)),
        tooltip=['index', "current_gunning_fog", "diff"],
        href='url:N'
    ).properties(
        width=800,
        height=800
    )

    positive_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='0.5'
    )
    negative_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='-0.5'
    )

    score_display.header('Changes in FOG Index')

    score_display.altair_chart(positive_line + negative_line + heatmap)

    score_display.write('Red horizontal rules at Change of FRE = \u00B1 0.5 to show small changes.')

    bars = base.mark_bar().encode(
        x2=alt.X2('previous_gunning_fog', title='Previous FOG'),
        x=alt.X('current_gunning_fog', title='2020 FOG'),
        y=alt.Y('index', sort="x", title='Section', axis=alt.Axis(labels=False)),
        color=alt.Color('diff',
                        scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, domainMin=-2, domainMax=2, reverse=True),
                        title='Change in FOG'),
        tooltip=['index', "current_gunning_fog", "diff"],
        href='url:N'
    ).properties(
        height=1200,
        width=800
    )

    Pro_line = base.mark_rule(color='red', opacity=0.3).encode(
        x='x:Q'
    ).transform_calculate(
        x='12'
    )

    line = base.mark_line().encode(
        x=alt.X('current_gunning_fog', title='2020 FOG'),
        y=alt.Y('index', sort="x", title='Section', axis=alt.Axis(labels=False)),
    )

    score_display.header("FOG Index for each section (Ordered)")

    score_display.altair_chart(Pro_line + bars + line)

    score_display.write("Red vertical rule at FOG = 12 to show documents for a general audience.")

if selected == "Automated Readability Index":
    score_intro.write("""
    ### Automated Readability Index
    
    Using the number of words per sentence and the number of characters per word,
    outputs the readability of the text in terms of US Grade Level
    (roughly number of years of formal schooling).
    [[Wiki]](https://en.wikipedia.org/wiki/Automated_readability_index) 

    The higher the score, the less readable.

    """)

    ari_view = dataset[['current_ari', 'previous_ari', 'current_lexicon_count', 'url']] \
        .reset_index()

    ari_view['diff'] = ari_view.index.map(
        lambda x: ari_view["current_ari"][x] - ari_view['previous_ari'][x])

    base = alt.Chart(ari_view)

    heatmap = base.mark_circle(size=100).encode(
        x=alt.X('current_lexicon_count', title='2020 Word Count'),
        y=alt.Y('diff', title='Change in ARI', sort='descending'),
        color=alt.Color('diff', scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, domainMin=-2, domainMax=2,
                                                reverse=True)),
        tooltip=['index', "current_ari", "diff"],
        href='url:N'
    ).properties(
        width=800,
        height=800
    )

    positive_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='0.5'
    )
    negative_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='-0.5'
    )

    score_display.header('Changes in Automated Readability Index')

    score_display.altair_chart(positive_line + negative_line + heatmap)

    score_display.write('Red horizontal rules at Change of ARI = \u00B1 0.5 to show small changes.')

    bars = base.mark_bar().encode(
        x2=alt.X2('previous_ari', title='Previous ARI'),
        x=alt.X('current_ari', title='2020 ARI'),
        y=alt.Y('index', sort="x", title='Section', axis=alt.Axis(labels=False)),
        color=alt.Color('diff',
                        scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, domainMin=-2, domainMax=2, reverse=True),
                        title='Change in ARI'),
        tooltip=['index', "current_ari", "diff"],
        href='url:N'
    ).properties(
        height=1200,
        width=800
    )

    G10_line = base.mark_rule(color='red', opacity=0.3).encode(
        x='x:Q',
    ).transform_calculate(
        x='10'
    )

    line = base.mark_line().encode(
        x=alt.X('current_ari', title='2020 ARI'),
        y=alt.Y('index', sort="x", title='Section', axis=alt.Axis(labels=False)),
    )

    score_display.header("Automated Readability Index for each section (Ordered)")
    score_display.altair_chart(G10_line + bars + line)
    score_display.write("Red vertical rule at ARI = 10 to show Grade 10 / Secondary School readability.")

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

    dc_view = dataset[['current_dale-chall', 'previous_dale-chall', 'current_lexicon_count', 'url']] \
        .reset_index()

    dc_view['diff'] = dc_view.index.map(
        lambda x: dc_view["current_dale-chall"][x] - dc_view['previous_dale-chall'][x])

    base = alt.Chart(dc_view)

    heatmap = base.mark_circle(size=100).encode(
        x=alt.X('current_lexicon_count', title='2020 Word Count'),
        y=alt.Y('diff', title='Change in DC', sort='descending'),
        color=alt.Color('diff', scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, reverse=True),
                        title='Change in DC'),
        tooltip=['index', "current_dale-chall", "diff"],
        href='url:N'
    ).properties(
        width=800,
        height=800
    )

    positive_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='0.5'
    )
    negative_line = base.mark_rule(color='red', opacity=0.3).encode(
        y='y:Q',
    ).transform_calculate(
        y='-0.5'
    )

    score_display.header('Changes in Dale-Chall Scores')
    score_display.altair_chart(positive_line + negative_line + heatmap)
    score_display.write('Red horizontal rules at Change of DC = \u00B1 0.5 to show small changes.')

    bars = base.mark_bar().encode(
        x2=alt.X2('previous_dale-chall', title='Previous DC'),
        x=alt.X('current_dale-chall', title='2020 DC'),
        y=alt.Y('index', sort="x", title='Section', axis=alt.Axis(labels=False)),
        color=alt.Color('diff',
                        scale=alt.Scale(scheme='pinkyellowgreen', domainMid=0, reverse=True),
                        title='Change in DC'),
        tooltip=['index', "current_dale-chall", "diff"],
        href='url:N'
    ).properties(
        height=1200,
        width=800
    )

    line = base.mark_line().encode(
        x=alt.X('current_dale-chall', title='2020 DC'),
        y=alt.Y('index', sort="x", title='Section', axis=alt.Axis(labels=False)),
    )

    G9_line = base.mark_rule(color='red', opacity=0.3).encode(
        x='x:Q',
    ).transform_calculate(
        x='7.0'
    )

    G14_line = base.mark_rule(color='red', opacity=0.3).encode(
        x='x:Q',
    ).transform_calculate(
        x='9.9'
    )

    score_display.header("Dale-Chall scores for each section (Ordered)")
    score_display.altair_chart(G9_line + G14_line + bars + line)
    score_display.write("""
    Red vertical rule at DC = 7 to show easily understood by a secondary 3 student.
    
    Red vertical rule at DC = 9.9 to show easily understood by college student.
    """)
