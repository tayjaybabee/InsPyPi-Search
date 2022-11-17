"""

File: inspypi_search/utils/history.py
Project: InsPyPi-Search
Description: 

Created: 11/11/22 - 08:37:53

"""


class History:
    __contents = {}

    #def __new__(cls):
    #    if not hasattr(cls, 'instance'):
    #        cls.instance = super(History, cls).__new__(cls)

    #    return cls.instance

    def __init__(self):
        pass

    def __call__(self):
        return self

    class Entry:
        __template = {
                'request': {
                        'interface': '',
                        'timestamp': '',
                        'query': '',
                        'options': {
                                'max_results': '',
                                'exact_match_required': '',
                                'timeout': '',
                        }
                },
                'response': {
                        'subprocess_response': {
                                'out': '',
                                'return_code': '',
                        },
                        'time_to_resolve': '',
                        'number_of_results': '',
                }

        }

        def __init__(self):
            pass


History = History()
