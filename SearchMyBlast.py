from lxml import etree
import argparse
import re
import sys

def parse(input):
	return etree.parse(input)

def getIterationsRoot(input):
	itsRoot = input.xpath("//BlastOutput_iterations")[0]
	return itsRoot

def removeAllIterations(input):
	itsRoot = getIterationsRoot(input)
	its = itsRoot.getchildren()
	[itsRoot.remove(i) for i in its]
	return input

def replaceIterations(input,newIterations):
	removeAllIterations(input)
	itsRoot = getIterationsRoot(input)
	[itsRoot.append(i) for i in newIterations]
	return input

def getIterationQDef(iteration):
	qdef = iteration.xpath(".//Iteration_query-def")[0]
	return qdef.text

def filterOnQuery(input,regex):
	itsRoot = getIterationsRoot(input)
	its = itsRoot.getchildren()
	newits = [i for i in its if re.search( regex , getIterationQDef(i) )]
	replaceIterations(input,newits)

def matchesAnIterationHitDef(iteration,regexs):
	try:
		hdefs = iteration.xpath(".//Hit_def")
	except IndexError:
		return False
	hdefText = [i.text for i in hdefs]
	matchesAll = lambda string,regex: len([i for i in regex if re.search(i,string)]) == len(regex) # returns true if all regexes match a string
	return len([i for i in hdefText if matchesAll(i,regexs)]) > 0

def filterOnHits(input,regexs):
	itsRoot = getIterationsRoot(input)
	its = itsRoot.getchildren()
	newits = [i for i in its if matchesAnIterationHitDef(i,regexs)]
	replaceIterations(input,newits)

def MatchesQuerySeqWithHits(iteration,regex):
	seq = iteration.xpath(".//Hsp_qseq")
	if len(seq) == 0:
		return False
	seq = seq[0].text
	if re.search(regex, seq):
		return True
	else:
		return False
	
def filterOnSeq(input,regex):
	itsRoot = getIterationsRoot(input)	
	its = itsRoot.getchildren()
	newits = [i for i in its if matchesQuerySeqWithHits(i,regex)]
	replaceIterations(input, newits)

def printQueryList(input):
	itsRoot = getIterationsRoot(input)
	its = itsRoot.getchildren()
	for i in its:
		itstext = i.xpath("./Iteration_query-def")[0]
		print( itstext.text )

def printReadableList(input):
	itsRoot = getIterationsRoot(input)
	its = itsRoot.getchildren()
	qdef = [i.xpath("Iteration_query-def")[0].text for i in its]	
	hitsdef = [[j.text for j in i.xpath(".//Hit_def")] for i in its]
	for q,hits in zip(qdef,hitsdef):
		print ( q )
		for j in hits:
			print ( "\t"+j )

def printTopHit(input):
	itsRoot = getIterationsRoot(input)
	its = itsRoot.getchildren()
	hitsdef = [[j.text for j in i.xpath(".//Hit_def")] for i in its]
	for hits in hitsdef:
		try:
			print( hits[0] )
		except IndexError:
			print( "." )

def filterOnEVal(input,minval):
	evalues = input.xpath("//Hsp_evalue")
	hits = [i.getparent().getparent().getparent() for i in evalues if float(i.text) > minval]
	rm = lambda x: x.getparent().remove(x)
	for i in hits:
		try:
			rm(i)
		except AttributeError:
			pass

def run(args):
	input = etree.parse(args.input[0])
	if args.evalue:
		filterOnEVal(input, args.evalue)
	if args.query:
		filterOnQuery(input, args.query)
	if args.hit:
		filterOnHits(input, args.hit)
	if args.seq:
		filterOnSeq(input, args.seq)
	if args.list:
		printQueryList(input)
	elif args.readable:
		printReadableList(input)
	elif args.tophit:
		printTopHit(input)
	else:
		sys.stdout.write( etree.tostring(input,encoding="UTF-8").decode("utf-8") )
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Search a BLAST XML result for keywords or sequences")
	parser.add_argument("-q", "--query", help="Filter on query description regex")
	parser.add_argument("-e", "--evalue", help="Filter on min E value", type=float)
	parser.add_argument("-t", "--hit", help="Filter on hit discription regex", nargs="+")
	parser.add_argument("-s", "--seq", help="Filter on query sequence regex. Only returns results which have hits and match regex")
	parser.add_argument("input", help="BLAST XML file", nargs=1)
	parser.add_argument("--xml", action="store_true", help="Output results as xml (default)")
	parser.add_argument("--list", action="store_true", help="Output results as list containing all query headers")
	parser.add_argument("--readable", action="store_true", help="Output results as list containing readable hit descriptions")
	parser.add_argument("--tophit", action="store_true", help="Output results as list containing readable hit descriptions")
	args = parser.parse_args()
	run(args)
