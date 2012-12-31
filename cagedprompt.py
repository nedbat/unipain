"""A python prompt in a cage, for producing prompt sessions."""

import code
import sys
import textwrap 
import locale

if sys.version_info[0] == 3:
    import io

    class Output(object):
        def __init__(self):
            self.s = io.BytesIO()

        def stream(self):
            class ObsessiveFlusher(object):
                """A hack to work around a thing in Python 3 I don't understand.

                When printing non-trivial Unicode strings, something examines
                the .encoding and then the .buffer of my stream, and writes 
                data out of order, by subverting the buffering.  I don't know
                why that is, but to fix it, whenever any attribute is examined
                on my stream, I flush it.

                """
                def __init__(self, s):
                    self.s = s

                def write(self, data):
                    self.s.write(data)

                def __getattr__(self, a):
                    self.s.flush()
                    return getattr(self.s, a)

            enc = 'ascii'  # locale.getpreferredencoding()
            self.stream = io.TextIOWrapper(io.BufferedWriter(self.s), encoding=enc, newline='\n')
            return ObsessiveFlusher(self.stream)

        def get_text(self):
            self.stream.flush()
            return self.s.getvalue().decode("ascii")

else:
    from cStringIO import StringIO
    class Output(object):
        def __init__(self):
            self.s = StringIO()

        def stream(self):
            return self.s

        def get_text(self):
            return self.s.getvalue()


class CagedPrompt(code.InteractiveConsole):
    def __init__(self):
        env = {'__name__': '__main__'}
        code.InteractiveConsole.__init__(self, env)

    def run(self, input):
        # Preferred form of input:
        #
        #   run(r"""
        #       a = "\u1234\x98"
        #       b = 12
        #       """)
        #
        if input[0] == '\n':
            input = input[1:]
        self.inlines = textwrap.dedent(input).splitlines()
        old_stdout = sys.stdout
        self.out = Output()
        sys.stdout = self.out.stream()
        self.interact("")#"Python " + sys.version.split("[")[0].strip())
        sys.stdout = old_stdout
        self.output = self.out.get_text()

    def raw_input(self, prompt):
        try:
            line = self.inlines.pop(0)
        except IndexError:
            raise EOFError
        if line or prompt == sys.ps2:
            self.write("%s%s\n" % (prompt, line))
        else:
            self.write("\n")
        return line

    def write(self, data):
        sys.stdout.write(data)

def prompt_session(input, prefix=None):
    cp = CagedPrompt()
    if prefix:
        cp.run(prefix)
    cp.run(input)
    return cp.output

if __name__ == '__main__':
    TEST_INPUT = """\
        2+2
        import random
        random.random()
        class Foo:
            pass


        f = Foo()
        f
        """

    print(prompt_session(TEST_INPUT))
