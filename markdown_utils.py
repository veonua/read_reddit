from markdown import Markdown
from io import StringIO


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()

    if element.tag in ['table', 'thead']:
        element.text = ""
        element.tail = ""

    if element.tag in ['tr']:
        element.text = ""

    if element.tag in ['th', 'td']:
        element.tail = "\t"

    if element.text:
        stream.write(element.text)

    # veon: keep urls
    if element.tag == 'a':
        stream.write(" " + element.attrib['href'] + " ")

    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(" " + element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain", extensions=['tables'])
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)
