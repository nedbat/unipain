# Helpers for cogging slides.

import cog
import cagedprompt
import sys
import textwrap

def quote_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def include_file(fname, highlight=None, start=None, end=None, section=None, klass=None):
    """Include a text file.

    `fname` is read as text, and included in a <pre> tag.
    
    `highlight` is a list of lines to highlight.
    
    `start` and `end` are the first and last line numbers to show, if provided.

    `section` is a named section.  If provided, a marked section in the file is extracted
    for display.  Markers for section foobar are "(((foobar))" and "(((end)))".

    """
    if fname.endswith(".py"):
        pre_class = "language-python"
    else:
        pre_class = "language-plain"
    if highlight:
        pre_class += "; highlight: %r" % (highlight,)
    text = open(fname).read()
    lines = text.split("\n")
    if section:
        assert start is None
        assert end is None
        start_marker = "(((%s)))" % section
        end_marker = "(((end)))"
        start = next(i for i,l in enumerate(lines, 1) if start_marker in l)
        end = next(i for i,l in enumerate(lines[start:], start+1) if end_marker in l)
        start += 1
        end -= 1
    else:
        if start is None:
            start = 1
        if end is None:
            end = len(lines)+1
    lines = lines[start-1:end]

    if start != 1:
        pre_class += "; first-line: %d" % start
    if klass:
        pre_class += "; class-name: %s" % klass

    pre_lines(lines, pre_class)

def if_version(ver, fn, *args):
    if sys.version_info[0] == ver:
        fn(*args)
    else:
        cog.out(cog.previous)

def prompt_session(ver, in1, in2=None):
    if_version(ver, _prompt_session, ver, in1, in2)

def _prompt_session(ver, in1, in2=None):
    if in2:
        prefix, input = in1, in2
    else:
        prefix, input = None, in1
    output = cagedprompt.prompt_session(input, prefix)
    cog.outl("<div class='version-marker'>%s</div>" % ver)
    pre_lines(output.strip().split("\n"), "language-python language-python-%d" % ver)

def wrap_lines(lines, width=65, indent=10):
    for line in lines:
        if line.startswith('  File '):
            # A line in a traceback, skip it for clarity.
            continue
        if 'Error' in line:     # Special wrapping for error lines.
            wrapped = textwrap.wrap(line, width=65, subsequent_indent=' '*indent, break_long_words=False)
            for l in wrapped or [""]:
                yield l
        else:
            yield line

def pre_lines(lines, pre_class=None):
    cog.outl("<pre%s>" % (" class='%s'" % pre_class if pre_class else ""))
    for line in wrap_lines(lines):
        if line:
            line = quote_html(line)
            klass = "line"
        else:
            line = "&nbsp;"
            klass = "blankline"     # So that lineselect can skip it.
        cog.outl("<span class='%s'>%s</span>" % (klass, line))
    cog.outl("</pre>")

def pre(text):
    if text[0] == '\n':
        text = text[1:]
    pre_lines(textwrap.dedent(text).splitlines())
