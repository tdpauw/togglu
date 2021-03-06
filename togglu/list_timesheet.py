
from togglu.timesheet_response import TimesheetResponse, TimesheetDateEntryResponse, TimesheetClientEntryResponse


class TimesheetQuery:
    def __init__(self, workspace_id, since=None, until=None, client_id=None, tag_id=None):
        self.workspace_id = workspace_id
        self.since = since
        self.until = until
        self.client_id = client_id
        self.tag_id = tag_id


class ListTimesheet:

    def __init__(self, timesheet_service):
        self.timesheet_service = timesheet_service

    def execute(self, query):

        timesheet = self.timesheet_service.timesheet(
            query.workspace_id, query.since, query.until, query.client_id, query.tag_id
        )

        return to_timesheet_response(timesheet)


def to_timesheet_response(timesheet):
    return TimesheetResponse(
        list(
            map(to_date_entry_response, timesheet.entries.values())
        ),
        timesheet.days_worked(),
        timesheet.duration()
    )


def to_date_entry_response(timesheet_date_entry):
    return TimesheetDateEntryResponse(
        timesheet_date_entry.date, list(map(to_customer_entry_response, timesheet_date_entry.entries.values()))
    )


def to_customer_entry_response(timesheet_customer_entry):
    return TimesheetClientEntryResponse(
        timesheet_customer_entry.client_name, timesheet_customer_entry.duration
    )
