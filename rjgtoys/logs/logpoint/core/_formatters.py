"""

Library of :class:`LogPoint` formatters

"""

from contextlib import contextmanager
import string
import re

from ._actions import LogAction, LogActionList


class FormatterActionList(LogActionList):

    @contextmanager
    def use_wrapper(self, m):
        with self.use_before((WrapMessage(m),)):
            yield

StringFormatters = FormatterActionList()

ReprFormatters = FormatterActionList()


class MsgFormatter(string.Formatter):

    def __init__(self):
        super(MsgFormatter, self).__init__()
        self.missed = set()

    def get_value(self, key, args, kwargs):

        try:
            return super(MsgFormatter, self).get_value(key, args, kwargs)
        except:
            pass
        self.missed.add(key)
        return '{%s}' % (key)


class WrapMessage(LogAction):

    """
    Wraps the message of any logpoints it handles
    in another message.

    This can be used to include more fields in
    the message but can also convert to other
    formats such as HTML or XML
    """

    _target = re.compile(r"{message}")

    def __init__(self, wrapper):
        super(WrapMessage, self).__init__()
        self.wrapper = wrapper

    def act(self, lpt):
        lpt.text = self._target.sub(lpt.text, self.wrapper)


def string_by_formatting(lpt):
    fmt = MsgFormatter()
    msg = fmt.vformat(lpt.text, (), lpt.dict())

    if fmt.missed:
        raise Exception("missing parameters: %s" %
                        (",".join(list(fmt.missed))))

    lpt._string = msg


def repr_by_kwargs(lpt):
    params = ",".join("%s=%r" % (k, v)
                      for (k, v) in lpt.__dict__.items()
                        if not k.startswith('_'))

    lpt._repr = "%s(%s)" % (lpt.__class__.__name__, params)

StringFormatters.append(string_by_formatting)

ReprFormatters.append(repr_by_kwargs)
