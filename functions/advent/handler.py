import json

from functions.advent.calendar import build_advent_calendar, parse_to_shape

# from functions.advent.csv_sheets import get_sheet_data_csv

from functions.advent.google_sheets import get_sheet_data
from functions.advent.request import should_show_preview, wants_html, success_response


def handler(event, context):
    advent_data = get_sheet_data(parse_to_shape)

    show_all_dates = should_show_preview(event)

    if wants_html(event):
        return success_response(
            build_advent_calendar(advent_data, show_all=show_all_dates), "text/html"
        )

    return success_response(json.dumps(advent_data), "text/json")
