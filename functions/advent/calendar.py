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
            WINDOW_LIST=build_box_list(advent_data),
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
                        <iframe src='{video}' frameborder='0' allowfullscreen></iframe>
                    </div>
                </div>
            </div>
        </div>"""
    return panel_template


def build_box_list(calendar_data):
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
