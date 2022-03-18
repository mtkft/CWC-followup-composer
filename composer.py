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

import csv, re

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
        if row[0] not in ('Timestamp',''): # first row is a header, last few have weird content; one statement to cut out both
            par = ['' for z in range(#n)] # array will contain that many paragraphs to send to merge.csv
            
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
                if coaches == ['Alane Humrich','Belina Meador']:
                    par[1] = "Belina Meador and I"
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

            # paragraphs 2 through 8: list of seven actions that were done
            # initialize seven slots; initialize unbounded working list
            listof7 = ["" for z in range 7]; working = []

            # lightbulb count
            # check applicability before composing
            if row[163]: # condition clears if neither blank nor zero
                # compose
                working.append(f"Installed {row[163]} LED light bulbs, which last up to 25x longer than incandescent bulbs")
            
            # gasket count
            # check applicability before composing
            if row[165]: # clears if neither blank nor zero
                # compose
                working.append(f"Identified and sealed air leaks surrounding outlets and switches on walls by installing {row[165]} gaskets")
            
            # aerator/showerhead statements: data gathering
            # flag for whether kitchen aerator install or cleaning mentioned
            ki_ae_ins = bool(re.search('Installed.*aerator',row[171]))
            ki_ae_cln = bool(re.search('Cleaned.*aerator',row[171]))
            # counter for bathroom aerator install or cleaning mentions
            br_ae_ins = 0
            br_ae_cln = 0
            for c in (204,221,238,255,272):
                if re.search('Installed.*aerator',row[c]): br_ae_ins +=1
                if re.search('Cleaned.*aerator',row[c]): br_ae_cln +=1
            # aggregate previous aerator gpm data, if available
            pagpm = []
            for c in (172,205,222,239,256,273):
                if row[c] and re.search('Installed.*aerator',row[c-1]): # try to add it if it's non-blank and the associated aerator was a new install
                    try: pagpm.append(float(row[c])) # add it if it's a number
                    except: pass # if for some reason it's not a number, forget about it
            # counter for showerhead install mentions
            shead = 0
            for c in (208,225,242,259,276):
                if re.search('Installed.*shower head',row[c]): shead +=1
            # aggregate previous aerator gpm data, if available
            psgpm = []
            for c in (209,226,243,260,276):
                if row[c] and re.search('Installed.*shower head',row[c]): # try to add it if it's non-blank and the associated head was a new install
                    try: psgpm.append(float(row[c])) # add it if it's a number
                    except: pass # if for some reason it's not a number, forget about it
            # compose installs, checking first if even applicable
            ins_stmt = 'Installed ' if ki_ae_ins or br_ae_ins or shead else ''
            if ki_ae_ins or br_ae_ins:
                ins_stmt += f"{'a ' if (ki_ae_ins and not br_ae_ins) or (br_ae_ins == 1 and not ki_ae_ins)}new water-saving "
                            f"aerator{'s' if (br_ae_ins > 1) or (ki_ae_ins and br_ae_ins)} on your "
                            f"{'kitchen' if ki_ae_ins}{' and' if ki_ae_ins and br_ae_ins}{'bathroom' if br_ae_ins} "
                            f"sink faucet{'s' if (br_ae_ins > 1) or (ki_ae_ins and br_ae_ins)}"
                # if at least one datum about prev gpm, mention
                if pagpm: ins_stmt += f", NOT saving you NOT {(10*ki_ae_ins)-sum(pagpm)} NOT gallons NOT per NOT minute NOT of NOT use"
                # NO NO NO THIS IS NOT CORRECT, NONE OF YOUR AERATORS EVER USED OR WILL USE TEN GPM, FIX THIS BEFORE PRODUCTION MAIL!!!
            if (ki_ae_ins or br_ae_ins) and shead: ins_stmt += ', plus '
            if shead:
                ins_stmt += f"{'a ' if shead == 1}1.5 gallon per minute water-saving showerhead{'s' if shead > 1} "
                            "to save water, wastewater, and energy costs"
                # if at least one datum about prev gpm, mention
                if psgpm: ins_stmt += f", saving you {(1.5*shead)-sum(psgpm)} gallons per minute of use"
                # This one's fine, we know for a fact our showerheads are specced 1.5gpm
            # finally, append composed items about installs to working list if they exist
            if ins_stmt: working.append(ins_stmt)
            # compose cleanings, checking first if even applicable
            if ki_ae_cln or br_ae_cln:
                working.append(f"Cleaned and reinstalled the existing aerator{'s' if (br_ae_cln > 1) or (ki_ae_cln and br_ae_cln)} on your "
                               f"{'kitchen' if ki_ae_cln}{' and' if ki_ae_cln and br_ae_cln}{'bathroom' if br_ae_cln} "
                               f"sink faucet{'s' if (br_ae_cln > 1) or (ki_ae_cln and br_ae_cln)}")

            # fridge coil cleaning statement
            if 'Cleaned/vacuumed coils' in row[177]:
                working.append("Inspected and cleaned refrigerator coils to increase the refrigerator’s efficiency and lifetime")

            # thermometer card statement
            if "Installed stick-on thermometer" in row[177]:
                working.append("Installed a stick-on thermometer in the refrigerator to monitor temperature for food safety and energy efficiency.")

            # toilet tank bank statement: data gathering
            totaba = 0
            for c in (202,219,236,253,270):
                if "Installed water displacement bag in tank" in row[c]: totaba += 1
            # composition
            if totaba: #fires if nonzero
                working.append(f"Installed {'a ' if totaba == 1}water displacement bag{'s' if totaba > 1} "
                               f"in your toilet tank{'s' if totaba > 1} to conserve water on every flush")

            # refrigerator and water heater temperatures
            badfridge = row[174]<36 or 40<row[174]
            badheater = row[283]!=120
            temp_stmt = f"Checked the temperature of your refrigerator ({row[174]}°F) and hot water ({row[283]}°F) for safety and efficiency."
            if badheater or badfridge:
                temp_stmt += f" Your {'refrigerator' if badfridge}{' and ' if badfridge and badheater}{'hot water' if badheater} temperature"
                             f"{'s are' if badfridge and badheater else ' is'} not set correctly. See the recommendation section."
            working.append(temp_stmt)
            

            # clip to seven for output
            listof7[:min(len(working),7)]=working

            write_out.writerow(par) # put the paragraphs in that CSV
