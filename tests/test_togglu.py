#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import io
import sys
import os

from .context import togglu
from togglu import togglu

import mountepy
import port_for

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestCLI(unittest.TestCase):

    def test_required_arguments(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            togglu.CLI()
        except BaseException as err:

            expected_output = 'usage: togglu.py [-h] [--toggl-url TOGGL_URL] [--reports-url REPORTS_URL]\n                 (--workspaces | --days-worked)\ntogglu.py: error: one of the arguments --workspaces --days-worked is required\n'
            self.assertEqual(actual_output.getvalue(), expected_output)

            pass
        finally:
            sys.stdout = sys.__stderr__

class TestDaysWorking(unittest.TestCase):

    @patch('togglu.togglu.reports', side_effect=[
            {
                'total_count': 3,
                'per_page': 1,
                'data': [
                    {'start': '2018-12-05T13:18:29+01:00'}
                ]
            },
            {
                'total_count': 3,
                'per_page': 1,
                'data': [
                    {'start': '2018-12-05T08:55:26+01:00'}
                ]
            },
            {
                'total_count': 3,
                'per_page': 1,
                'data': [
                    {'start': '2018-12-04T13:36:06+01:00'}
                ]
            }
        ])
    def test_calculate(self, reports):
        actual_days_worked = togglu.DaysWorked.calculate()
        self.assertEqual(actual_days_worked, 2)

    def test_calculate_per_page(self):

        time_entries = [
            { 'start': '2018-12-06T14:57:18+01:00' },
            { 'start': '2018-12-05T13:18:29+01:00' },
            { 'start': '2018-12-05T08:55:26+01:00' },
            { 'start': '2018-12-04T20:25:24+01:00' },
            { 'start': '2018-12-04T20:09:09+01:00' },
            { 'start': '2018-12-04T13:36:06+01:00' }
        ]
        (actual_days_worked, _) = togglu.DaysWorked.calculate_per_page(time_entries)
        self.assertEqual(actual_days_worked, 3)


class TestTogglU(unittest.TestCase):

    def test_workspaces(self):
        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output

            with open(os.path.join(THIS_DIR, os.pardir,'tests/workspaces.json'), 'r') as myfile:
                data = myfile.read().replace('\n', '')

            with mountepy.Mountebank() as mb:
                imposter = mb.add_imposter_simple(path='/workspaces', response=data)
                stub_url = 'http://localhost:{}'.format(imposter.port)

                cli = togglu.CLI(['--toggl-url', stub_url, '--workspaces'])
                cli.execute()

                expected_output = "1234567:workspace 1\n2345678:workspace 2\n3456789:workspace 3\n\n"
                self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__

    def test_daysworked(self):
        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output

            with open(os.path.join(THIS_DIR, os.pardir,'tests/days_worked1.json'), 'r') as myfile:
                data1 = myfile.read().replace('\n', '')
            with open(os.path.join(THIS_DIR, os.pardir,'tests/days_worked2.json'), 'r') as myfile:
                data2 = myfile.read().replace('\n', '')
            with open(os.path.join(THIS_DIR, os.pardir,'tests/days_worked3.json'), 'r') as myfile:
                data3 = myfile.read().replace('\n', '')

            with mountepy.Mountebank() as mb:
                imposter = mb.add_imposter({
                    'protocol': 'http',
                    'port': port_for.select_random(),
                    'stubs': [
                        {
                            'predicates': [
                                {
                                    'equals': {
                                        'method': 'GET',
                                        'path': '/details'
                                    }
                                }
                            ],
                            'responses': [
                                {
                                    'is': {
                                        'statusCode': 200,
                                        'headers': {'Content-Type': 'application/json'},
                                        'body': data1
                                    }
                                },
                                {
                                    'is': {
                                        'statusCode': 200,
                                        'headers': {'Content-Type': 'application/json'},
                                        'body': data2
                                    }
                                },
                                {
                                    'is': {
                                        'statusCode': 200,
                                        'headers': {'Content-Type': 'application/json'},
                                        'body': data3
                                    }
                                }
                            ]
                        }
                    ]
                })

                stub_url = 'http://localhost:{}'.format(imposter.port)

                cli = togglu.CLI(['--reports-url', stub_url, '--days-worked'])
                cli.execute()

                expected_output = "4\n"
                self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__



