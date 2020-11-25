import json

from functions.advent.calendar import build_advent_calendar
from functions.advent.google_sheets import get_sheet_data, parse_to_shape
from functions.advent.request import should_show_preview, wants_html


def handler(event, context):
    advent_data = get_sheet_data(parse_to_shape)

    show_all_dates = should_show_preview(event)
    if show_all_dates:
        print("showing all dates, handler")

    if wants_html(event):
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": build_advent_calendar(advent_data, show_all=show_all_dates),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/json"},
        "body": json.dumps(advent_data, show_all=show_all_dates),
    }
