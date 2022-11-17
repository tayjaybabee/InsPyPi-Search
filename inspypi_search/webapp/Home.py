"""

File: inspypi_search/webapp/Home.py
Project: InsPyPi-Search
Description: 

Created: 11/6/22 - 21:49:29

"""
import streamlit as st
from streamlit_searchbox import st_searchbox

from inspypi_search.utils.search import do_search as search

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
    res = search(query, 'table')
    return res.package_list



selected = st_searchbox(
    search_pypi,

)

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
