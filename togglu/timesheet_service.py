
from togglu.timesheet import Timesheet


class TimesheetService:

    def __init__(self, report_repository):
        self.report_repository = report_repository

    def timesheet(self, workspace_id, since=None, until=None, client_id=None, tag_id=None):
        time_entries = self.report_repository.detailed_report(workspace_id, since, until, client_id, tag_id)

        timesheet = Timesheet()

        for entry in time_entries:
            timesheet.add(entry)

        return timesheet
