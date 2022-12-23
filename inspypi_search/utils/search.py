"""

File: inspypi_search/utils/search.py
Project: InsPyPi-Search
Description: 

Created: 11/8/22 - 20:17:23

"""
# Some imports of standard libraries
from subprocess import PIPE, Popen

from inspypi_search.__about__ import __PROG__ as PROG
from inspypi_search.utils.data import HEADERS, get_results_dataframe, pack_table, parse_to_dict
# Now some imports of our own libraries/packages
from inspypi_search.utils.resparse import ResParse

LOG_NAME = f'{PROG}.utils.search:Module'

DEFAULT_RESULT_TYPE = 'table'
""" 
The default setting for what type of results are returned from the :func:`do_search` function.

:const:`DEFAULT_RESULT_TYPE` is set by developer choice to 'table' so that the results can be easily funneled into a 
streamlit dataframe/table on the front-end. However, for the convenience of other developers or future projects using 
this code, or any other possible case, the search can be performed using this module directly and without the Streamlit 
front-end interface, and this may facilitate the need for results to be returned in different formats. Since the data 
exists in all the available formats already as a result of cleaning the data for the current front-end interface I've 
chosen to make them available by simply changing the :param:`result_type` parameter.

"""
res = None


def search_cmd(query):
    global res
    res = ResParse(Popen(
        f'pip search {query}',
        shell = True,
        stdout = PIPE,
        stderr = PIPE,
        universal_newlines = True,
        encoding = 'utf8').communicate())
    return res


# region Main search command
def do_search(query, result_type: str = None):
    """
    The do_search function takes a query string and returns a dataframe of results.
    The do_search function is the primary interface for interacting with the search engine.

    Args:
        query (str):
            Search the database

        result_type: (Optional(str)):
            The type of result you'd like returned.

            Supported types are:

                - 'raw_tuple';
                The raw output of the Popen().communicate() call-chain.

                - 'raw_utf8';
                The results straight from the command-line search output, decoded into a UTF-8 string from bytes.

                - 'cleaned_string';
                The results from the command-line search output, decoded into a UTF-8 string, then stripped of '(', ')',
                '[', ']', and finally all instances of ' - ', characters.

                - 'sorted_dict';
                The results from the command-line search output as a dictionary of results after having been converted
                from a bytestring to a UTF-8 encoded string, then cleaned of unnecessary whitespace and punctuation
                before finally being parsed and sorted into what's returned.

                - 'table';
                The aforementioned dictionary of results broken into a list of lists of strings. Each of the lists
                within the top-level list are representative of table rows, with each element representing cell values.
                The column headers come from the result dictionary's keys (except the first, which is the name of each
                package) and thus each element of each list should correspond to the placing of the header strings in
                the header list. (Default value)

                - 'dataframe';
                A pandas DataFrame containing the results. The table described above is provided as the data, and the
                :obj:`HEADERS` object is provided as the value for the :param:`columns` parameter on instantiation.


    Returns:
        Union[str, list[list[str, str, str, str], dict]
    """
    result_types = [
            'raw_tuple'
            'raw_utf8',
            'cleaned_string',
            'sorted_dict',
            'table',
            'dataframe',
    ]

    # Figure out what our result type is going to be, and fill the :var:`result_type` variable with the choice,
    if result_type is not None and isinstance(result_type, str) and result_type.lower() in result_types:
        result_type = result_type.lower()
    elif not isinstance(result_type, str):
        raise TypeError(f'result_type must be a string, not {type(result_type)}!')
    elif result_type not in result_types:
        raise ValueError(f"'result_type' must be one of {', '.join(result_types)}")
    elif result_type is None:
        result_type = DEFAULT_RESULT_TYPE

    raw_res = search_cmd(query)

    if result_type == 'raw_tuple':
        return raw_res

    _res = raw_res['raw_utf8']

    if result_type == 'raw_utf8':
        return _res

    res_lst = _res.splitlines()

    if result_type == 'raw_list':
        return res_lst

    results = parse_to_dict(res)

    if result_type == 'sorted_dict':
        return results

    result_table = pack_table(results)

    if result_type == 'table':
        return result_table

    dataframe = get_results_dataframe(result_table, HEADERS)

    if result_type == 'dataframe':
        return dataframe

    if result_type == 'all':
        return [
                res,
                results,
                result_table,
                dataframe
                ]
# endregion
