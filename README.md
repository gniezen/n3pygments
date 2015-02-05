==========
n3pygments
==========

This is a [Pygments](http://http://pygments.org/) lexer that performs syntax highlighting for:

* n3, turtle : Turtle/N3/NT (*.ttl, *.n3 and *.NT) 
* sparql : SPARQL (*.sparql)

Make sure you're running Pygments 1.7 or higher and run

    sudo python setup.py install
    
to install and e.g.

    pygmentize -l turtle filename.ttl

to run Pygments.

This is mostly code from [Openvest](http://www.openvest.com/trac/wiki/n3SyntaxHighlighting#Pygments) which seems to be abandoned. The original instructions on that site only works when using `pygmentize` from the command-line. This implementation registers the package as a proper Pygments plugin which you can use from within Python, e.g.:

    from pygments.lexers import (get_lexer_by_name,get_lexer_for_filename)
    get_lexer_by_name("turtle")

should return `<pygments.lexers.Notation3Lexer>`. 

n3pygments was created based on [this answer](http://tex.stackexchange.com/a/14929/8419) on the TeX StackExchange site. So yes, you can use it to perform using syntax highlighting on your code in LaTeX using [Minted](http://code.google.com/p/minted/). I have also used it with success to perform syntax highlighting on an [Octopress 2.0](http://octopress.org) blog.

Thanks go out to [Raphaël Pinson](http://www.raphink.info) and [Philip Cooper](http://Openvest.com).     
