"Subselects a fasta file based on a list of identifiers"
import sys, argparse, re
from Bio import SeqIO

def run(args):
	ids=(args.ids.read().split())
	goodrecords = []
	for record in SeqIO.parse(args.fasta[0], "fasta"):
		toprint = False
		for i in ids:
			if i in record.description:
				toprint = True
		if toprint:
			goodrecords.append(record)
	if args.c:
		for seq in goodrecords:
			print("{0}\t{1}".format(seq.description,len(seq.seq)))
	else:
		SeqIO.write(goodrecords,sys.stdout,"fasta")
			
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Subselects a fasta file based on a list of identifiers")
	parser.add_argument("fasta", help="fasta file", type=argparse.FileType('r'), nargs=1)
	parser.add_argument("--ids", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument("-c", action="store_true" )#lengths
	#parser.add_argument("-s","--search",action="store_true")#use a search term instead of list of ids
	args = parser.parse_args()
	run(args)
