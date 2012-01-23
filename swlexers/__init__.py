# -*- coding: utf-8 -*-
"""
    pygments.lexers.sw
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for semantic web languages.

    :copyright: 2007 by Philip Cooper <philip.cooper@openvest.com>.
    :license: BSD, see LICENSE for more details.
"""

import re

from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Error, Punctuation, \
     Text, Comment, Operator, Keyword, Name, String, Number, Literal
from pygments.util import shebang_matches


__all__ = ['Notation3Lexer','SparqlLexer']


class Notation3Lexer(RegexLexer):
    """
    Lexer for the N3 / Turtle / NT
    """
    name = 'N3'
    aliases = ['n3', 'turtle']
    filenames = ['*.n3', '*.ttl', '*.NT']
    mimetypes = ['text/rdf+n3','application/x-turtle','application/n3']

    tokens = {
        'comments': [
            (r'(\s*#.*)', Comment)
        ],
        'root': [
            include('comments'),
            (r'(\s*@(?:prefix|base|keywords)\s*)(\w*:\s+)?(<[^> ]*>\s*\.\s*)',bygroups(Keyword,Name.Variable,Name.Namespace)),
            (r'\s*(<[^>]*\>)', Name.Class, ('triple','predObj')),
            (r'(\s*[a-zA-Z_:][a-zA-Z0-9\-_:]*\s)', Name.Class, ('triple','predObj')),
            (r'\s*\[\]\s*', Name.Class, ('triple','predObj')),
        ],
        'triple' : [
            (r'\s*\.\s*', Text, '#pop')
        ],
        'predObj': [
            include('comments'),
            (r'(\s*[a-zA-Z_:][a-zA-Z0-9\-_:]*\b\s*)', Operator, 'object'),
            (r'\s*(<[^>]*\>)', Operator, 'object'),
            (r'\s*\]\s*', Text, '#pop'),
            (r'(?=\s*\.\s*)', Keyword, '#pop'), 
        ],
        'objList': [
            include('comments'),
            (r'\s*\)', Text, '#pop'),
            include('object')
        ],
        'object': [
            include('comments'),
            (r'\s*\[', Text, 'predObj'),
            (r'\s*<[^> ]*>', Name.Attribute),
            (r'\s*("""(?:.|\n)*?""")(\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', bygroups(Literal.String,Text)),
            (r'\s*".*?[^\\]"(?:\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', Literal.String),
            (r'\s*[a-zA-Z0-9\-_\:]\s*', Name.Attribute),
            (r'\s*\(', Text, 'objList'),
            (r'\s*;\s*\n?', Text, '#pop'),
            (r'(?=\s*\])', Text, '#pop'),            
            (r'(?=\s*\.)', Text, '#pop'),           
        ],
    }


class SparqlLexer(RegexLexer):
    """
    Lexer for SPARQL Not Complete
    """
    name = 'SPARQL'
    aliases = ['sparql']
    filenames = ['*.sparql']
    mimetypes = ['text/x-sql']
    flags = re.IGNORECASE
    tokens = {
        'comments': [
            (r'(\s*#.*)', Comment)
        ],
        'root': [
            include('comments'),        
            (r'(\s*(?:PREFIX|BASE)\s+)(\w*:\w*)?(\s*<[^> ]*>\s*)',bygroups(Keyword,Name.Variable,Name.Namespace)),
            (r'(\s*#.*)', Comment),
            (r'((?:SELECT|ASK|CONSTRUCT|DESCRIBE)\s*(?:DISTINCT|REDUCED)?\s*)((?:\?[a-zA-Z0-9_-]+\s*)+|\*)(\s*)',bygroups(Keyword,Name.Variable,Text)),
            (r'(FROM\s*(?:NAMED)?)(\s*.*)', bygroups(Keyword,Text)),
            (r'(WHERE)?\s*({)',bygroups(Keyword,Text),'graph'),
            (r'(LIMIT|OFFSET)(\s*[+-]?[0-9]+)',bygroups(Keyword,Literal.String)),
        ],
        'graph':[
            (r'\s*(<[^>]*\>)', Name.Class, ('triple','predObj')),
            (r'(\s*[a-zA-Z_0-9\-]*:[a-zA-Z0-9\-_]*\s)', Name.Class, ('triple','predObj')),
            (r'(\s*\?[a-zA-Z0-9_-]*)', Name.Variable, ('triple','predObj')),            
            (r'\s*\[\]\s*', Name.Class, ('triple','predObj')),
            (r'\s*(FILTER\s*)((?:regex)?\()',bygroups(Keyword,Text),'filterExp'),
            (r'\s*}', Text, '#pop'),
        ],
        'triple' : [
            (r'(?=\s*})', Text, '#pop'),                    
            (r'\s*\.\s*', Text, '#pop'),
        ],
        'predObj': [
            include('comments'),
            (r'(\s*\?[a-zA-Z0-9_-]*\b\s*)', Name.Variable,'object'),            
            (r'(\s*[a-zA-Z_:][a-zA-Z0-9\-_:]*\b\s*)', Operator, 'object'),
            (r'\s*(<[^>]*\>)', Operator, 'object'),
            (r'\s*\]\s*', Text, '#pop'),
            (r'(?=\s*\.\s*)', Keyword, '#pop'), 
        ],
        'objList': [
            (r'\s*\)', Text, '#pop'),
            include('object'),
        ],
        'object': [
            include('variable'),
            (r'\s*\[', Text, 'predObj'),
            (r'\s*<[^> ]*>', Name.Attribute),
            (r'\s*("""(?:.|\n)*?""")(\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', bygroups(Literal.String,Text)),
            (r'\s*".*?[^\\]"(?:\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', Literal.String),
            (r'\s*[a-zA-Z0-9\-_\:]\s*', Name.Attribute),
            (r'\s*\(', Text, 'objList'),
            (r'\s*;\s*', Text, '#pop'),
            (r'(?=\])', Text, '#pop'),            
            (r'(?=\.)', Text, '#pop'),           
        ],
        'variable':[
            (r'(\?[a-zA-Z0-9\-_]+\s*)', Name.Variable),            
        ],
        'filterExp':[
            include('variable'),
            include('object'),
            (r'\s*[+*/<>=~!%&|-]+\s*', Operator),
            (r'\s*\)', Text, '#pop'),            
        ],

    }

