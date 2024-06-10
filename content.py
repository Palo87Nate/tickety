from .models import User, Event, Ticket, Session as session
from sqlalchemy import func

about_content = """
Ever faced the hassle of having to wait in line to get a ticket to a concert? Or even worse, after waiting
for long, the tickets get sold out before you could get one?
That is why Tickety is here, we ensure conter goers, or really any event goers, have access tickets from the
comfort of their homes,while
providing a platform for event organisers to easily share their events with a wide range of potential
attendees.
"""

about_snippet = about_content[:350] + "..."

top_events = (
        session.query(Event)
        .join(Ticket, Event.id == Ticket.event_id)
        .group_by(Event.id)
        .order_by(func.count(Ticket.id).desc())
        .limit(3)
        .all()
    )