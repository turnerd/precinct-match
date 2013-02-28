#!/usr/bin/env python
#
# Derek Turner 2013 for NOI VIP / Election Administration team job application
#


#check presence of two input files; check that they are well formatted

#sourced: precinct_id,county,precinct_name,precinct_number,ward,polling_location_ids,source,INTERNAL_notes,,,,
#VF: vf_precinct_id,vf_precinct_county,vf_precinct_ward,vf_precinct_name,vf_precinct_code,vf_precinct_count
#matched: sourced_precinct_id,vf_precinct_id,sourced_county,vf_precinct_county,sourced_precinct_name,vf_precinct_name,
#	sourced_precinct_number,vf_precinct_code,sourced_ward,vf_precinct_ward,vf_precinct_count,polling_location_ids

import re

class Precinct:
	def __init__(self, s_precinct_id='',vf_precinct_id='',s_county='',vf_county='',s_precinct_name='',vf_precinct_name='',
	s_precinct_number='',vf_precinct_code='',s_ward='',vf_ward='',vf_precinct_count='',polling_location_ids='',source='',internal_notes=''):
		self.s_precinct_id = s_precinct_id
		self.vf_precinct_id = vf_precinct_id
		self.s_county = s_county
		self.vf_county = vf_county
		self.s_precinct_name = s_precinct_name
		self.vf_precinct_name = vf_precinct_name
		self.s_precinct_number = s_precinct_number
		self.vf_precinct_code = vf_precinct_code
		self.s_ward = s_ward
		self.vf_ward = vf_ward
		self.vf_precinct_count = vf_precinct_count
		self.polling_location_ids = polling_location_ids
		self.source = source
		self.internal_notes = internal_notes
	def copySourcedInfo(self, sp):
		self.s_precinct_id = sp.s_precinct_id
		self.s_county = sp.s_county
		self.s_precinct_name = sp.s_precinct_name
		self.s_precinct_number = sp.s_precinct_number
		self.s_ward = sp.s_ward
		self.polling_location_ids = sp.polling_location_ids
		self.source = sp.source
		self.internal_notes = sp.internal_notes
	def getCombinedInfo(self):
		return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (self.s_precinct_id,self.vf_precinct_id,self.s_county,self.vf_county,
			self.s_precinct_name,self.vf_precinct_name,self.s_precinct_number,self.vf_precinct_code,self.s_ward,self.vf_ward,
			self.vf_precinct_count,self.polling_location_ids)
	def getVFInfo(self):
		return '%s,%s,%s,%s,%s,%s\n' % (self.vf_precinct_id,self.vf_county,self.vf_ward,self.vf_precinct_name,
			self.vf_precinct_code,self.vf_precinct_count) #ordering consistent with input, although the example output file differs			
	def getSourcedInfo(self):
		return '%s,%s,%s,%s,%s,%s,%s,%s\n' % (self.s_precinct_id,self.s_county,self.s_precinct_name,self.s_precinct_number,
			self.s_ward,self.polling_location_ids,self.source,self.internal_notes) #source,internal_notes are not in example output

def countySort(precinctObj):
	if (precinctObj.vf_county != ''): return precinctObj.vf_county
	else: return precinctObj.s_county 

def precinctsStrongMatch(vp,sp):
	if (vp.vf_precinct_code == sp.s_precinct_number): return True
	if (vp.vf_precinct_code.lstrip('0') == sp.s_precinct_number.lstrip('0')): return True
	if (vp.vf_precinct_name.lower() == sp.s_precinct_name.lower()): return True
	return False
	
def precinctsWeakMatch(vp,sp):
	short_name = re.sub('[()]','',sp.s_precinct_name) #unmatched parentheses are a problem in regex pattern, so all parens are removed
	long_name = re.sub('[()]','',vp.vf_precinct_name)
	#print '\tworking with short_name(sp) %s and long_name(vp) %s (%s county)' %(short_name,long_name,vp.vf_county)
	if ((short_name == '') or (long_name == '')): return False
	#maybe add condition that short_name not be all digits
	match = re.search(short_name,long_name,re.IGNORECASE)
	if (match):
		#print 'substring name match! %s and %s (s_precinct_id %s, vf_precinct_id %s)' % (short_name, long_name, sp.s_precinct_id,vp.vf_precinct_id)
		return True
	return False
		
def main():
	sourcedPrecinctsPerCounty = {} #dictionary with key=county_name and value=LIST of Precinct objects
	vfPrecincts = [] #list of Precinct objects
	matched = []
	sourced_unmatched = []
	vf_unmatched = []
	final_vf_unmatched = []

	try: 
		sfile = open('sourced_precincts.csv', 'r')
	except IOError:
		print "The input file 'sourced_precincts.csv' must be present in the same directory as this script"
		return
	rownum = 0
	for line in sfile:
		if (rownum == 0 ): #header row
			try:
				if (not re.search("precinct_id,county,precinct_name,precinct_number,ward,polling_location_ids,source,INTERNAL_notes",line)):
					raise ValueError
			except ValueError:
				print "The input file 'sourced_precincts.csv' must begin with these headers, in order:"
				print "precinct_id,county,precinct_name,precinct_number,ward,polling_location_ids,source,INTERNAL_notes"
				return
		else: #all subsequent rows
			parts = line.split(',') #assumes no values contain commas, which is the case in sample data. if this weren't so, would use csv module
			precinctObj = Precinct(s_precinct_id=parts[0],s_county=parts[1],s_precinct_name=parts[2],s_precinct_number=parts[3],s_ward=parts[4],polling_location_ids=parts[5],source=parts[6],internal_notes=parts[7].strip())
			cnty = parts[1]
			if (cnty in sourcedPrecinctsPerCounty):
				sourcedPrecinctsPerCounty[cnty].append(precinctObj)
			else:
				sourcedPrecinctsPerCounty[cnty] = [precinctObj]
		rownum+=1		
	sfile.close()
	
	try:
		vfile = open('vf_precincts.csv', 'r')
	except IOError:
		print "The input file 'vf_precincts.csv' must be present in the same directory as this script"
		return
	rownum = 0
	for line in vfile:
		if (rownum == 0): #header row
			try:
				if (not re.search("vf_precinct_id,vf_precinct_county,vf_precinct_ward,vf_precinct_name,vf_precinct_code,vf_precinct_count",line)):
					raise ValueError
			except ValueError:
				print "The input file 'vf_precincts.csv' must begin with these headers, in order:"
				print "vf_precinct_id,vf_precinct_county,vf_precinct_ward,vf_precinct_name,vf_precinct_code,vf_precinct_count"
				return
		else: #all subsequent rows
			parts = line.split(',')
			vfPrecincts.append(Precinct(vf_precinct_id=parts[0],vf_county=parts[1],vf_ward=parts[2],vf_precinct_name=parts[3],vf_precinct_code=parts[4],vf_precinct_count=parts[5].strip()))
		rownum+=1	
	vfile.close()

	for vp in sorted(vfPrecincts,key=countySort):
	#TAKE A SINGLE VF PRECINCT
		match_found = False
		cnty = vp.vf_county
		if (cnty in sourcedPrecinctsPerCounty):
			for sp in sourcedPrecinctsPerCounty[cnty]:
			#GET A LIST OF EVERY SOURCED PRECINCT IN THAT SAME COUNTY
				#FALSELY MATCH TO MULTIPLES OF THEM
				if (precinctsStrongMatch(vp,sp)):
					vp.copySourcedInfo(sp)
					matched.append(vp)
					sourcedPrecinctsPerCounty[cnty].remove(sp) #AND FOR EACH FALSE MATCH, A POTENTIAL SOURCED PRECINCT IS LOST, AND THE TRUE VF MATCH FOR THAT ONE IS ORPHANED
					match_found = True #COULD MAKE THIS A COUNTER OF SOME KIND?
															#OR COULD DO A SECOND PASS
			if (not match_found):
				vf_unmatched.append(vp)
				#print 'now %s in vf_unmatched incl vf_precinct_id %s' % (len(vf_unmatched),vp.vf_precinct_id)
 ###SECOND PASS###
	#IF 'WEAK' FLAG
	for vp in vf_unmatched:
		cnty = vp.vf_county
		matches_to_this_vp = 0
		if (cnty in sourcedPrecinctsPerCounty):
			for sp in sourcedPrecinctsPerCounty[cnty]:
				if (precinctsWeakMatch(vp,sp)):
					matches_to_this_vp+=1
					if (matches_to_this_vp > 1):
						print "%d WEAK MATCHES! vf_precinct_name %s, 1st s_precinct_name %s, 2nd s_precinct_name %s" % (matches_to_this_vp,
							vp.vf_precinct_name, temp, sp.s_precinct_name)
					temp = sp.vf_precinct_name
			if (matches_to_this_vp == 1):
				vp.copySourcedInfo(sp)
				matched.append(vp)
				sourcedPrecinctsPerCounty[cnty].remove(sp)
			if (matches_to_this_vp == 0):
				final_vf_unmatched.append(vp)


		#handle blank final line
	
	### MATCHED ###
	fmatched = open('matched_test.csv','w')
		#update output file names to spec
	fmatched.write('sourced_precinct_id,vf_precinct_id,sourced_county,vf_precinct_county,sourced_precinct_name,vf_precinct_name,sourced_precinct_number,vf_precinct_code,sourced_ward,vf_precinct_ward,vf_precinct_count,polling_location_ids\n')
	for p in sorted(matched,key=countySort):
		fmatched.write(p.getCombinedInfo())
	fmatched.close()
	
	### VF UNMATCHED ###
	#change the list to be using final_vf_unmatched or somehow integrate the two lists of unmatched (from strong, weak)
	fvf_unmatched = open('vf_unmatched_test.csv','w')
	fvf_unmatched.write('vf_precinct_id,vf_precinct_county,vf_precinct_ward,vf_precinct_name,vf_precinct_code,vf_precinct_count\n') 
	for p in sorted(vf_unmatched,key=countySort):
		fvf_unmatched.write(p.getVFInfo())
	fvf_unmatched.close() 
	#handle zero unmatched
	
	### SOURCED UNMATCHED ###
	sourced_unmatched_counter = 0
	fs_unmatched = open('sourced_unmatched_test.csv','w')
	fs_unmatched.write('sourced_precinct_id,sourced_county,sourced_precinct_name,sourced_precinct_number,sourced_ward,polling_location_ids,source,internal_notes\n')
	for cnty in sorted(sourcedPrecinctsPerCounty.keys()):
		for p in sourcedPrecinctsPerCounty[cnty]:
			fs_unmatched.write(p.getSourcedInfo())
			sourced_unmatched_counter+=1
	fs_unmatched.close()
	
	print 'Matched %d precincts' % len(matched)
	print '%d vf precincts unmatched' % len(vf_unmatched)
	print '%d sourced precincts unmatched' % sourced_unmatched_counter

	#county names should match exactly; 
	#vf_precinct_name may contain the sourced_name (example, vf_precinct_name 'Canyon - 09' contains sourced name '9')
	#sourced_precinct_number may match vf_precinct_code except for leading zero
	
	print 'done!'




#1) adjust loop to deal with multiple matches
#2) reject weak matches when short_name is numeric
#3) test
#4) make header validation look at beginning of row


if __name__ == "__main__":
	main()