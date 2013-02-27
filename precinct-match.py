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
	def pInfo(self):
		print '\nvf_county: %s s_county: %s vf_precinct_name: %s s_precinct_name: %s' % (self.vf_county, self.s_county, self.vf_precinct_name, self.s_precinct_name)

def MyFn(self):
	return self.vf_county

def main():
	vfPrecincts = {} #dict with key = vf_precinct_id and value = Precinct objects
#	vfPrecincts = [] #list of Precinct objects
	sourcedPrecinctsByCounty = {} #dictionary with key = county_name and value = LIST of Precinct objects

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
	#may need to store some fields as numbers rather than strings?
	sfile.close()
	
	vfile = open('vf_precincts.csv', 'r')
	for line in vfile:
		parts = line.split(',')
		vfPrecincts[parts[0]] = (Precinct(vf_precinct_id=parts[0],vf_county=parts[1],vf_ward=parts[2],vf_precinct_name=parts[3],vf_precinct_code=parts[4],vf_precinct_count=parts[5]))
	vfile.close()

	match_count = 0
	for vfp in vfPrecincts:
		cnty = vfPrecincts[vfp].vf_county
		if (cnty in sourcedPrecinctsByCounty):
			for sp in sourcedPrecinctsByCounty[cnty]:
				if (vfPrecincts[vfp].vf_precinct_code == sp.s_precinct_number):
					vfPrecincts[vfp].pInfo()
					sp.pInfo()
					match_count+=1
					print match_count
		else:
			print "VF COUNTY (%s) MISSING FROM SOURCED" % cnty
	#handle blank final line


	#county names should match exactly; 
	#vf_precinct_name may contain the sourced_name (example, vf_precinct_name 'Canyon - 09' contains sourced name '9')
	#sourced_precinct_number may match vf_precinct_code
	
	print 'done!'

if __name__ == "__main__":
	main()