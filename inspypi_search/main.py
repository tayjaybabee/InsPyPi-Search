"""

File: /main.py
Project: InsPyPi-Search
Description: 

Created: 11/6/22 - 21:47:32

"""
# region Imports

from inspyre_toolbox.humanize import Numerical

from inspypi_search.cli.arguments import Arguments
from inspypi_search.utils.data import pack_table
from inspypi_search.utils.search import search_cmd as search

# endregion

# region Argument Parsing
arguments = Arguments()
ARGS = arguments.parse()
# endregion


# region Main Function

def main():
    # print(ARGS)
    print(f'Starting search for {ARGS.query}')
    results = search(ARGS.query, )
    parsed_results = results.formatted_results
    print(parsed_results)
    # Parsing the results into a dictionary.
    # res_dict = parse_to_dict(parsed_results)
    # print(res_dict)
    parsed_table = pack_table(results.formatted_results)
    for line in parsed_table:
        line = ' | '.join(line)
        line = line.replace('| False | None | None', '')
        print(line)

    num_results = Numerical(results.result_count, noun='result')

    print(f"Found {num_results.count_noun()}")

    return results

# endregion


# region Command-line entry point

if __name__ == '__main__':
    res = main()

# endregion
