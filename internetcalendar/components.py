import logging
import requests
import StringIO
from unidecode import unidecode

logging.basicConfig()
logger = logging.getLogger('internetcalendar')

def set_log_level(level=logging.INFO):
    logger.setLevel(level)

def parse_url(ics_url):
    """Download calendar from URL and parse. Return a Calendar object."""
    ics_data = requests.get(ics_url).text
    component, last_line = parse(StringIO.StringIO(ics_data))
    return component

def parse_file(filename):
    """Open a calendar file and parse. Return a Calendar object."""
    component, last_line = parse(open(filename, 'r'))
    return component

def parse(fp, component=None, last_line=None):
    """Return a component of an iCalendar and the last line of fp, since this
    function is used recursively."""
    log = logger.getChild('parse')
    for current_line in fp:
        current_line = current_line.rstrip()
        log.debug('last_line: {0}'.format(unidecode(last_line or u'')))
        log.info('current_line: {0}'.format(unidecode(current_line or u'')))
        if last_line is None:
            # keep track of last line in case we need to unfold the next line
            last_line = current_line
        elif current_line.startswith(' '):
            # unfold the line: remove first space and append to last line
            log.info('unfold current line')
            last_line += current_line.replace(' ', '', 1)
        elif last_line.startswith('BEGIN'):
            # new component or subcomponent
            _, name = last_line.split(':', 1)
            if component is None:
                log.info('create Component {0}'.format(name))
                component, last_line = parse(fp, {'type': name}, current_line)
            else:
                log.info('create subcomponent {0}'.format(name))
                subcomponent, last_line = parse(fp, {'type': name}, current_line)
                if name.startswith('V'):
                    plural_name = '{0}s'.format(name).replace('V', '', 1).lower()
                    log.info('add {0} {1}'.format(component['type'], plural_name))
                    component[plural_name] = component.get(plural_name, [])
                    component[plural_name].append(subcomponent)
                else:
                    log.info('set {0} {1}'.format(component['type'], key))
                    component[name] = subcomponent
                log.info('set last_line to {0}'.format(last_line))
        else:
            key, value = last_line.split(':', 1)
            if key == 'END':
                log.info('return subcomponent {0}'.format(value))
                return component, current_line
            log.info('set {0} {1}'.format(component['type'], key))
            component[key] = value
            last_line = current_line
    return component, None

