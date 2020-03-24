#!/usr/bin/env python
"""
Index Generator for The Book of Statistical Proofs
_
This script loads all files from the proof/definition directories and
- checks if they are in "Table of Contents" (structured overview)
- writes them as a list into "Proof by Number" (chronological list)
- writes them as a list into "Proof by Topic" (an alphabetical list)
- writes them as a list into "Proof by Author" (sorted by contributor)
- writes them as a list into "Definition by Number" (chronological list)
- writes them as a list into "Definition by Topic" (an alphabetical list)
- writes them as a list into "Definition by Author" (sorted by contributor)

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2019-09-27 12:55:00
 Last edit: 2020-02-13 16:51:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import re
import numpy as np
from datetime import datetime

# List files in proof directory
#-----------------------------------------------------------------------------#
files     = os.listdir('P/')
proofs    = dict()
pr_ids    = []
pr_nos    = []
pr_titles = []
pr_users  = []

# Browse through list of files
#-----------------------------------------------------------------------------#
for file in files:
    if '.md' in file:
        
        # Read proof file
        #---------------------------------------------------------------------#
        file_obj = open('P/' + file, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Parse YAML header
        #---------------------------------------------------------------------#
        for line in file_txt:
            if line.find('proof_id:') == 0:
                proof_id = re.sub('"', '', line[10:-1])
            if line.find('shortcut:') == 0:
                shortcut = re.sub('"', '', line[10:-1])
            if line.find('title:') == 0:
                title = re.sub('"', '', line[7:-1])
            if line.find('author:') == 0:
                author = re.sub('"', '', line[8:-1])
            if line.find('username:') == 0:
                username = re.sub('"', '', line[10:-1])
                if not username:
                    if not author:
                        username = 'unknown'
                    else:
                        username = author
            if line.find('date:') == 0:
                date = datetime.strptime(line[6:-1], '%Y-%m-%d %H:%M:%S')
        
        # Write dictionary entry
        #---------------------------------------------------------------------#
        proofs[proof_id] = {'proof_id': proof_id, 'shortcut': shortcut, 'title': title, \
                            'username': username, 'date': date}
        pr_ids.append(proof_id)
        pr_nos.append(int(proof_id[1:]))
        pr_titles.append(title)
        pr_users.append(username)

# List files in definition directory
#-----------------------------------------------------------------------------#
files       = os.listdir('D/')
definitions = dict()
def_ids     = []
def_nos     = []
def_titles  = []
def_users   = []

# Browse through list of files
#-----------------------------------------------------------------------------#
for file in files:
    if '.md' in file:
        
        # Read proof file
        #---------------------------------------------------------------------#
        file_obj = open('D/' + file, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Parse YAML header
        #---------------------------------------------------------------------#
        for line in file_txt:
            if line.find('def_id:') == 0:
                def_id = re.sub('"', '', line[8:-1])
            if line.find('shortcut:') == 0:
                shortcut = re.sub('"', '', line[10:-1])
            if line.find('title:') == 0:
                title = re.sub('"', '', line[7:-1])
            if line.find('author:') == 0:
                author = re.sub('"', '', line[8:-1])
            if line.find('username:') == 0:
                username = re.sub('"', '', line[10:-1])
                if not username:
                    if not author:
                        username = 'unknown'
                    else:
                        username = author
            if line.find('date:') == 0:
                date = datetime.strptime(line[6:-1], '%Y-%m-%d %H:%M:%S')
        
        # Write dictionary entry
        #---------------------------------------------------------------------#
        definitions[def_id] = {'def_id': def_id, 'shortcut': shortcut, 'title': title, \
                               'username': username, 'date': date}
        def_ids.append(def_id)
        def_nos.append(int(def_id[1:]))
        def_titles.append(title)
        def_users.append(username)

# Output number of proof files
#-----------------------------------------------------------------------------#
print('\n-> StatProofBook Index Generator:')
print('   - ' + str(len(proofs)) + ' files found in proof directory!')
print('   - ' + str(len(definitions)) + ' files found in definition directory!')


# Table of Contents: read index file
#-----------------------------------------------------------------------------#
print('\n1. "Table_of_Contents.md":')
ind1 = open('I/Table_of_Contents.md', 'r')
tocs = ind1.readlines()
ind1.close()

# Table of Contets: check for proof Shortcuts
#-----------------------------------------------------------------------------#
incl = np.zeros(len(proofs), dtype=bool)
for (i, proof) in enumerate(proofs):
    for line in tocs:
        if line.find('(/P/' + proofs[proof]['shortcut'] + ')') > -1:
            incl[i] = True
    if ~incl[i]:
        print('   - WARNING: proof "' + proofs[proof]['shortcut'] + '" is not in table of contents!')
if all(incl):
    print('   - ' + str(sum(incl)) + ' proofs found in table of contents!')

# Table of Contets: check for definition Shortcuts
#-----------------------------------------------------------------------------#
incl = np.zeros(len(definitions), dtype=bool)
for (i, definition) in enumerate(definitions):
    for line in tocs:
        if line.find('(/D/' + definitions[definition]['shortcut'] + ')') > -1:
            incl[i] = True
    if ~incl[i]:
        print('   - WARNING: definition "' + definitions[definition]['shortcut'] + '" is not in table of contents!')
if all(incl):
    print('   - ' + str(sum(incl)) + ' definitions found in table of contents!')


# Proof by Number: prepare index file
#-----------------------------------------------------------------------------#
print('\n2a."Proof_by_Number.md":')
ind2a = open('I/Proof_by_Number.md', 'w')
ind2a.write('---\nlayout: page\ntitle: "Proof by Number"\n---\n\n\n')
ind2a.write('| ID | Shortcut | Theorem | Author | Date |\n')
ind2a.write('|:-- |:-------- |:------- |:------ |:---- |\n')

# Proof by Number: sort by Proof ID
#-----------------------------------------------------------------------------#
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(pr_nos)])]
for i in sort_ind:
    ind2a.write('| ' + proofs[pr_ids[i]]['proof_id'] + ' | ' + proofs[pr_ids[i]]['shortcut'] + ' | [' + \
                       proofs[pr_ids[i]]['title'] + '](/P/' + proofs[pr_ids[i]]['shortcut'] + ') | ' + \
                       proofs[pr_ids[i]]['username'] + ' | ' + proofs[pr_ids[i]]['date'].strftime('%Y-%m-%d') + ' |\n')
ind2a.close()
print('   - successfully written to disk!')


# Definition by Number: prepare index file
#-----------------------------------------------------------------------------#
print('\n2b."Definition_by_Number.md":')
ind2b = open('I/Definition_by_Number.md', 'w')
ind2b.write('---\nlayout: page\ntitle: "Definition by Number"\n---\n\n\n')
ind2b.write('| ID | Shortcut | Theorem | Author | Date |\n')
ind2b.write('|:-- |:-------- |:------- |:------ |:---- |\n')

# Definition by Number: sort by Definition ID
#-----------------------------------------------------------------------------#
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(def_nos)])]
for i in sort_ind:
    ind2b.write('| ' + definitions[def_ids[i]]['def_id'] + ' | ' + definitions[def_ids[i]]['shortcut'] + ' | [' + \
                       definitions[def_ids[i]]['title'] + '](/D/' + definitions[def_ids[i]]['shortcut'] + ') | ' + \
                       definitions[def_ids[i]]['username'] + ' | ' + definitions[def_ids[i]]['date'].strftime('%Y-%m-%d') + ' |\n')
ind2b.close()
print('   - successfully written to disk!')


# Proof by Topic: prepare index file
#-----------------------------------------------------------------------------#
print('\n3a."Proof_by_Topic.md":')
ind3a = open('I/Proof_by_Topic.md', 'w')
ind3a.write('---\nlayout: page\ntitle: "Proof by Topic"\n---\n\n\n')

# Proof by Topic: sort by Title
#-----------------------------------------------------------------------------#
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(pr_titles)])]
for i in range(0,len(pr_titles)):
    shortcut = proofs[pr_ids[sort_ind[i]]]['shortcut']
    title    = proofs[pr_ids[sort_ind[i]]]['title']
    if i == 0:
        ind3a.write('### ' + title[0] + '\n\n')
    else:
        if title[0] != proofs[pr_ids[sort_ind[i-1]]]['title'][0]:
            ind3a.write('\n### ' + title[0] + '\n\n')
    ind3a.write('- [' + title + '](/P/' + shortcut + ')\n')
ind3a.close()
print('   - successfully written to disk!')


# Definition by Topic: prepare index file
#-----------------------------------------------------------------------------#
print('\n3b."Definition_by_Topic.md":')
ind3b = open('I/Definition_by_Topic.md', 'w')
ind3b.write('---\nlayout: page\ntitle: "Definition by Topic"\n---\n\n\n')

# Definition by Topic: sort by Title
#-----------------------------------------------------------------------------#
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(def_titles)])]
for i in range(0,len(def_titles)):
    shortcut = definitions[def_ids[sort_ind[i]]]['shortcut']
    title    = definitions[def_ids[sort_ind[i]]]['title']
    if i == 0:
        ind3b.write('### ' + title[0] + '\n\n')
    else:
        if title[0] != definitions[def_ids[sort_ind[i-1]]]['title'][0]:
            ind3b.write('\n### ' + title[0] + '\n\n')
    ind3b.write('- [' + title + '](/D/' + shortcut + ')\n')
ind3b.close()
print('   - successfully written to disk!')


# Proof by Author: prepare index file
#-----------------------------------------------------------------------------#
print('\n4a."Proof_by_Author.md":')
ind4a = open('I/Proof_by_Author.md', 'w')
ind4a.write('---\nlayout: page\ntitle: "Proof by Author"\n---\n\n')

# Proof by Authors: sort by Username
#-----------------------------------------------------------------------------#
unique_users = list(set(pr_users))
unique_users.sort()
for user in unique_users:
    user_proofs = [proof for proof in proofs.values() if proof['username'] == user]
    if len(user_proofs) == 1:
        ind4a.write('\n### ' + user + ' (1 proof)\n\n')
    else:
        ind4a.write('\n### ' + user + ' (' + str(len(user_proofs)) + ' proofs)\n\n')
    user_titles = []
    for proof in user_proofs:
        user_titles.append(proof['title'])
    sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(user_titles)])]
    for i in range(0,len(user_titles)):
        shortcut = user_proofs[sort_ind[i]]['shortcut']
        title    = user_proofs[sort_ind[i]]['title']
        ind4a.write('- [' + title + '](/P/' + shortcut + ')\n')
ind4a.close()
print('   - successfully written to disk!')


# Definition by Author: prepare index file
#-----------------------------------------------------------------------------#
print('\n4b."Definition_by_Author.md":')
ind4a = open('I/Definition_by_Author.md', 'w')
ind4a.write('---\nlayout: page\ntitle: "Definition by Author"\n---\n\n')

# Definition by Authors: sort by Username
#-----------------------------------------------------------------------------#
unique_users = list(set(def_users))
unique_users.sort()
for user in unique_users:
    user_definitions = [definition for definition in definitions.values() if definition['username'] == user]
    if len(user_definitions) == 1:
        ind4a.write('\n### ' + user + ' (1 definition)\n\n')
    else:
        ind4a.write('\n### ' + user + ' (' + str(len(user_definitions)) + ' definitions)\n\n')
    user_titles = []
    for definition in user_definitions:
        user_titles.append(definition['title'])
    sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(user_titles)])]
    for i in range(0,len(user_titles)):
        shortcut = user_definitions[sort_ind[i]]['shortcut']
        title    = user_definitions[sort_ind[i]]['title']
        ind4a.write('- [' + title + '](/D/' + shortcut + ')\n')
ind4a.close()
print('   - successfully written to disk!')