#!/usr/bin/python
import simplejson as json
import codecs
import os
import bz2
from optparse import OptionParser

def parseTweet(jsondata):
	try:
		dict = json.loads(jsondata)

		if 'text' in dict.keys():

			""" gets some attributes from tweet
          		createdAt
          		username(screen_name)
          		tweet text
          		we could get other attibutes like:
          		id
          		timestamp
          		username(name)
          		...
      		"""
			createdAt = dict['created_at']
			screenName = dict['user']['screen_name']
			tweetText = dict['text'].replace('\n',' ').replace('\t',' ').replace('\r',' ')

			output = '%s\t\t%s\t\t%s' % (createdAt, screenName, tweetText)
			print output.encode('utf8') 

	except:
		None
		print "fail"

def parseDir(inputDir):

	total = 0

	for path, subdirs, files in os.walk(inputDir):

		for archive in files:

			filepath = os.path.join(path, archive)

			if archive.endswith(".json.bz2"):
				total += parseFile_bz2(filepath ,archive)          
			elif archive.endswith(".json"):
				total += parseFile_json(filepath ,archive)  

	print "Total of parsed tweets: %d" % (total)

def parseFile(inputFile):

	try:
		logFileHandle = codecs.open(inputFile, 'r', 'utf-8')
	
		if inputFile.endswith(".json"):
			parseFile_json(inputFile, inputFile)
		elif inputFile.endswith(".json.bz2"):
			parseFile_bz2(inputFile, inputFile)	
	except:
		print "Error: the file doesn`t exists or the type of the file is not json or bz2."
  
def parseFile_bz2(filepath, archive):
	
	count = 0

	with bz2.BZ2File(filepath,'r') as fin:
		for line in fin:
			parseTweet(str(line).decode('utf-8'))
			count += 1

	print "*%s: parsed | %d tweets*" % (archive, count)         
	print '-----------------------------------------------------------------------'    

	return count

def parseFile_json(filepath, archive):

	count = 0

	logFileHandle = codecs.open(filepath, 'r', 'utf-8')
	for line in file(filepath):
		parseTweet(line)
		count += 1
	print "*%s: parsed | %d tweets*" % (archive, count)    
	print '-----------------------------------------------------------------------'

	return count

if __name__ == '__main__':

	# The program gives options to the user.   
	parser = OptionParser()
	parser.add_option("-d", "--directory", dest="dir",
					  help="Directory containing all files", metavar="FOLDER")
	parser.add_option("-f", "--file", dest="file",
					  help="A single file", metavar="FILE")

	(options, args) = parser.parse_args()

	inputFile = options.file
	inputDir = options.dir

	if inputDir == None:
		parseFile(inputFile)
	else:
		parseDir(inputDir)
