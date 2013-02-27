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
	s_precinct_number='',vf_precinct_code='',s_ward='',vf_ward='',vf_precinct_count='',polling_location_ids='',source='',INTERNAL_notes=''):
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
		self.INTERNAL_notes = INTERNAL_notes
	def combineInfo(self, sp):
		self.s_precinct_id = sp.s_precinct_id
		self.s_county = sp.s_county
		self.s_precinct_name = sp.s_precinct_name
		self.s_precinct_number = sp.s_precinct_number
		self.s_ward = sp.s_ward
		self.polling_location_ids = sp.polling_location_ids
		self.source = sp.source
		self.INTERNAL_notes = sp.INTERNAL_notes
	def printfull(self):
		print '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (self.s_precinct_id,self.vf_precinct_id,self.s_county,self.vf_county,
			self.s_precinct_name,self.vf_precinct_name,self.s_precinct_number,self.vf_precinct_code,self.s_ward,self.vf_ward,
			self.vf_precinct_count,self.polling_location_ids)
		
def main():
	vfPrecincts = {} #dict with key = vf_precinct_id and value = Precinct objects
#	vfPrecincts = [] #list of Precinct objects
	sourcedPrecinctsByCounty = {} #dictionary with key = county_name and value = LIST of Precinct objects
	matched = []
	sourced_unmatched = []
	vf_unmatched = []

	sfile = open('sourced_precincts.csv', 'r')
	counter = 0
	for line in sfile:
		parts = line.split(',') #assumes no values contain commas, which is the case in sample data. if this weren't so, would use csv module
		if (counter != 0): #must skip headers
			precinctObj = Precinct(s_precinct_id=parts[0],s_county=parts[1],s_precinct_name=parts[2],s_precinct_number=parts[3],s_ward=parts[4],polling_location_ids=parts[5],source=parts[6],INTERNAL_notes=parts[7])
			cnty = parts[1]
			if (cnty in sourcedPrecinctsByCounty):
				sourcedPrecinctsByCounty[cnty].append(precinctObj)
			else:
				sourcedPrecinctsByCounty[cnty] = [precinctObj]
		counter+=1		
	sfile.close()
	
	vfile = open('vf_precincts.csv', 'r')
	for line in vfile:
		parts = line.split(',')
		vfPrecincts[parts[0]] = Precinct(vf_precinct_id=parts[0],vf_county=parts[1],vf_ward=parts[2],vf_precinct_name=parts[3],vf_precinct_code=parts[4],vf_precinct_count=parts[5].strip())
	vfile.close()

	match_count = 0
	for v in vfPrecincts:
		match_found = False
		cnty = vfPrecincts[v].vf_county
		if (cnty in sourcedPrecinctsByCounty):
			for sp in sourcedPrecinctsByCounty[cnty]:
				if (vfPrecincts[v].vf_precinct_code == sp.s_precinct_number): #this may not be right criteria
					vfPrecincts[v].combineInfo(sp)
					matched.append(vfPrecincts[v])
					match_found = True
					match_count+=1
		if (not match_found):
			vf_unmatched.append(vfPrecincts[v])
					#how to get list of sourced_unmatched?
		else:
			print "VF COUNTY (%s) MISSING FROM SOURCED" % cnty #handle blank final line
	
	print '\n\n############## MATCHED #############'
	for p in matched:
		p.printfull()
	print match_count
	
	print '\n\n############## VF UNMATCHED ##########'
	for p in vf_unmatched:
		p.printfull() #handle zero unmatched
	print 'num vf_unmatched is %d ' % len(vf_unmatched)
		

	#county names should match exactly; 
	#vf_precinct_name may contain the sourced_name (example, vf_precinct_name 'Canyon - 09' contains sourced name '9')
	#sourced_precinct_number may match vf_precinct_code
	
	print 'done!'

if __name__ == "__main__":
	main()