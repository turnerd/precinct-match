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
	def __init__(self, pcounty, pname, pnum, pward, p_location_ids, psource, pnotes, vfcount):
		self.county = pcounty
		self.name = pname
		self.precinct_number = pnum
		self.ward = pward
		self.polling_location_ids = p_location_ids
		self.source = psource
		self.notes = pnotes
		self.count = vfcount
	def precinctInfo(self):
		print '\ncounty: %s name: %s polling_location_ids: %s' %(self.county, self.name, self.polling_location_ids)

def main():
	sourcedPrecincts = {} #dict of sourced precinct_id and Precinct Objects
	vfPrecincts = {} #dict of vf_precinct_id and Precinct Objects

	sourcedPrecinctsByCounty = {} #dictionary with key = county_name and value = list of Precinct objects

	sfile = open('sourced_precincts.csv', 'r')
	for line in sfile:
		chunks = line.split(',') #assumes no values contain commas, which is the case in sample data.  if this weren't so, would use csv module
		precinctObj = Precinct(pcounty=chunks[1],pname=chunks[2],pnum=chunks[3],pward=chunks[4],p_location_ids=chunks[5],psource=chunks[6],pnotes=chunks[7],vfcount='')
		county = chunks[1]
		if (county in sourcedPrecinctsByCounty):
			sourcedPrecinctsByCounty[county].append(precinctObj)
		else:
			sourcedPrecinctsByCounty[county] = [precinctObj]
			
		#may need to store some fields as numbers rather than strings?
	sfile.close()

	vf = open('vf_precincts.csv', 'r')
	for line in vf:
		chunks = line.split(',')
		vfPrecincts[chunks[0]] = Precinct(chunks[1],chunks[3],chunks[4],chunks[2],'','','',chunks[5])
	

	#for p in sourcedPrecincts:
	#	sourcedPrecincts[p].precinctInfo()
	match_count = 0
	for v in vfPrecincts:
		c = vfPrecincts[v].county
		if (c in sourcedPrecinctsByCounty):
			for pre in sourcedPrecinctsByCounty[vfPrecincts[v].county]:
				if (vfPrecincts[v].precinct_number == pre.precinct_number):
					vfPrecincts[v].precinctInfo()
					pre.precinctInfo()
					match_count+=1
					print match_count
		else:
			print "VF COUNTY (%s) MISSING FROM SOURCED" % c
			


	#county names should match exactly; 
	#vf_precinct_name may contain the sourced_name (example, vf_precinct_name 'Canyon - 09' contains sourced name '9')
	#sourced_precinct_number may match vf_precinct_code
	
	print 'done!'

if __name__ == "__main__":
	main()