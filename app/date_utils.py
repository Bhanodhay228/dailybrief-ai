def format_published_date(published_at):

    if not published_at:
        return "Publication date unavailable"

    return published_at.strftime(
        "%A, %d %B %Y • %I:%M %p"
    )