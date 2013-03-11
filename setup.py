"""
Turtle/N3 and SPARQL syntax highlighting for Pygments.
"""
from setuptools import setup
entry_points = """
[pygments.lexers]
n3 = swlexers:Notation3Lexer
sparql = swlexers:SparqlLexer
"""
setup(
    name         = 'swlexers',
    version      = '0.3',
    description  = __doc__,
    packages     = ['swlexers'],
    entry_points = entry_points
)
