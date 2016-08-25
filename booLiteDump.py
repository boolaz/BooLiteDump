#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------
# Name 		: booLiteDump
# Author 	: Bruno Valentin
# date 		: 25/08/2016
# Revision	: 1.0
# Purpose	: Finds & dumps SQLite databases
# ----------------------------------------------------

import os,sys,re,getopt,shutil
from sys import argv
import sqlite3 as lite
import textwrap
import struct
from genericpath import exists

reload(sys)
sys.setdefaultencoding("utf-8")

softdesc={"name":"booLiteDump",
          "version":"1.0", \
          "release":"25/08/2016", \
          "purpose":"Dumps content of non-empty SQlite tables to CSV files", \
          "link":"https://github.com/boolaz/booLitedump" }

usage_text="""USAGE: booLiteDump.py [options] src_folder dst_folder
options:
  -h, --help : help
  -c, --copy : Create copy of original SQLite databases"""

#-------------------------
class Banner(object):
    """Banner for the program"""
    def __init__(self, banner_values):
        super(Banner, self).__init__()
        self.banner_values = banner_values

    def display(self):
        print("""
****************************************************** \n\
* {0} {1} ({2}) \n\
* Author : Bruno Valentin (bruno@boolaz.com) \n\
* {3}           \n\
* Updates : {4} \n\
******************************************************\n""" \
         .format(self.banner_values['name'],self.banner_values['version'],
                 self.banner_values['release'],self.banner_values['purpose'],
                 self.banner_values['link']))

#-------------------------
def usage(usage_text):
    """Usage"""
    print usage_text+"\n"

#-------------------------
def mkdir(dirname):
	if not os.path.isdir(dirname):
		try:
			os.makedirs(dirname)
		except:
			pass

#-------------------------
def display_title(title):
	sep=''+'-' * (len(title)+6)+''
	print "{0}".format(sep)
	print "|  {0}  |".format(title)
	print "{0}".format(sep)

#-------------------------
def get_file_list(chemin):
	fichiers=[]
	for root, dirs, files in os.walk(chemin, topdown=False):
		for i in files:
			fichiers.append(os.path.join(root, i))
	return(fichiers)

#-------------------------
def is_sqlite(fichier):
	try:
		curfile=open(fichier,"rb")
		curfile.seek(0)
		header = curfile.read(16)
		if "SQLite" in header: isSQLite=True
		else: isSQLite=False
	except:
		print ("File not Found")
		exit(0)
	return(isSQLite)

#-------------------------
def sqlite_get_file_list(chemin):

	display_title("SEARCHING FOR FILES")
	fichiers=get_file_list(chemin)
	totalFiles=len(fichiers)
	print "{0} files found\n".format(totalFiles)

	display_title("SEARCHING FOR SQLITE HEADER IN FILES")
	sqliteFiles=[]
	for fichier in fichiers:
		if is_sqlite(fichier): sqliteFiles.append(fichier)
	print "{0} SQLite files found\n".format(len(sqliteFiles))
	return(sqliteFiles)

#-------------------------
def get_tables_list(database):
	tables=[]
	try:
		con = lite.connect(database)
		cursor = con.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		for table in cursor.fetchall():
			nomtable=table[0]
			sql="SELECT count(*) FROM '{0}';".format(nomtable)
			try:
				cursor.execute(sql)
				row=cursor.fetchone()
				nbrec=row[0]
			except:
				nbrec=0
			tables.append((nomtable,nbrec))
	except:
		print "{0} : invalid database".format(database)
		pass
	return tables

#-------------------------
def dump_table_data(database,tablename,path,cpt):
	con = lite.connect(database)
	debnom=re.sub('/|\.|\\\\', '_',"{0}".format(database))
	debnom=re.sub('^_', '',"{0}".format(debnom))
	#print debnom
	filename="./{0}/{1:03d}-{2}-{3}.tsv".format(path,cpt,debnom,tablename)
	exportfile=open(filename,"w")
	cursor = con.cursor()
	if tablename: #
		sql="SELECT * FROM '{0}';".format(tablename)
		cursor.execute(sql)
		fieldnames=[f[0] for f in cursor.description]
		exportfile.write("\t".join(fieldnames))
		exportfile.write('\n')
		for row in cursor.fetchall():
			exportfile.write('\t'.join(map(str, row)))
			exportfile.write('\n')

#-------------------------
def export_csv_file(filename,outdir,lines,sep):
	mkdir(outdir)
	filename=outdir + '/' + filename
	exportfile = open(filename,"w")
	exportfile.write('DB num'+sep+'DB file'+sep+'Table'+sep+'Records'+'\n')
	for line in lines:
		exportfile.write(line+'\n')
	return(filename)

#-------------------------
def remove_ascii_non_printable(chunk):
	chunk = ' '.join(chunk .split())
	return ''.join([ch for ch in chunk if (ord(ch) > 31 and ord(ch) < 34) \
	               or (ord(ch) > 34 and ord(ch) < 126)])

#-------------------------
def main(argv):

	copyfiles = False

	my_banner=Banner(softdesc)
	my_banner.display()


	# Any argument ?
	try:
		opts, args = getopt.getopt(argv, \
	        "hc", \
	        ["help","copy"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	try:
		chemin,destdir=args
	except:
		usage(usage_text)
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage(usage_text)
			sys.exit()
		elif opt in ("-c", "--copy"):
			try:
				copyfiles = True
			except:
				print "invalid parameter in --copy command"

	tablefile="tables.tsv"
	separator="\t"

	sqliteFiles=sqlite_get_file_list(chemin)

	basepath=destdir+"/booLitedump"
	originpath=destdir+"/booLitedump/origin"
	mkdir(originpath)
	tablepath=destdir+"/booLitedump/tables"
	mkdir(tablepath)

	display_title("DUMPING NON-EMPTY TABLES")
	lines=[]
	cpt=nvcpt=0
	for database in sqliteFiles:
		print database
		cpt+=1
		debnom=re.sub('^\.|/|\\\\', '_',"{0}".format(database))
		debnom=re.sub('^_', '',"{0}".format(debnom))
		if copyfiles: shutil.copy(database, "{0}/{1:03d}-{2}" \
		                          .format(originpath,cpt,debnom))

		tables=get_tables_list(database)
		for table in tables:
			nomTable,nbRec=table
			lines.append("%s\t%s\t%s\t%s" % (cpt,database,nomTable,nbRec))
			if nbRec>0:
				nvcpt+=1
				dump_table_data(database, nomTable, tablepath,cpt)
	print "Extracted tables: {0}\n".format(nvcpt)

	if 'tablefile' in locals() and tablefile<>'':
		display_title("CREATING SUMMARY...")
		try:
			nomcsv=export_csv_file(tablefile, basepath, lines, \
			                       separator)
			print "Created file : {0}".format(nomcsv)
		except:
			print "Error occured while generating file"
			sys.exit(2)
	else:
		for line in lines:
			print "{0}".fomat(line)
	print "\n"

#-------------------------
if __name__ == "__main__":
	main(sys.argv[1:])
