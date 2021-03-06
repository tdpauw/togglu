
import unittest
import io
import sys

from .context import togglu
from togglu import togglu


class TestCLI(unittest.TestCase):

    def test_required_subcommand(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI()
            cli.execute()

        except SystemExit:
            expected_output = \
                'usage: togglu [-h] [--config CONFIG] [--toggl-url TOGGL_URL]\n' \
                '              [--reports-url REPORTS_URL]\n' \
                '              {workspaces,timesheet} ...\n' \
                'togglu: error: the following arguments are required: subcommand\n'

            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stderr = sys.__stderr__

    def test_required_arguments_for_timesheet(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI(['timesheet'])
            cli.execute()

        except SystemExit:
            expected_output = \
                'usage: togglu timesheet [-h] --workspace-id WORKSPACE_ID [--since SINCE]\n' \
                '                        [--until UNTIL] [--client-id CLIENT_ID]\n' \
                '                        [--tag-id TAG_ID]\n' \
                'togglu timesheet: error: the following arguments are required: --workspace-id\n'

            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stderr = sys.__stderr__
