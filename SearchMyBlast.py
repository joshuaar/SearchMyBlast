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

def matchesAnIterationHitDef(iteration,regex):
	try:
		hdefs = iteration.xpath(".//Hit_def")
	except IndexError:
		return False
	hdefText = [i.text for i in hdefs]
	return len([i for i in hdefText if re.search(regex, i)]) > 0

def filterOnHits(input,regex):
	itsRoot = getIterationsRoot(input)
	its = itsRoot.getchildren()
	newits = [i for i in its if matchesAnIterationHitDef(i,regex)]
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

def run(args):
	input = etree.parse(args.input[0])
	if args.query:
		filterOnQuery(input, args.query)
	if args.hit:
		filterOnHits(input, args.hit)
	if args.seq:
		filterOnSeq(input, args.seq)
	if args.list:
		printQueryList(input)
	else:
		sys.stdout.write( etree.tostring(input,encoding="UTF-8").decode("utf-8") )
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Search a BLAST XML result for keywords or sequences")
	parser.add_argument("-q", "--query", help="Filter on query description regex")
	parser.add_argument("-t", "--hit", help="Filter on hit discription regex")
	parser.add_argument("-s", "--seq", help="Filter on query sequence regex. Only returns results which have hits and match regex")
	parser.add_argument("input", help="BLAST XML file", nargs=1)
	parser.add_argument("--xml", action="store_true", help="Output results as xml (default)")
	parser.add_argument("--list", action="store_true", help="Output results as list containing all query headers")
	args = parser.parse_args()
	print(args)	
	run(args)
