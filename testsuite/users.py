from .requester import test_route
from colorama import init, Fore, Back, Style
import requests
import json
import os


def test_users(cookies={}):
    SUPER_ADMIN_MAIL = os.getenv('SUPER_ADMIN_MAIL')
    tests = [
    {'description': 'GET CURRENT USER INFO',
                    'url': '/user/',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'bio': None, 'birth': None, 'country': None, 'email': SUPER_ADMIN_MAIL, 'name': 'Super', 'organization': None, 'phone': None, 'position': None, 'service_status': 'superadmin', 'surname': 'Admin', 'town': None},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'PUT CURRENT USER email or password failed',
                    'url': '/user/',
                    'method': 'put',
                    'data': {"email": "mail@mail", "password": "1234", "name": "kek"},
                    'valid_code': '<Response [400]>',
                    'valid_data': {'error': 'Wrong json key(s)!'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'PUT CURRENT USER correct',
                    'url': '/user/',
                    'method': 'put',
                    'data': {"name": "kek", "phone": "88005553535"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Profile info successfully updated.'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER INFO updated',
                    'url': '/user/',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'bio': None, 'birth': None, 'country': None, 'email': SUPER_ADMIN_MAIL, 'name': 'kek', 'organization': None, 'phone': '88005553535', 'position': None, 'service_status': 'superadmin', 'surname': 'Admin', 'town': None},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS with incorrect role',
                    'url': '/user/events/kek',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'Unknown route!'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS admin creator',
                    'url': '/user/events/creator',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS admin manager',
                    'url': '/user/events/manager',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS admin paresenter',
                    'url': '/user/events/presenter',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS admin viewer',
                    'url': '/user/events/viewer',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS user creator',
                    'url': '/user/events/creator',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS user manager',
                    'url': '/user/events/manager',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS user paresenter',
                    'url': '/user/events/presenter',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET CURRENT USER EVENTS user viewer',
                    'url': '/user/events/viewer',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET ALL USERS non-admin',
                    'url': '/user/all',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'No rights!'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET ALL USERS admin',
                    'url': '/user/all',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET USER INFO non-admin',
                    'url': '/user/1',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'AccessError - No rights.'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET USER INFO admin',
                    'url': '/user/2',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {},
                    'need_decision': True,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET USER INFO admin not found',
                    'url': '/user/20',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No user with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET USER EVENTS presenter admin not found',
                    'url': '/user/10/events/presenter',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No user with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET USER EVENTS presenter admin',
                    'url': '/user/2/events/presenter',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [],
                    'need_decision': True,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'GET USER EVENTS presenter non-admin',
                    'url': '/user/2/events/presenter',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'AccessError - No rights.'},
                    'need_decision': False,
                    'cookie': 'user',
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


    print(Fore.BLACK + Back.WHITE + '==========================( TESTS USERS )==========================' + Style.RESET_ALL)
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

    print(Fore.BLACK + Back.WHITE + '======================( TESTS USERS FINISHED )=====================' + Style.RESET_ALL)
    print('TESTS: ' + str(i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - data_passed) + Style.RESET_ALL)
    print()

    return i, code_passed, data_passed, cookies
