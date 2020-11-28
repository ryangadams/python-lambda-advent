def should_show_preview(event):
    return (
        "queryStringParameters" in event
        and "preview" in event["queryStringParameters"]
        and event["queryStringParameters"]["preview"] == "yes"
    )


def wants_html(event):
    return (
        "headers" in event
        and "accept" in event["headers"]
        and event["headers"]["accept"].startswith("text/html")
    )


def success_response(content, content_type):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": content_type},
        "body": content,
    }
