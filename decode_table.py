import sys
import cog

def show_decode(b, encoding):
    empty = "".encode(encoding)
    u = b.decode(encoding)
    b_parsed = []
    for c in u:
        c_encoded = c.encode(encoding)
        if c_encoded.startswith(empty):
            c_encoded = c_encoded[len(empty):]
        b_parsed.append(c_encoded)
    return b_parsed, u

def output_row(bytes, encoding, labels):
    cog.out("<tr class='chars'>")
    if labels:
        cog.out("<td class='label'>{0}</td>".format(encoding))
    for b, c in zip(*show_decode(bytes, encoding)):
        if len(b) > 1:
            span = " colspan='{0}'".format(len(b))
        else:
            span = ""
        cog.out("<td{0}>&#x{1:x};</td>".format(span, ord(c)))
    cog.out("</tr>\n")

def output_table(bytes, encodings, labels=True):
    cog.out("<table class='decode_table'>\n")
    cog.out("<tr class='bytes'>")
    if labels:
        cog.out("<td class='label'>&nbsp;</td>")
    for b in bytes:
        cog.out("<td>{0:2x}</td>".format(ord(b)))
    cog.out("</tr>\n")

    for encoding in encodings:
        output_row(bytes, encoding, labels=labels)

    cog.out("</table>\n")
