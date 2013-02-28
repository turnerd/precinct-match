#!/usr/bin/env python
#
# Derek Turner 2013 for NOI VIP / Election Administration team
#

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
			self.vf_precinct_code,self.vf_precinct_count) 
			#using order consistent with input file, although the example output file differs			
	def getSourcedInfo(self):
		return '%s,%s,%s,%s,%s,%s,%s,%s\n' % (self.s_precinct_id,self.s_county,self.s_precinct_name,self.s_precinct_number,
			self.s_ward,self.polling_location_ids,self.source,self.internal_notes) 
			#source,internal_notes are not in example output but retained here for utility

### This is a helper function to allow the sorting of a list of Precinct objects by their county names
def countySort(precinctObj):
	if (precinctObj.vf_county != ''): return precinctObj.vf_county
	else: return precinctObj.s_county 

### This function contains the logic for matches that are highly confident--they must have the same county, 
### plus either a match on code and number (dropping leading zeros since these are stored as strings) 
### or a match on name, provided the names aren't blank.
def precinctsStrongMatch(vp,sp):
	if ((vp.vf_precinct_code == '') and (sp.sp_precinct_number == '')):
			print "code and number can't both be blank"
			return False
	if (vp.vf_precinct_code == sp.s_precinct_number): return True
	if (vp.vf_precinct_code.lstrip('0') == sp.s_precinct_number.lstrip('0')): return True
	if ((vp.vf_precinct_name == '') or (sp.s_precinct_name == '')): return False
	if (vp.vf_precinct_name.lower() == sp.s_precinct_name.lower()): return True
	return False

### This function contains the logic for matches that are somewhat less confident. These matches are rejected (in the logic of the 
### second pass) if multiple possible match combinations are found for any one precinct. 
### Since the sourced name is often a shorter version of the voterfile name, we term these the 'short_name' and the 'long_name' and 
### check to see if the short_name is a substring of the long one.  Names that contain only numbers are not allowed to be matched
### this way since they are very likely to create false positives.
def precinctsWeakMatch(vp,sp):
	short_name = re.sub('[()]','',sp.s_precinct_name) #unmatched parentheses are a problem in regex pattern, so all parens are removed
	long_name = re.sub('[()]','',vp.vf_precinct_name)
	if ((short_name == '') or (long_name == '')): return False
	if (not re.search(r'[a-zA-Z]',short_name)):
		#print "s_precinct_id %s has a name containing only numbers (%s)--insufficient to do a substring match" % (sp.s_precinct_id,short_name)
		return False
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

### READ SOURCED DATA ###
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
				print "The input file 'sourced_precincts.csv' must have these headers, in order:"
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

### READ VOTERFILE DATA ###
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
				print "The input file 'vf_precincts.csv' must have these headers, in order:"
				print "vf_precinct_id,vf_precinct_county,vf_precinct_ward,vf_precinct_name,vf_precinct_code,vf_precinct_count"
				return
		else: #all subsequent rows
			parts = line.split(',')
			vfPrecincts.append(Precinct(vf_precinct_id=parts[0],vf_county=parts[1],vf_ward=parts[2],vf_precinct_name=parts[3],vf_precinct_code=parts[4],vf_precinct_count=parts[5].strip()))
		rownum+=1	
	vfile.close()

### FIRST PASS: STRONG MATCH ###
	for vp in sorted(vfPrecincts,key=countySort):
		strong_matches_to_vp = 0
		cnty = vp.vf_county
		if (cnty in sourcedPrecinctsPerCounty):
			for sp in sourcedPrecinctsPerCounty[cnty]:
				if (precinctsStrongMatch(vp,sp)):
					vp.copySourcedInfo(sp)
					matched.append(vp)
					sourcedPrecinctsPerCounty[cnty].remove(sp)
					strong_matches_to_vp+=1
			if (strong_matches_to_vp == 0):
				vf_unmatched.append(vp)
			assert strong_matches_to_vp <= 1, "vf_precinct_id %s has matched to more than one sourced precinct on name or code alone"
				#assert checks for an unexpected condition that would indicate a false positive, and therefore prints to stderr
		else: vf_unmatched.append(vp) #this is for cases where there are no sourced precincts with a matching county

### SECOND PASS: WEAK MATCH ###
	for vp in vf_unmatched:
		cnty = vp.vf_county
		weak_matches_to_vp = 0
		if (cnty in sourcedPrecinctsPerCounty):
			for sp in sourcedPrecinctsPerCounty[cnty]:
				if (precinctsWeakMatch(vp,sp)):
					weak_matches_to_vp+=1
					if (weak_matches_to_vp > 1):
						print "vf_precinct_name '%s' has %d possible weak matches (incl '%s' and '%s') so ignoring all" % (vp.vf_precinct_name,weak_matches_to_vp,temp,sp.s_precinct_name)
					temp = sp.s_precinct_name
			if (weak_matches_to_vp == 1):
				vp.copySourcedInfo(sp)
				matched.append(vp)
				sourcedPrecinctsPerCounty[cnty].remove(sp)
				vf_unmatched.remove(vp)
	
### OUTPUT ###
	fmatched = open('matched.csv','w')
	fmatched.write('sourced_precinct_id,vf_precinct_id,sourced_county,vf_precinct_county,sourced_precinct_name,vf_precinct_name,sourced_precinct_number,vf_precinct_code,sourced_ward,vf_precinct_ward,vf_precinct_count,polling_location_ids\n')
	for p in sorted(matched,key=countySort):
		fmatched.write(p.getCombinedInfo())
	fmatched.close()
	
	fvf_unmatched = open('vf_unmatched.csv','w')
	fvf_unmatched.write('vf_precinct_id,vf_precinct_county,vf_precinct_ward,vf_precinct_name,vf_precinct_code,vf_precinct_count\n') 
	for p in sorted(vf_unmatched,key=countySort):
		fvf_unmatched.write(p.getVFInfo())
	fvf_unmatched.close() 
	
	sourced_unmatched_counter = 0
	fs_unmatched = open('sourced_unmatched.csv','w')
	fs_unmatched.write('sourced_precinct_id,sourced_county,sourced_precinct_name,sourced_precinct_number,sourced_ward,polling_location_ids,source,internal_notes\n')
	for cnty in sorted(sourcedPrecinctsPerCounty.keys()):
		for p in sourcedPrecinctsPerCounty[cnty]:
			fs_unmatched.write(p.getSourcedInfo())
			sourced_unmatched_counter+=1
	fs_unmatched.close()
	
	print '\nMatched %d precincts' % len(matched)
	print '%d vf precincts unmatched' % len(vf_unmatched)
	print '%d sourced precincts unmatched\n' % sourced_unmatched_counter

if __name__ == "__main__":
	main()