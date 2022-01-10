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

# [' '.join(z.split(' ')[:-1]) for z in name.split(' and ')] for splitting resident names

with open(input('Tune-Up data path (*.csv) >>> '),encoding="utf-8") as tuneups, open('merge.csv','w',encoding="utf-8") as merge:
    read_in=csv.reader(tuneups)
    write_out=csv.writer(merge)
    write_out.writerow(['salutation','par1','par2','par3'])
    for row in read_in:
        if row[0] not in ('Timestamp',''): # first row is a header, last few have weird content
            par = ['' for z in range(n)] # array will contain n paragraphs to send to merge.csv
            
            # paragraph 0: salutation
            # take contents of field 2 (third one over) and spit it out with the
            # last word taken out (word: has spaces around it)
            # and with formatting "Dear namename,"
            # That doesn't work yet, so I've commented out the line. It takes the whole field for now.
            par[0] = f"Dear {' '.join(row[2].strip().split(' ')[:-1]).strip()},"
            
            # paragraph 1: energy coaches involved
            # grab working copy of names list and strip blanks
            coaches = par[18:23]; coaches.remove('')
            # if only one coach...
            if int(row[17])==1:
                # if that's a staff member...
                if row[18] in ('Alane Humrich','Belina Meador'): par[1] = "I"
                # otherwise...
                else: par[1] = f"our Volunteer Energy Coach, {row[18]}"
            # if two...
            elif int(row[17])==2:
                # if both Alane and Belina...
                if coaches == ['Alane Humrich','Belina Meador']: par[1] = "Belina Meador and I"
                # else if Alane but not Belina...
                elif ('Alane Humrich' in coaches) and not ('Belina Meador' in coaches):
                    coaches.remove('Alane Humrich')
                    par[1] = f"our Volunteer Energy Coach, {''.join(coaches)}, and I"
                # else if just Belina but not Alane...
                elif ('Belina Meador' in coaches) and not ('Alane Humrich' in coaches):
                    coaches.remove('Belina Meador')
                    par[1] = f"our Volunteer Energy Coach, {''.join(coaches)}, and I"
                # else if no staff, just volunteers...
                else:
                    par[1] = f"our Volunteer Energy Coaches, {' and '.join(coaches)}"
            # if more...
            elif int(row[17])>2:
                # if Alane... TODO: decide wording if Alane AND Belina AND volunteers
                if ('Alane Humrich' in coaches):
                    coaches.remove('Alane Humrich') # this will currently class Belina under volunteers, if Belina present
                    par[1] = f"our Volunteer Energy Coaches, {', '.join(coaches)}, and I"
                # else if Belina but not Alane...
                elif ('Belina Meador' in coaches) and not ('Alane Humrich' in coaches): # do we actually need this second check about Alane?
                    coaches.remove('Belina Meador')
                    par[1] = f"our Volunteer Energy Coach, {', '.join(coaches)}, and I"
                # else if no staff, just volunteers...
                else:
                    par[1] = f"our Volunteer Energy Coaches, {', '.join(coaches[:-1])}, and coaches[-1]"

            write_out.writerow(par) # put the paragraphs in that CSV
