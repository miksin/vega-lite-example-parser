import re
import json

SPEC_MARK = """{{ spec }}"""

def replace_url(spec_obj):
    if not spec_obj.has_key('data'):
        return
    if not spec_obj['data'].has_key('url'):
        return

    path = spec_obj['data'].pop('url', None)
    with open(path, 'rb') as p:
        values = json.load(p)
        spec_obj['data'][u'values'] = values


def apply_template(spec, template, output):
    with open(spec, 'rb') as s, open(template, 'rb') as t, open(output, 'wb') as o:
        spec_obj = json.load(s)
        replace_url(spec_obj)
        template_str = t.read().replace(SPEC_MARK, json.dumps(spec_obj))
        o.write(template_str)

def main():
    from sys import argv

    if len(argv) < 3:
        print 'Usage: python {} <spec-file> <template-file>'.format(argv[0])
        exit(1)

    spec = argv[1]
    template = argv[2]

    try:
        output = re.match(r'^.*?([^/]*)\.json$', spec).group(1) + '.html'
    except AttributeError:
        output = 'out.html'

    apply_template(spec, template, output)

if __name__ == '__main__':
    main()
