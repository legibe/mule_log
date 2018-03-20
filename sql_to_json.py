import re
import json

def remove_convert(s):
    # replace the CONVERT(type, date, style) calls with the date
    matches = re.findall('(CONVERT\(.*?\))', s)
    for match in matches:
        terms = [ x.strip() for x in match.split(',') ]
        s = s.replace(match, terms[1],1)
    return s

def record_to_python(data):
    u = json.loads(data['result']['_raw'])
    s = u['message']
    index = s.index('(')
    s = s[index+1:]
    index = s.index(')')
    s = s[:index]
    fields = [ x.strip() for x in s.split(',') ]
    s = u['message']
    _, s = s.split('VALUES ')
    index = s.index('(')
    s = s[index+1:]
    s = remove_convert(s)
    # remove last bracket
    s = s[:-1]
    values = [ x.strip() for x in s.split(',') ]
    d = {}
    for i in range(len(fields)-1):
        d[fields[i]] = values[i]
    last = len(fields) - 1
    if last + 1 < len(values):
        d[fields[last]] = ', '.join(values[last:])
    else:
        d[fields[last]] = values[last]
    print(json.dumps(d, indent=4))

with open('t.json') as f:
    data = json.load(f)
    record_to_python(data)
