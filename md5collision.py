#!/usr/bin/python
import hashlib
import shutil
import os
import binascii
import time



catfile = open("cat.jpg", "rb+")
dogfile = open("dog.jpg", "rb+")
if(os.path.exists("newdog.jpg")):
	os.remove("newdog.jpg")
newdogfile = open("newdog.jpg", "ab+")
shutil.copyfile("dog.jpg","newdog.jpg")
if(os.path.exists("newcat.jpg")):
	os.remove("newcat.jpg")
newcatfile = open("newcat.jpg", "ab+")
shutil.copyfile("cat.jpg","newcat.jpg")

catfile.seek(0)
print(repr(catfile.read(22)))
catfile.seek(0)
dogfile.seek(0)
print(repr(dogfile.read(22)))
dogfile.seek(0)

matching = False
num_match = 10 #This is the number of hex digits that match before matching is set true

cathash = hashlib.md5(catfile.read()).hexdigest()
catfile.seek(0)
catcomp = cathash[:num_match]
doghash = hashlib.md5(dogfile.read()).hexdigest()
dogfile.seek(0)
dogcomp = doghash[:num_match]

catAssoc = []
dogAssoc = []
catAssoc.append((catcomp,""))
dogAssoc.append((dogcomp,""))
print("Cat hash")
print(cathash)
print("dog hash")
print(doghash)
#print("Assoc")
#print(Assoc[0][0] , Assoc[1][0])



newdogread = newdogfile.read()
newcatread = newcatfile.read()
finaldogsalt = ""
finalcatsalt = ""
start_time = time.time()
i = 1
count = 0
while(matching != True):
	nonsalt = os.urandom(i)
	newdoghash = hashlib.md5(newdogread + nonsalt).hexdigest()
	dogcomp = newdoghash[:num_match]

	for ITEM in catAssoc:
		if (ITEM[0] == dogcomp):
			finaldogsalt = nonsalt
			finalcatsalt = ITEM[1]
			matching=True
	if(matching == False):
		dogAssoc.append((dogcomp,nonsalt))
		nonsalt = os.urandom(i)
		newcathash = hashlib.md5(newcatread + nonsalt).hexdigest()
		catcomp = newcathash[:num_match]
		
		for ITEM in dogAssoc:
			if (ITEM[0] == catcomp):
				finaldogsalt = ITEM[1]
				finalcatsalt = nonsalt
				matching=True
		if(matching == False):
			catAssoc.append((catcomp,nonsalt))
	count = count +1;
	print(count)
	if (count > 2**(i*7)):
		print("adding byte at %s seconds ---" % (time.time() - start_time))
		i = i+1
		count = 0
		

newdogfile.write(finaldogsalt)
newcatfile.write(finalcatsalt)
newdogfile.seek(0)
newcatfile.seek(0)
print("new dog hash")
print(hashlib.md5(newdogfile.read()).hexdigest())
print("new cat hash")
print(hashlib.md5(newcatfile.read()).hexdigest())
print("--- %s seconds ---" % (time.time() - start_time))
catfile.close()
dogfile.close()
newdogfile.close()
newcatfile.close()