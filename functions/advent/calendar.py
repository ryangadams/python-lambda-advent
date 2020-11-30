import pathlib
from datetime import datetime
from string import Template

import inflect


def build_advent_calendar(advent_data, show_all):
    with open(pathlib.Path(__file__).parent.absolute() / "calendar.html") as template:
        template_object = Template(template.read())
        html = template_object.substitute(
            CALENDAR_TITLE=advent_data["title"],
            BG_IMAGE=advent_data["image"],
            WINDOW_LIST=build_window_list(advent_data),
            PANEL_LIST=build_panel_list(advent_data, show_all=show_all),
        )
    return html


def build_panel_list(calendar_data, show_all=False):
    """
    We only want to get a panel for each day up to and including today.
    If it's January we'll show the whole calendar, otherwise show none, unless it's December

    """

    today = datetime.today()
    if show_all:
        filtered_dates = calendar_data["values"]
    else:
        if 1 < today.month < 12:
            return ""

        if today.month == 12:
            filtered_dates = [
                date
                for date in calendar_data["values"]
                if int(date["day"]) <= today.day
            ]
        else:
            filtered_dates = calendar_data["values"]
    print("showing")
    print(filtered_dates)
    built_html = [build_panel(**date) for date in filtered_dates]
    return "".join(built_html)


def build_panel(day, title, image, video, comments):
    p = inflect.engine()
    current_day = p.number_to_words(day)
    panel_template = f"""<div id="{current_day}" class="panel-container">
            <div class="panel">
                <div class="inner">
                    <a class="close" href="#">Close</a>
                    <h2>{current_day.capitalize()} – {title}</h2>
                    <p>{comments}</p>
                    <div class='embed-container'>
                        <iframe id="vid-{day}" src="{video}?version=3&enablejsapi=1&autoplay=1" frameborder='0' allowfullscreen enablejsapi="1"></iframe>
                    </div>
                </div>
            </div>
        </div>"""
    return panel_template


def build_window_list(calendar_data):
    """
    here we want to print out the full list (24 days), but only add the opened
    class to dates in the past
    """
    boxes = [build_window(day) for day in range(1, 25)]
    return "".join(boxes)


def build_window(day):
    p = inflect.engine()
    today = datetime.today()
    if today.month == 1:
        is_open = True
    elif today.month < 12:
        is_open = False
    else:
        is_open = day <= today.day

    return f"""<li {'class="opened""' if is_open else ''}>
    <a href="#{p.number_to_words(day)}">{day}</a>
    </li>"""


def parse_to_shape(sheet_data):
    values = [
        {
            "day": row[0],
            "title": row[1],
            "image": row[2],
            "video": row[3],
            "comments": row[4],
        }
        for row in sheet_data["values"]
        if row[0] != "Date" and row[0] != "Meta"  # ignore first rows
    ]
    # hard coded references
    calendar_title = sheet_data["values"][0][2]
    calendar_image = sheet_data["values"][0][4]

    return {"values": values, "title": calendar_title, "image": calendar_image}
