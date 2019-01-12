import requests
import StringIO

def parse_url(ics_url):
    """Download calendar from URL and parse. Return a Calendar object."""
    ics_data = requests.get(ics_url).text
    return parse(None, StringIO.StringIO(ics_data))

def parse(component, fp):
    key = None
    value = None
    for line in fp:
        # might need to remove \r\n
        line = line.rstrip()
        if line.startswith(' '):
            # remove the first space and append to the previous value
            value += line.replace(' ', '', 1)
        else:
            property_line = line.split(':')
            key = property_line[0]
            value = ''.join(property_line[1:])
        if key == 'BEGIN':
            name = value
            if component is None:
                component = parse({'type': name}, fp)
            else:
                plural_name = '{0}s'.format(name)
                subcomponent = parse({'type': name}, fp)
                component[plural_name] = component.get(plural_name, [])
                component[plural_name].append(subcomponent)
        elif key == 'END':
            return component
        else:
            component[key] = value
    return component

