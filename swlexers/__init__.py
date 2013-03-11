# -*- coding: utf-8 -*-
"""
    pygments.lexers.sw
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for semantic web languages.

    :copyright: 2007 by Philip Cooper <philip.cooper@openvest.com>.
    :license: BSD, see LICENSE for more details.
    
    Modified and extended by Gerrit Niezen. (LICENSE file described above is missing, wasn't distributed with original file) 
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
            (r'(\s*(?:PREFIX|BASE)\s+)([\w-]*:[\w-]*)?(\s*<[^> ]*>\s*)',bygroups(Keyword,Name.Variable,Name.Namespace)),
            (r'(\s*#.*)', Comment),
            (r'(\s*)(SELECT\s*(?:DISTINCT|REDUCED)?)(\s*)',bygroups(Text, Keyword,Text), 'selectVars'),
            (r'(\s*)((?:ASK|CONSTRUCT|DESCRIBE)\s*(?:DISTINCT|REDUCED)?\s*)((?:\?[a-zA-Z0-9_-]+\s*)+|\*)(\s*)',
             bygroups(Text, Keyword,Name.Variable,Text)),
            (r'(\s*)((?:LOAD|CLEAR|DROP|CREATE)\s*(?:SILENT)?\s*)(\s*(?:GRAPH)?\s*)(\s*<[^> ]*>\s*)(;)(\s*)',
             bygroups(Text, Keyword, Keyword, Name.Attribute, Text, Text)),
            (r'(\s*)((?:ADD|MOVE|COPY)\s*(?:SILENT)?\s*)(\s*(?:GRAPH)?\s*)(\s*<[^> ]*>\s*)((?:TO)\s*)(\s*(?:GRAPH)?\s*)(\s*<[^> ]*>\s*)?(;)(\s*)',
             bygroups(Text, Keyword, Keyword, Name.Attribute, Keyword, Keyword, Name.Attribute, Text, Text)),
            (r'(\s*)((?:INSERT|DELETE)\s*(?:DATA)?)\s*',bygroups(Text, Keyword),'quaddata'),
            (r'(\s*)(CONSTRUCT)?\s*({)',bygroups(Text, Keyword,Punctuation),'graph'),
            (r'(\s*)(FROM\s*(?:NAMED)?)(\s*.*)', bygroups(Text, Keyword,Text)),
            (r'(\s*)(WHERE)?\s*({)',bygroups(Text, Keyword, Punctuation),'groupgraph'),
            (r'(\s*)(LIMIT|OFFSET)(\s*[+-]?[0-9]+)',bygroups(Text, Keyword,Literal.String)),
			(r'(ORDER BY (?:ASC|DESC)\s*)(\()\s*',bygroups(Text, Keyword,Punctuation),'bindgraph'),
            (r'(\s*)(})', bygroups(Text, Punctuation)), 
        ],
        'selectVars':[
            (r'(\s*)(\*)(\s*)',bygroups(Text,Keyword,Text), '#pop'),
            (r'(?=\s*(FROM|WHERE|GROUP|HAVING|ORDER|LIMIT|OFFSET))', Text, '#pop'),
            (r'(\s*)(\()(\s*)', bygroups(Text, Punctuation, Text), 'bindgraph'),
            include('variable'),
            (r'\n', Text),
            (r'', Text, '#pop'),
        ],
        'quaddata':[
            (r'(\s*)({)(\s*)(GRAPH)(\s*<[^> ]*>\s*)', bygroups(Text, Punctuation, Text, Keyword, Name.Attribute), 'quads'),
            (r'(\s*)({)(\s*)',bygroups(Text,Punctuation,Text), 'graph'),
            (r'', Text, '#pop'),
        ],
        'quads':[
            (r'(\s*)({)(\s*)(GRAPH)(\s*<[^> ]*>\s*)', bygroups(Text, Punctuation, Text, Keyword, Name.Attribute), '#push'),
            (r'(\s*)({)(\s*)', bygroups(Text,Punctuation,Text), 'graph'),
            (r'(\s*)(})(\s*)', bygroups(Text,Punctuation,Text), '#pop'),
        ],
        'groupgraph':[
            (r'(\s*)(UNION)(\s*)({)(\s*)', bygroups(Text, Keyword, Text, Punctuation, Text), '#push'),
            (r'(\s*)({)(\s*)',bygroups(Text, Punctuation, Text), '#push'),
            include('graph'),
            include('root'),
            (r'', Text, '#pop'),
        ],
        'graph':[
            (r'(\s*)(<[^>]*\>)', bygroups(Text, Name.Class), ('triple','predObj')),
            (r'(\s*[a-zA-Z_0-9\-]*:[a-zA-Z0-9\-_]*\s)', Name.Class, ('triple','predObj')),
            (r'(\s*\?[a-zA-Z0-9_-]*)', Name.Variable, ('triple','predObj')),            
            (r'\s*\[\]\s*', Name.Class, ('triple','predObj')),
            (r'(\s*)(FILTER)(\s*)',bygroups(Text, Keyword,Text),'filterConstraint'),
            (r'(\s*)(BIND)(\s*)(\()(\s*)',bygroups(Text, Keyword, Text, Punctuation, Text),'bindgraph'),
            (r'(\s*)(OPTIONAL)(\s*)({)',bygroups(Text, Keyword, Text, Punctuation), '#push'),
            (r'(\s*)(})(\s*)(\.)(\s*)', bygroups(Text, Punctuation, Text, Punctuation, Text), '#pop'),
            (r'(\s*)(})', bygroups(Text, Punctuation), '#pop'),
            (r'(\s*)(\.)(\s*)', bygroups(Text, Punctuation, Text), '#pop'),
        ],
        'triple' : [
            (r'(?=\s*})', Text, '#pop'),                    
            (r'(\s*)(\.)(\s*)', bygroups(Text, Punctuation, Text), '#pop'),
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
            (r'(\s*)(\))', bygroups(Text, Punctuation), '#pop'),
            include('object'),
        ],
        'object': [
            include('variable'),
            (r'\s*\[', Text, 'predObj'),
            (r'\s*<[^> ]*>', Name.Attribute),
            (r'(\s*)("""(?:.|\n)*?""")(\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', bygroups(Text, Literal.String,Text)),
            (r'\s*".*?[^\\]"(?:\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', Literal.String),
            (r'(\s*)((?:[+-])?\d+\.?\d*)(\s*)', bygroups(Text, Number, Text)),
            (r'\s*[a-zA-Z0-9\-_\:]+\s*', Name.Attribute),
            (r'(\s*)(\()', bygroups(Text, Punctuation), 'objList'),
            (r',', Punctuation),
            (r'(\s*)(;)(\s*)', bygroups(Text, Punctuation, Text), '#pop'),
            (r'(?=\])', Text, '#pop'),            
            (r'\s*(?=\.)', Text, '#pop'),
        ],
        'variable':[
            (r'(\?[a-zA-Z0-9\-_]+\s*)', Name.Variable),            
        ],
        'filterConstraint':[
            include('filterBuiltin'),
            (r'(\s*)(\()(\s*)', bygroups(Text, Punctuation, Text), 'filterExp'),
            (r'(\s*)(\.)(\s*)', bygroups(Text, Punctuation, Text), '#pop'),
        ],
        #filterBuiltin is intended to be included, not pushed
        'filterBuiltin':[
            include('aggregate'),
            (r'(str|lang|langmates|datatype|bound|iri|uri|bnode)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
            (r'(abs|ceil|floor|round)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
            (r'(strlen|ucase|lcase|encode_for_uri|contains|strstarts|strends|strbefore|strafter)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
            (r'(year|month|day|hours|minutes|seconds|timezone|tz)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
            (r'(md5|sha1|sha256|sha384|sha512)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
            (r'(if|strlang|strdt)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
            (r'(sameterm|isIRI|isURI|isBlank|isLiteral|isNumeric)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
            (r'(regex)(\s*)(\()', bygroups(Name.Builtin, Text, Punctuation), 'objList'),
        ],
        # aggregate  is intended to be included, not pushed
        'aggregate':[
            (r'(\s*)(COUNT)(\s*)(\()(\s*)(DISTINCT)?(\s*)(\*)(\s*)', 
             bygroups(Text, Keyword, Text, Punctuation, Text, Keyword, Text, Keyword, Text)),
            (r'(\s*)(COUNT|SUM|MIN|MAX|AVG|SAMPLE)(\s*)(\()(\s*)(DISTINCT)?(\s*)', 
             bygroups(Text, Keyword, Text, Punctuation, Text, Keyword, Text), 'filterExp'),
            (r'(\s*)(GROUP_CONCAT)(\s*)(\()(\s*)(DISTINCT)?(\s*)', 
             bygroups(Text, Keyword, Text, Punctuation, Text, Keyword, Text), 'groupConcatExp'),
        ],
        'groupConcatExp':[
            (r'(\s*)(;)(\s*)(SEPARATOR)(\s*)(=)(\s*)', 
             bygroups(Text, Punctuation, Text, Keyword, Text, Operator, Text), 'string'),
            include('filterExp'),
         ],
        'filterExp':[
            include('filterBuiltin'),
            (r'(\s*)(\()(\s*)', bygroups(Text, Punctuation, Text), '#push'),
            include('variable'),
            include('object'),
            (r'\s*[+*/<>=~!%&|-]+\s*', Operator),
            (r'(\s*)(\))', bygroups(Text, Punctuation), '#pop'),            
        ],
        'bindgraph':[
            (r'(\s*)(\()(\s*)', bygroups(Text, Punctuation, Text), '#push'),
            (r'\s*AS\s*', Keyword),
            (r'(\s*)(IRI)(\s*)(\()(\s*)',bygroups(Text, Keyword, Text, Punctuation, Text),'iri'),
            (r'(\s*)(\))(\s*)', bygroups(Text, Punctuation, Text), '#pop'),
            include('filterExp'),
            include('variable'),
            include('object'),
            (r'', Text, '#pop'),
        ],
        'iri':[
            include('object'),
            (r'(\s*)(\))', bygroups(Text, Punctuation), '#pop'),
        ],
        'string':[
            (r'(\s*)("""(?:.|\n)*?""")(\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', bygroups(Text,Literal.String,Text), '#pop'),
            (r'\s*".*?[^\\]"(?:\@[a-z]{2-4}|\^\^<?[a-zA-Z0-9\-\:_#/\.]*>?)?\s*', Literal.String, '#pop'),
        ],
    }
