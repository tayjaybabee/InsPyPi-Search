"""

File: inspypi_search/webapp/Home.py
Project: InsPyPi-Search
Description: 

Created: 11/6/22 - 21:49:29

"""
import streamlit as st
from pandas import DataFrame

# from streamlit_searchbox import st_searchbox
from inspypi_search.utils.data import HEADERS
from inspypi_search.utils.data import pack_table
from inspypi_search.utils.search import search_cmd as search

res = None

if 'search_config' in st.session_state.keys():
    session_search_config = st.session_state['search_config']
else:
    st.session_state['search_config'] = {
        'exact_match': False,
        'save_history': True,
        'theme': 'dark'
    }


def search_pypi(query) -> list[str]:
    res = search(query)
    parsed = res.formatted_results
    table = pack_table(parsed)

    return table


with st.form('Search') as f:
    _query = st.text_input('Query')

    submitted = st.form_submit_button('Submit')

    if submitted:
        with st.spinner('Searching...') as sp:
            res = search_pypi(_query)
            st.write(res)
            st.success('Search complete!')
        st.dataframe(DataFrame(res, columns=HEADERS))

# selected = st_searchbox(
#    search_pypi,
#
# $)

# def run(query, exact_match=st.session_state.search_config.exact_match):
#     try:
#         hist = st.session_state.query_history
#     except NameError:
#         st.session_state.query_history = []
#         hist = st.session_state.query_history
#     hist.append(query)
#
#     result_table = search(query, 'table')
#
#     return result_table


# col1, col2, col3 = st.columns(3)
#
# with col1:
#     exact_match_checkbox = st.checkbox('Exact Match', key='opt_exact_match', on_change=st.session_state)
#
# with col2:
#     txt_in = st.text_input(
#         'Search Query 👇'
#     )
#
#     if txt_in:
#         st.write(f"You entered: {txt_in}")
#
# with col3:
#     st.button('Search', on_click=run, args=[txt_in])
