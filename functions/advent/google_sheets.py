import os
from datetime import datetime, timedelta
from typing import Union

from apiclient import discovery

from functions.advent.calendar import parse_to_shape
from functions.advent.google_credentials import get_credentials

service = discovery.build("sheets", "v4", credentials=(get_credentials()))

spreadsheet_id = os.environ.get("SHEET_ID")
range_ = os.environ.get("SHEET_RANGE")

simple_caching_sheet_data = None
simple_caching_time: Union[datetime, None] = None
cache_time = timedelta(minutes=60)


def cache_expired_or_empty():
    if simple_caching_sheet_data is None:
        return True
    if simple_caching_time is None:
        return True
    request_time = datetime.now()
    if (request_time - simple_caching_time) >= cache_time:
        return True
    return False


def get_sheet_data(data_mapper):
    global simple_caching_sheet_data
    if cache_expired_or_empty():
        print("fetching sheet as cache expired")
        request = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_)
        )
        simple_caching_sheet_data = request.execute()
    return data_mapper(simple_caching_sheet_data)


if __name__ == "__main__":
    print(get_sheet_data(parse_to_shape))
