"""
composer.py: compose followup letter based on home energy tune-up inputs.
Copyright (C) 2021 Adam Livay

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import csv

print("""
composer.py Copyright (C) 2021 Adam Livay

This program comes with ABSOLUTELY NO WARRANTY.

This is free software, and you are welcome to redistribute it
in accordance with the GNU General Public License, version 3.
""")

with open(input('Tune-Up data path (*.csv) >>> '),encoding="utf-8") as tuneups, open('merge.csv','w',encoding="utf-8") as merge:
    read_in=csv.reader(tuneups)
    write_out=csv.writer(merge)
    write_out.writerow(['salutation','par1','par2','par3'])
    for row in read_in:
        if row[0] not in ('Timestamp',''): # first row is a header, last few have weird content
            par = ['' for z in range(4)] # array will contain paragraphs to send to merge.csv
            
            # compose salutation paragraph
            # take contents of field 2 (third one over) and spit it out with the
            # last word taken out (word: has spaces around it)
            # and with formatting "Dear namename,"
            # That doesn't work yet, so I've commented out the line. It takes the whole field for now.
            par[0] = 'Dear '+' '.join(row[2].strip().split(' ')[:-1]).strip()+','
            #par[0] = f"Dear {row[2]},"
            
            # paragraph 1
            # this is obviously facetious; remove in production script!
            hometype = 'apartment' if row[8] else 'house'
            par[1] = f"We visited your {hometype} at {' '.join(row[4:8])}"
            if hometype=='apartment':
                par[1] += ', '+row[8] # add a comma, a space, and the apartment number field
            par[1] += ', and energy coach(es) '+row[12]
            # logic isn't quite working, but is an example of complex handling
            #coaches = row[12].replace('"','').split(',') # make list of energy coaches and strip quotation marks
            #print(str(coaches))
            #if len(coaches)>1 : # more than one energy coach?
            #    par[1] += 'es '+', '.join(coaches[:-1])+', and '+coaches[-1]
            #else: par[1] += ' '+coaches[0]
            par[1] += ' did some tuning-up.'

            # not bothered to write paragraphs 2 or 3 (expandable!)

            write_out.writerow(par) # put the paragraphs in that CSV
