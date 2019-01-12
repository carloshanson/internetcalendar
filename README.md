# internetcalendar

Create a dictionary and list representation of an iCalendar.

```
import internetcalendar
ics_url = "https://calendar.google.com/calendar/ical/..."
calendar = internetcalendar.parse_url(ics_url)
from pprint import pprint
pprint(calendar['VEVENTs'][0])
```

