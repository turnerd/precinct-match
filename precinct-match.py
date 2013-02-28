#!/usr/bin/env python
#
# Derek Turner 2013 for NOI VIP / Election Administration team job application
#

#check presence of two input files; check that they are well formatted
#read them into memory
#do a prelim match based on perfect equality
#do a secondary match? optional
#output matched and unmatchables
#special cases to handle?

#sourced: precinct_id,county,precinct_name,precinct_number,ward,polling_location_ids,source,INTERNAL_notes,,,,
#VF: vf_precinct_id,vf_precinct_county,vf_precinct_ward,vf_precinct_name,vf_precinct_code,vf_precinct_count
#matched: sourced_precinct_id,vf_precinct_id,sourced_county,vf_precinct_county,sourced_precinct_name,vf_precinct_name,
#	sourced_precinct_number,vf_precinct_code,sourced_ward,vf_precinct_ward,vf_precinct_count,polling_location_ids

#dict of (lists of Precincts) with county name for keys

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
		return '%s,%s,%s,%s,%s,%s\n' % (self.vf_precinct_id,self.vf_county,self.vf_ward,self.vf_precinct_name,self.vf_precinct_code,
			self.vf_precinct_count)
	def getSourcedInfo(self):
		return '%s,%s,%s,%s,%s,%s,%s,%s\n' % (self.s_precinct_id,self.s_county,self.s_precinct_name,self.s_precinct_number,self.s_ward,
			self.polling_location_ids,self.source,self.internal_notes)

def countySort(precinctObj):
		if (precinctObj.vf_county != ''): return precinctObj.vf_county
		else: return precinctObj.s_county 
		
def main():
	sourcedPrecinctsPerCounty = {} #dictionary with key= county_name and value= LIST of Precinct objects
	vfPrecincts = [] #list of Precinct objects
	matched = []
	sourced_unmatched = []
	vf_unmatched = []

	sfile = open('sourced_precincts.csv', 'r')
	counter = 0
	for line in sfile:
		parts = line.split(',') #assumes no values contain commas, which is the case in sample data. if this weren't so, would use csv module
		if (counter != 0): #skip header
			precinctObj = Precinct(s_precinct_id=parts[0],s_county=parts[1],s_precinct_name=parts[2],s_precinct_number=parts[3],s_ward=parts[4],polling_location_ids=parts[5],source=parts[6],internal_notes=parts[7].strip())
			cnty = parts[1]
			if (cnty in sourcedPrecinctsPerCounty):
				sourcedPrecinctsPerCounty[cnty].append(precinctObj)
			else:
				sourcedPrecinctsPerCounty[cnty] = [precinctObj]
		counter+=1		
	sfile.close()
	
	vfile = open('vf_precincts.csv', 'r')
	counter = 0
	for line in vfile:
		if (counter != 0): #skip header
			parts = line.split(',')
			vfPrecincts.append(Precinct(vf_precinct_id=parts[0],vf_county=parts[1],vf_ward=parts[2],vf_precinct_name=parts[3],vf_precinct_code=parts[4],vf_precinct_count=parts[5].strip()))
		counter+=1	
	vfile.close()

	for vp in vfPrecincts:
		match_found = False
		cnty = vp.vf_county
		if (cnty in sourcedPrecinctsPerCounty):
			for sp in sourcedPrecinctsPerCounty[cnty]:
				if (vp.vf_precinct_code == sp.s_precinct_number): #this may not be right criteria
					vp.copySourcedInfo(sp)
					matched.append(vp)
					sourcedPrecinctsPerCounty[cnty].remove(sp)
					match_found = True
		if (not match_found):
			vf_unmatched.append(vp)
		#else: print "VF COUNTY (%s) MISSING FROM SOURCED" % cnty 
			#handle blank final line
	
	print '\n\n############## MATCHED #############'
	fmatched = open('matched_test.csv','w')
	for p in sorted(matched,key=countySort):
		fmatched.write(p.getCombinedInfo())
	fmatched.close()
	
	print '\n\n############## VF UNMATCHED ##########'
	fvf_unmatched = open('vf_unmatched_test.csv','w') 
	#print headers too
	for p in sorted(vf_unmatched,key=countySort):
		fvf_unmatched.write(p.getVFInfo())
	fvf_unmatched.close() 
	#handle zero unmatched
	
	print '\n\n############## SOURCED UNMATCHED ############'
	sourced_unmatched_counter = 0
	fs_unmatched = open('sourced_unmatched_test.csv','w')
	for cnty in sorted(sourcedPrecinctsPerCounty.keys()):
		for p in sourcedPrecinctsPerCounty[cnty]:
			fs_unmatched.write(p.getSourcedInfo())
			sourced_unmatched_counter+=1
	fs_unmatched.close()
	
	print 'num matched is %d' % len(matched)
	print 'num vf_unmatched is %d ' % len(vf_unmatched)
	print 'num sourced_unmatched is %d' % sourced_unmatched_counter

	#county names should match exactly; 
	#vf_precinct_name may contain the sourced_name (example, vf_precinct_name 'Canyon - 09' contains sourced name '9')
	#sourced_precinct_number may match vf_precinct_code
	
	print 'done!'
#1) sort list of Precinct Objects -- DONE

#3) output to files
#2) experiment with adding other match criteria
#4) validate headers
#5) make a web app
if __name__ == "__main__":
	main()