import numpy as np
import statsmodels.api as sm
import rhythmtoolbox as rtb
from collections import Counter
from sklearn.linear_model import LogisticRegression

#This code is used to present some examples of the use of the different functions in rhythmtoolbox.py

#_________
print "Example 1: load a database fo patterns"
# Load a data base composed of symbolic drum patterns.
# The HTB database has House, Techno and Breakbeat patterns.
#the output format of each pattern is: [patt-name, [onsets step1], [onsets step2]...]

htb=rtb.loadPatterns('src/HTB.txt',16)
print htb
print "_____________________"

#_________
print "Example 2: load midi patterns from a folder to a list"
boska = rtb.midifolder2list('boska')
print boska
print "_____________________"

#_________
print "example 3: visualize a specific pattern"
# Once the patterns have been loaded into the list called 'htb', we can do cool stuff with them.
# For example, to visualize the pattern

name='breakfunkydrummer_EH'
p=[x for x in htb if x[0] == name][0] #search within the patterns in 'htb' that matches 'name'
print p
rtb.heatmap(p) #call the heatmap function for pattern p
print "_____________________"

#_________
print "example 4: generate a style from patterns in 'htb'"
# Create some style knowledge based for example on the techno patterns in htb. 
# The style to be used with Dr.Drums a real time drum generator and transformer
# Written in PureData whcih can be found here:
# https://github.com/danielgomezmarin/mididrums/blob/master/README.md

# # Example creating Techno style
# htb=rtb.loadPatterns('src/HTB.txt',16)
# t=[x for x in htb if x[0][0]=='t'] #create a list only of techno patterns which start with a 't'.
# print t
# rtb.makestyle(t,16,'styles','alltechno') #create a style based on techno, length 16, save in folder 'styles', name'alltechno'

# As before, select only breakbeat patterns 
# and make a style based on them

# htb=rtb.loadPatterns('src/HTB.txt',16)
# bb=[x for x in htb if x[0][:5]=='break'] #list of breakbeat patterns: patterns in htb which start with 'break'
# for bbp in bb:
# 	print bbp
# rtb.makestyle(bb,16,'styles','allbreakbeat') #create a style based on breakbeat, length 16, save to folder 'styles', name'allbreakbeat'

htb=rtb.loadPatterns('src/HTB.txt',16)
h=[x for x in htb if 'house' in x[0]] #list of breakbeat patterns: patterns in htb which start with 'break'
for hp in h:
	print hp
rtb.makestyle(h,16,'styles','allhouse') #create a style based on house, length 16 steps, save to folder 'styles', name'allhouse'
print "_____________________"

#_________
print "example 5: generatye a style based on the elements of a folder"
sano = rtb.midifolder2list('sano')
print sano
rtb.makestyle(sano,16,'styles','allsano') #create a style based on sano, length 16, save to folder 'styles', name'allsano'
print "_____________________"

#_________
print "example 6: generate a rhythm space"
# With the following two lines compute a rhythm space using the methodology found experimentally.
# The rs_gen function computes the positions for each pattern 
# The rs_plot function plots the graph
names,pos=rtb.rs_gen(htb) # compute positions
rtb.rs_plot(names,pos,'Rhythm Space') # plot on a space and set title as Rhythm Space
for i,n in enumerate(names):
	print n, pos[i]
print "_____________________"

#_________
print "example 7: analyze MIDI patterns from a folder"
boska = rtb.midifolder2list('boska')
sano = rtb.midifolder2list('sano')
analysis_boska = rtb.patts2Mtx(boska)
descriptors_boska=np.delete(analysis_boska[1], np.s_[16:], 1)
analysis_sano = rtb.patts2Mtx(sano)
descriptors_sano=np.delete(analysis_sano[1], np.s_[16:], 1)
# print analysis_boska[0]
# print descriptors_boska
# print descriptors_sano
# print analysis_sano[0]
# print analysis_sano[1]
#consolidate both collections in one array
X=np.concatenate((descriptors_boska,descriptors_sano), axis=0)
y_boska=np.array([1]*10)
y_sano=np.array([2]*10)
y=np.concatenate((y_boska,y_sano), axis=0)

lr=LogisticRegression()
lr.fit(X, y)

preds = lr.predict(X) #test classification model with an np.array of descriptors.

important_descriptors=[]
for i,w in enumerate(lr.coef_[0]):
	
	important_descriptors.append([rtb.descriptorList16[i], w])
important_descriptors.sort(key=lambda x: x[1])

print "these are the important descriptors sorted"
print important_descriptors
boskasano=boska+sano
print boskasano

"""generate a rhythm space"""
names,pos=rtb.rs_gen(boskasano) # compute positions
rtb.rs_plot(names,pos,'Rhythm Space') # plot on a space and set title as Rhythm Space
for i,n in enumerate(names):
	print n, pos[i]

print "_____________________"