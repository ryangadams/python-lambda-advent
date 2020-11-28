import pathlib


def get_sheet_data_csv(data_mapper):
    import csv

    with open(
        pathlib.Path(__file__).parent / "calendar-data.csv", newline=""
    ) as csvfile:
        calendar_data = csv.reader(csvfile, delimiter=",", quotechar='"')
        rows = list(calendar_data)
    sheet_shaped_response = {
        "range": "Sheet1!A1:E1000",
        "majorDimension": "ROWS",
        "values": rows,
    }
    return data_mapper(sheet_shaped_response)
