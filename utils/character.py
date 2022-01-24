from typing import Any
import six
from krysalid.utils.iteration import drop_while


ESCAPE_CHARACTERS = ('\n', '\t', '\r')

HTML5_WHITESPACE = ' \t\n\r\x0c'



def convert_to_unicode(value: Any, encoding='utf-8', errors='strict'):
    """
    Return the unicode representation of a bytes object `text`.
    If the value is already a text, return it.
    """
    if isinstance(value, six.text_type):
        return value

    if not isinstance(value, (bytes, six.text_type)):
        raise TypeError(f'Value must be of type bytes, str or unicode. Got {type(value)}')

    return value.decode(encoding, errors)



def replace_escape_chars(value: str, replace_by: Any = u'', encoding: str = None):
    """
    Replaces/removes the escape characters that are often found
    in strings retrieved from the internet. They are replaced
    by default ''
    """
    text = convert_to_unicode(value)
    for escape_char in ESCAPE_CHARACTERS:
        text = text.replace(
            escape_char, convert_to_unicode(replace_by, encoding))
    return text


def strip_white_space(text: str):
    """
    Strips the leading and trailing white space
    from a string. This does not affect space within
    an the string e.g. Kendall\rJenner, the \\r will
    not be affected

    Parameters
    ----------

        text (str): value to correct
    """
    return text.strip(HTML5_WHITESPACE)


def deep_clean(value: str):
    """
    Special helper for cleaning words that have a
    special characters between them and for which the 
    normal `replace_escape_chars` does not modify
    """
    value = replace_escape_chars(strip_white_space(value), replace_by=' ')
    cleaned_words = drop_while(lambda x: x == '', value.split(' '))
    return ' '.join(cleaned_words)
