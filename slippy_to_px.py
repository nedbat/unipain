"""Convert a Slippy presentation into a .px file."""

import lxml.html, lxml.etree
import sys

def has_class(elt, klass):
    return klass in elt.attrib['class'].split()

class XmlWriter(object):
    def __init__(self, elt):
        self.start = elt
        self.elt = elt

    def add(self, elt):
        self.elt.addnext(elt)
        self.elt = elt
        return self.elt

    def add_element(self, tag, attrs=None):
        return self.add(lxml.etree.Element(tag, attrs))

    def cleanup(self):
        self.start.getparent().remote(self.start)


def slippy_to_px(tname, fname, fout, slug):
    # Parse the template
    tmpl = lxml.etree.parse(tname)
    content = tmpl.getroot().xpath("//content")[0]

    out = XmlWriter(content)

    # Find text in the presentation
    islide = 0
    lh = lxml.html.parse(fname)
    for div in lh.getroot().cssselect("div.text, div.slide"):
        if has_class(div, "slide"):
            title = div.cssselect("h1")[0].text_content()
            if has_class(div, "title") and not has_class(div, "preztitle"):
                h1 = out.add_element("h1")
                h1.text = title
                h1.tail = "\n\n"

            fig = out.add_element(
                "figurep",
                {
                    'href': 'text/{slug}/{slug}.html#{num}'.format(slug=slug, num=islide+1),
                },
            )
            img = lxml.etree.SubElement(
                fig,
                "img",
                {
                    'src': 'text/{slug}_pix/{num:03d}.png'.format(slug=slug, num=islide),
                    'alt': title,
                    'scale': '0.5',
                },
            )
            islide += 1

        if has_class(div, "text"):
            for c in div.getchildren():
                out.add(c)

    content.getparent().remove(content)
    fout.write(lxml.etree.tostring(tmpl))

if __name__ == "__main__":
    with open(sys.argv[2], "w") as fout:
        slippy_to_px("px_template.px", sys.argv[1], fout, sys.argv[3])
