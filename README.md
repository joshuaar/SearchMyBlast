SearchMyBlast
=============

simple command line keyword search for XML formatted blast results


##Purpose

Are you tired of taking days to filter your NGS results with GO terms? Are you just interested in a few key words that a simple blast search could reveal? Then SearchMyBlast may be for you. This program enables you to filter your blast results based on the following fields:

* Query header: return query sequences who's header matches a specific keyword or regular expression
* Hit headers: return query sequences that have hits against proteins matching a specific keyword or regular expression
* Sequences: return only query sequences matching a specific regular expression

Results are either formatted as a list or XML. The output shares the same format as the input BLAST results, so it can be used in any downstream analysis (Blast2GO, etc.)

##Installation
requires lxml, python3 and pip

    pip install lxml
    git clone https://github.com/joshuaar/SearchMyBlast
    cd SearchMyBlast
    python SearchMyBlast.py ...
    
    
##Usage
The interface is pretty simple:

    usage: SearchMyBlast.py [-h] [-q QUERY] [-t HIT] [-s SEQ] [--xml] [--list] input
    
* -t : search hit headers
* -q : search query headers
* -s : search seq headers

EXAMPLE:

    python SearchMyBlast.py -q "isotig\.1.*" -t "Olfactory|olfactory" -s "AVHAD" myBlastFile.xml
    
The above returns all blast results from isotigs1.... that align with olfactory proteins and contain the sequence AVHAD.
You can mix and match search terms however you like. You do not have to specify all three search fields.

Results are returned by defult as BLAST XML. You can use the --list parameter to output as a list of query sequences.
