from .requester import test_route
from colorama import init, Fore, Back, Style
import requests
import json
import os


def test_events(cookies={}):
    SUPER_ADMIN_MAIL = os.getenv('SUPER_ADMIN_MAIL')
    tests = [
    {'description': 'CREATE EVENT wrong keys',
                    'url': '/event/',
                    'method': 'post',
                    'data': {"na": "naaaaame", "sm_descriprion": "sm_descriprion"},
                    'valid_code': '<Response [400]>',
                    'valid_data': {'error': 'Wrong json key(s)!'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'CREATE EVENT wrong date/time',
                    'url': '/event/',
                    'method': 'post',
                    'data': {"name": "naaaaame", "sm_descriprion": "sm_descriprion",
                             "description": "description", "start_date": "10",
                             "start_time": "", "location": "location",
                             "site_link": "site_link", "additional_info": "additional_info"},
                    'valid_code': '<Response [422]>',
                    'valid_data': {'error': 'Incorrect date or time format'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'CREATE EVENT correct',
                    'url': '/event/',
                    'method': 'post',
                    'data': {"name": "naaaaame", "sm_description": "sm_descriprion",
                             "description": "description", "start_date": "2020-02-27",
                             "start_time": "23:59", "location": "location",
                             "site_link": "site_link", "additional_info": "additional_info"},
                    'valid_code': '<Response [201]>',
                    'valid_data': {'extra': '1'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET EVENT wrong id',
                    'url': '/event/10',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No event with this id'},
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'GET EVENT correct',
                    'url': '/event/1',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {},
                    'need_decision': True,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'GET EVENT correct with creator cookie',
                    'url': '/event/1',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {},
                    'need_decision': True,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'CREATE EVENT correct via non-admin',
                    'url': '/event/',
                    'method': 'post',
                    'data': {"name": "11", "sm_description": "22", "description": "33",
                             "start_date": "2222-02-27", "start_time": "23:59",
                             "location": "44", "site_link": "55", "additional_info": "66"},
                    'valid_code': '<Response [201]>',
                    'valid_data': {'extra': '2'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'UPDATE EVENT not owned',
                    'url': '/event/1',
                    'method': 'put',
                    'data': {"name": "11", "sm_description": "22", "description": "33",
                             "start_date": "2222-02-27"},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'No rights!'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'UPDATE EVENT admin',
                    'url': '/event/2',
                    'method': 'put',
                    'data': {"name": "change", "start_date": "3333-02-27"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Successfully updated.'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET EVENT updated',
                    'url': '/event/2',
                    'method': 'get',
                    'data': {"name": "change", "start_date": "3333-02-27"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {},
                    'need_decision': True,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'UPDATE EVENT wrong keys',
                    'url': '/event/2',
                    'method': 'put',
                    'data': {"na": "changed name", "start_date": "3333-02-27"},
                    'valid_code': '<Response [400]>',
                    'valid_data': {'error': 'Wrong json key(s)!'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'UPDATE EVENT owner',
                    'url': '/event/2',
                    'method': 'put',
                    'data': {"name": "kekekekeke"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Successfully updated.'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'ALL EVENTs no query',
                    'url': '/event/all',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'ALL EVENTs wrong query',
                    'url': '/event/all?offset=5&size=10',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'ALL EVENTs correct query',
                    'url': '/event/all?offset=1&size=1',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'JOIN admin 2 viewer',
                    'url': '/event/2/join',
                    'method': 'post',
                    'data': {"role": "viewer", "report": "report",
                             "presenter_description": "presenter_description"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Successfully joined'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'JOIN wrong id',
                    'url': '/event/10/join',
                    'method': 'post',
                    'data': {"role": "viewer", "report": "report",
                             "presenter_description": "presenter_description"},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No event with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'JOIN repeat join',
                    'url': '/event/2/join',
                    'method': 'post',
                    'data': {"role": "viewer"},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'User has already joined this event as [viewer]!'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'JOIN user 1 presenter',
                    'url': '/event/1/join',
                    'method': 'post',
                    'data': {"role": "presenter", "report": "report",
                             "presenter_description": "presenter_description"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Successfully joined'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET PRESENTERS 1',
                    'url': '/event/1/presenters',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'none',
                    'get_cookie': False
    },
    {'description': 'GET PRESENTERS 2',
                    'url': '/event/2/presenters',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': False,
                    'cookie': 'none',
                    'get_cookie': False
    },
    ]

    i = 0
    code_passed = 0
    data_passed = 0

    if not hasattr(cookies, 'admin'):
        data = {
            "email": SUPER_ADMIN_MAIL,
            "password": "1234"
        }
        answer = requests.post('http://127.0.0.1:{}/login'.format(os.getenv('PORT')), data=json.dumps(data), headers={'Content-type': 'application/json'})
        cookies['admin'] = answer.cookies
    if not hasattr(cookies, 'user'):
        data = {
            "email": "mail@mail",
            "name": "Name",
            "surname": "Surname",
            "password": "1234"
        }
        answer = requests.post('http://127.0.0.1:{}/register'.format(os.getenv('PORT')), data=json.dumps(data), headers={'Content-type': 'application/json'})
        data = {
            "email": "mail@mail",
            "password": "1234"
        }
        answer = requests.post('http://127.0.0.1:{}/login'.format(os.getenv('PORT')), data=json.dumps(data), headers={'Content-type': 'application/json'})
        cookies['user'] = answer.cookies
    if not hasattr(cookies, 'none'):
        cookies['none'] = ''
        

    print(Fore.BLACK + Back.WHITE + '==========================( TESTS EVENTS )=========================' + Style.RESET_ALL)
    print()

    for test in tests:
        if test['get_cookie']:
            i, code_passed, data_passed, cookies[test['to_cookie']] = test_route(i, code_passed, data_passed,
                                                                    test['description'],
                                                                    test['url'],
                                                                    test['method'],
                                                                    test['data'],
                                                                    test['valid_code'],
                                                                    test['valid_data'],
                                                                    test['need_decision'],
                                                                    cookies[test['cookie']],
                                                                    test['get_cookie']
            )
        else:
            i, code_passed, data_passed = test_route(i, code_passed, data_passed,
                                                                    test['description'],
                                                                    test['url'],
                                                                    test['method'],
                                                                    test['data'],
                                                                    test['valid_code'],
                                                                    test['valid_data'],
                                                                    test['need_decision'],
                                                                    cookies[test['cookie']],
                                                                    test['get_cookie']
            )


    print(Fore.BLACK + Back.WHITE + '=====================( TESTS EVENTS FINISHED )=====================' + Style.RESET_ALL)
    print('TESTS: ' + str(i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - data_passed) + Style.RESET_ALL)
    print()

    return i, code_passed, data_passed, cookies
