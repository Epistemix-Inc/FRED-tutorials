"""
    FRED lexer derived from the pygments.lexers.RegexLex class
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the FRED Modeling Language (TM).

    :copyright: Copyright 2021 by Epistemix In.c
    :license: BSD, see LICENSE for details.
"""

from sphinx.highlighting import lexers
from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, default
from pygments.token import Comment, Keyword, Literal, Name, Number, Operator, Punctuation, String, Text

__name__=['FREDLexer']

class FREDLexer(RegexLexer):
    """
    For the `FRED <http://www.epistemix.com/>`_ Modeling Language.

    .. versionadded:: 7.3
    """

    name = 'FRED'
    aliases = ['fred']
    filenames = ['*.fred', '*.fredmod']
    mimetypes = ['text/x-fred']

    builtins = {
         'default', 'then', 'next','wait', 'with',
         'locations', 'start_date', 'end_date', 'weekly_data',
         'start_state', 'meta_start_state', 'has_administrator',
         'global', 'personal', 'import', 'import_per_capita',
         'transmission_mode', 'exposed_state'}

    keywords = {
       'condition', 'include', 'parameters', 'simulation', 'state', 'variables'}

    operators = {
        '~', '+', '-', '*', '|', '^', '=', '==', '~=', '~==', '<', '<=',
        '>', '>=', '&', '|'}

    functions = {
        'if', 'foobar', 'select', 'prob', 'absent', 'present',
        'bernoulli', 'set_state', 'lognormal',
        'date_range', }

    valid_name = '\\\\?[\\w!&*<>|^$%@\\-+~?/=]+'

    def get_tokens_unprocessed(self, text):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in self.builtins:
                    yield index, Name.Builtin, value
                    continue
                if value in self.keywords:
                    yield index, Keyword, value
                    continue
                if value in self.functions:
                    yield index, Name.Builtin, value
                    continue
                if value in self.operators:
                    yield index, Operator, value
                    continue
            yield index, token, value

    tokens = {
        'root': [
            # Whitespace
            (r'\s+', Text),

            # single line comment
            (r'#.*?\n', Comment.Single),

            # lid header
            #(r'([a-z0-9-]+)(:)([ \t]*)(.*(?:\n[ \t].+)*)',
            #    bygroups(Name.Attribute, Operator, Text, String)),

            default('code')  # no header match, switch to code
        ],
        'code': [
            # Whitespace
            (r'\s+', Text),

            # single line comment
            (r'#.*?\n', Comment.Single),

            # multi-line comment
            #(r'/\*', Comment.Multiline, 'comment'),

            # strings and characters
            #(r'"', String, 'string'),
            #(r"'(\\.|\\[0-7]{1,3}|\\x[a-f0-9]{1,2}|[^\\\'\n])'", String.Char),

            # floating point
            (r'[-+]?(\d*\.\d+(e[-+]?\d+)?|\d+(\.\d*)?e[-+]?\d+)', Number.Float),

            # decimal integer
            (r'[-+]?\d+', Number.Integer),

            # Punctuation
            (r'(#\(|#\[|##|[(){}\[\],.;])', Punctuation),

            # Most operators are picked up as names and then re-flagged.
            # This one isn't valid in a name though, so we pick it up now.
            #(r':=', Operator),

            # Pick up #t / #f before we match other stuff with #.
            (r'#[tf]', Literal),

            # class names
            #('<' + valid_name + '>', Name.Class),

            # define variable forms.
            #(r'\*' + valid_name + r'\*', Name.Variable.Global),

            # define constant forms.
            #(r'\$' + valid_name, Name.Constant),

            # everything else. We re-flag some of these in the method above.
            (valid_name, Name),
        ],
        #'comment': [
        #    (r'[^*/]', Comment.Multiline),
        #    (r'/\*', Comment.Multiline, '#push'),
        #    (r'\*/', Comment.Multiline, '#pop'),
        #    (r'[*/]', Comment.Multiline)
        #],
        'keyword': [
            (r'"', String.Symbol, '#pop'),
            (r'[^\\"]+', String.Symbol),  # all other characters
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-f0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ]
    }
