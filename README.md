SearchMyBlast
=============

simple command line keyword search for XML formatted blast results


##Purpose

   Are you tired of waiting for Blast2GO to finish mapping GO terms to your BLAST results?  
   Are you just interested in a few key genes that probably are already labeled the description headers of your BLAST result?  
   Then SearchMyBlast may be for you. This program enables you to filter your blast results based on the following fields:  

* Query header: 
 * return query sequences with description lines matching a specific keyword or regular expression
* Hit headers:
 * return query sequences having hits against proteins with description lines matching a specific keyword or regular expression
 * multiple arguments combine as a boolean AND query, returning description lines matching all arguments
* Sequences:
 * return only query sequences matching a specific regular expression

The output shares the same format as the input BLAST results, so it can be used in any downstream analysis (Blast2GO, enrichment, etc.)

##Installation
requires lxml, python3 and pip

    pip install lxml
    git clone https://github.com/joshuaar/SearchMyBlast
    cd SearchMyBlast

to run:

    python SearchMyBlast.py ...

To execute as a command:

    echo "python $PWD/SearchMyBlast.py $@" > /usr/local/bin/SearchMyBlast
    chmod +x /usr/local/bin/SearchMyBlast
    
then execute:

    SearchMyBlast ...
    
    
##Usage
The interface is pretty simple:

    usage: SearchMyBlast.py [-h] [-q QUERY] [-t HIT] [-s SEQ] [--xml] [--list] input

The script provides three ways to search your blast results in addition to e-value filtering. You can filter BLAST results using either the query sequence headers, th hit sequence headers, or the query sequence iteslf.
    
* -t : search hit headers
* -q : search query headers
* -s : search seq headers
* -e : filter on minimum e value

EXAMPLE:

    python SearchMyBlast.py -q "isotig1.*" -t "Olfactory|olfactory" -s "AVHAD" -e 0.001 --xml myBlastFile.xml

The above returns all blast results from sequences labeled isotig1.* that align with olfactory proteins, contain the sequence AVHAD and have an e-value of less thatn 0.001.
You can mix and match search terms however you like. You do not have to specify all three search fields.

Results are returned by defult as BLAST XML. You can use the --list parameter to output as a list of query sequences.
