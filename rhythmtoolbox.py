import numpy as np
from scipy import stats
from sklearn import linear_model
from sklearn.decomposition import PCA
from sklearn import manifold
import matplotlib.pyplot as plt
import pylab
from collections import Counter
import mido as mido
import os

def compute(pattern):
# Compute a set of rhythmic descrptors for one polyphonic pattern
# a pattern must be a list of lists: the fists element is the name of the pattern
# the other elememts are lists, each list is a 16th step of the pattern.
# each of this lists contains MIDI numbers of the onsets present on that step.

	descriptorlist=['noi', 'loD', 'midD', 'hiD', 'stepD', 'lowness', 'midness', 'hiness', 
	'lowsync', 'midsync', 'hisync', 'losyness', 'midsyness', 'hisyness', 
	'beatdiv', 'polysync',
	'B1_lo','B2_lo','B3_lo','B4_lo','B5_lo','B6_lo','B7_lo','B8_lo',
	'B1_mid','B2_mid','B3_mid','B4_mid','B5_mid','B6_mid','B7_mid','B8_mid',
	'B1_hi','B2_hi','B3_hi','B4_hi','B5_hi','B6_hi','B7_hi','B8_hi']
	#print "name, noi, loD, midD, hiD, stepD, lowness, midness, hiness, lowsync, midsync, hisync, losyness, midsyness, hisyness, beatdiv, polysinc"

	#for pattern:
	descriptorvector=[]
	pattname= pattern[0]
	pattern=pattern[1:]
	#print len(pattern)
	descriptorvector.append(pattname)
	#Descriptor1: number of instruments

	listofinstruments=[]
	for steps in pattern:
		for events in steps:
			listofinstruments.append(events)
	setofinstruments=list(set(listofinstruments))
	if 0 in setofinstruments: setofinstruments.remove(0)
	noi=len(setofinstruments)
	descriptorvector.append(noi)

	#Descriptor2: loD density of low pitched instrumenst (kick and low conga)
	#Descriptor3: midD density of the upbeat instruments(snare, rimshot, hiconga)
	#Descriptor4: hiD density of high pitched sounds (closed hihat, shaker, clave)
	#Descriptor5: stepD density: percentage of the steps that have onsets (loD+midD+hiD)
	#Descriptors 6 7 8: lowness, midness, hiness i.e. lowD/stepD, midD/stepD. hiD/stepD
	#NOTE: these descriptors only augment once per step, overlapping of instruments of same descriptor counts as one
	lodcount=0
	lopatt=[0]*(len(pattern))
	middcount=0
	midpatt=[0]*(len(pattern))
	hidcount=0
	hipatt=[0]*(len(pattern))
	stepDcount=0
	lodcount_r=0 #counts 2 if kick and loconga are overlapped on same step
	middcount_r=0 #counts manyif mids overlapped at step
	hidcount_r=0 #counts many if his overlapped at step
	for s,steps in enumerate(pattern):
		
		for events in steps:
			if events == 36 or events == 64 or events == 45: #lows (kick and low conga and low tom)
				lodcount=lodcount+1
				lopatt[s]=1 #create a pattern for the lows
			if events == 38 or events == 63 or events == 37 or events == 39 or events == 40: #mids (snare, hi conga, rimshot,handclap, electricsnare)
				middcount=middcount+1
				midpatt[s]=1 #create a pattern for the mids
			if events == 69 or events == 42 or events == 75 or events == 46: #his (cabasa, closed hihat, clave, pedalhihat)
				hidcount=hidcount+1
				hipatt[s]=1 #create a pattern for the highs
			if events == 0:
				stepDcount=stepDcount+1
			#from here we start adding even if lows, mids or his are overlapped	
			#lows
			if events == 36:
				lodcount_r=lodcount_r+1
			if events == 64:
				lodcount_r=lodcount_r+1
			if events == 45:
				lodcount_r=lodcount_r+1
			#mids
			if events == 38:
				middcount_r=middcount_r+1
			if events == 63:
				middcount_r=middcount_r+1
			if events == 37:
				middcount_r=middcount_r+1
			if events == 39:
				middcount_r=middcount_r+1
			if events == 40:
				middcount_r=middcount_r+1
			#his
			if events == 69:
				hidcount_r=hidcount_r+1
			if events == 42:
				hidcount_r=hidcount_r+1
			if events == 75:
				hidcount_r=hidcount_r+1
			if events == 46:
				hidcount_r=hidcount_r+1
	
	loD=float(lodcount / float(len(pattern)))
	descriptorvector.append(loD)
	midD=float(middcount / float(len(pattern)))
	descriptorvector.append(midD)
	hiD=float(hidcount / float(len(pattern)))
	descriptorvector.append(hiD)
	stepD=(len(pattern)-stepDcount) / float(len(pattern))
	descriptorvector.append(stepD)
	lowness=loD/float(stepD)
	descriptorvector.append(lowness)
	midness=midD/float(stepD)
	descriptorvector.append(midness)
	hiness=hiD/float(stepD)
	descriptorvector.append(hiness)
	
	#Descriptor 9: losync syncopation of low instruments
	#Descriptor 10: midsync syncopation of mid instruments
	#Descriptor 11: hisync syncopation of hi instruments
	
	
	if len(pattern)%4 == 0:
		salienceprofile=[5,1,2,1,3,1,2,1,4,1,2,1,3,1,2,1,4,1,2,1,3,1,2,1,4,1,2,1,3,1,2,1] #using binary LHL profile
	if len(pattern)%3 == 0:
		salienceprofile=[5,1,2,1,2,1,3,1,2,1,2,1,4,1,2,1,2,1,3,1,2,1,2,1] #using ternary LHL profile

	salow=[0]*len(pattern)
	samid=[0]*len(pattern)
	sahi=[0]*len(pattern)
	
	for s,step in enumerate(lopatt):
		if lopatt[s]==1 and lopatt[(s+1)%len(pattern)]==0: #look for an onset and a silence
			salow[s]=abs(salienceprofile[s]-5) #compute syncpoations for lows
		if midpatt[s]==1 and midpatt[(s+1)%len(pattern)]==0: 
			samid[s]=abs(salienceprofile[s]-5) ##compute syncpoations for mids
		if hipatt[s]==1 and hipatt[(s+1)%len(pattern)]==0: 
			sahi[s]=abs(salienceprofile[s]-5) ##compute syncpoations for his
	 
	losync=sum(salow)
	descriptorvector.append(losync)
	midsync=sum(samid)
	descriptorvector.append(midsync)
	hisync=sum(sahi)
	descriptorvector.append(hisync)
	#print "lopatt",lopatt
	
	#print pattname, salow

	#Descriptor 12: losyness, amount of syncopation in the lows by low density (lowsync/lodcount)
	#Descriptor 13: midsyness, amount of syncopation in the mids by mid density(midsync/middcount)
	#Descriptor 14: hisyness, amount of syncopation in the his by hi density (hisync/hidcount)
	if lodcount != 0:
		losyness=float(losync)/lodcount_r
	else:
		losyness=0
	descriptorvector.append(losyness)
	if middcount != 0:
		midsyness=float(midsync)/middcount_r
	else:
		midsyness = 0
	descriptorvector.append(midsyness)
	if hidcount != 0:
		hisyness=float(hisync)/hidcount_r
	else:
		hisyness=0
	descriptorvector.append(hisyness)
	#print descriptorvector
	
	
	#from here extra descriptors: beat division, polyphonic syncopation, ps by beat, syn by beat by group
	
	#Descriptor 15: beatdiv, divisions of the beat 3 or 4
	if len(pattern)%3 == 0:
		beatdiv=3
	if len(pattern)%4 == 0:
		beatdiv=4
	descriptorvector.append(beatdiv)
	nonsilence=[]
	#Descriptor 16: polysync, polyphonic syncopation based on Witeks formula

	#compute POLYPHONIC SYNCOPATION as proposed by witek et al. 2014
	#iterate through all three patterns and consolidate a non silence pattern with (index, elements, salience)
	for s,step in enumerate(lopatt):
		pack=[]
		if lopatt[s] != 0:
			pack.append('l')
		if midpatt[s] != 0:
			pack.append('m')
		if hipatt[s] != 0:
			pack.append('h')
		if len(pack) != 0:
			nonsilence.append((s,pack, salienceprofile[s])) 

	#print pattname, pattern
	#print pattname, nonsilence
	polysync=[]
	for s, step in enumerate(nonsilence):
		if step[1] != nonsilence[(s+1)%len(nonsilence)][1]: #los dos steps no pueden ser iguales
			#caso del kick vs snare
			if 'l' in step[1] and 'm' in nonsilence[(s+1)%len(nonsilence)][1] and step[2]<= nonsilence[(s+1)%len(nonsilence)][2]:
				#print 'yes', step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+2
				syncpack=step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+2, 'c1'
				polysync.append(syncpack)

			#caso del kick vs hh
			if 'l' in step[1] and 'h' in nonsilence[(s+1)%len(nonsilence)][1] and 'm' not in nonsilence[(s+1)%len(nonsilence)][1] and step[2]<= nonsilence[(s+1)%len(nonsilence)][2]:
				#print 'yes', step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+2
				syncpack=step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+5, 'c2'
				polysync.append(syncpack)

			#caso del sn vs kick
			if 'm' in step[1] and 'l' in nonsilence[(s+1)%len(nonsilence)][1] and step[2]<= nonsilence[(s+1)%len(nonsilence)][2]:
				#print 'yes', step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+2
				syncpack=step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+1, 'c3'
				polysync.append(syncpack)

			#caso del sn vs hh
			if 'm' in step[1] and 'h' in nonsilence[(s+1)%len(nonsilence)][1] and 'l' not in nonsilence[(s+1)%len(nonsilence)][1] and step[2]<= nonsilence[(s+1)%len(nonsilence)][2] :
				#print 'yes', step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+2
				syncpack=step[0], abs(step[2] - nonsilence[(s+1)%len(nonsilence)][2])+5, 'c4'
				polysync.append(syncpack)
		
	#print pattname, nonsilence
	#print pattname, polysync
	totalpolysinc=0
	for s in polysync:
		totalpolysinc=totalpolysinc+s[1]
	#print 'polysync:', polysync, totalpolysinc
	##############end of polyphonic syncopation###############
	descriptorvector.append(totalpolysinc)
	
	#sincopa por beat

	beatsync_lo=[]
	beatsync_mid=[]
	beatsync_hi=[]
	if len(salow)%16==0: #patt binario
		for s in range(len(salow)/4):
			#print s,salow[s*4:(s*4)+4]
			#print sum(salow[s*4:(s*4)+4])
			beatsync_lo.append(sum(salow[s*4:(s*4)+4]))
			beatsync_mid.append(sum(samid[s*4:(s*4)+4]))
			beatsync_hi.append(sum(sahi[s*4:(s*4)+4]))
		#print pattname,beatsync_lo
		#print pattname,beatsync_mid
		#print pattname,beatsync_hi
	if len(salow)%12==0: #patt ternario
		for s in range(len(salow)/3):
			#print s,salow[s*4:(s*4)+4]
			#print sum(salow[s*4:(s*4)+4])
			beatsync_lo.append(sum(salow[s*3:(s*3)+3]))
			beatsync_mid.append(sum(samid[s*3:(s*3)+3]))
			beatsync_hi.append(sum(sahi[s*3:(s*3)+3]))
		#print pattname,beatsync_lo
		#print pattname,beatsync_mid
		#print pattname,beatsync_hi
	
	for b in beatsync_lo:
		descriptorvector.append(b)
	for b in beatsync_mid:
		descriptorvector.append(b)
	for b in beatsync_hi:
		descriptorvector.append(b)
	# print 'salow', salow
	# print 'samid', samid
	# print 'sahi', sahi
	

	#luego los filtramos
	# print len(usefuldescriptors), 'len useful'
	# print len(descriptorvector), 'len dvector'
	# print len(descriptorlist), 'len desc list'
	# print 'dvector', descriptorvector

	# destoerase=[]
	# for num,des in enumerate(descriptorlist):
	# 	#print des,descriptorvector[num+1]
	# 	if des not in usefuldescriptors:
	# 		destoerase.append(num+1)
	# #print 'destoerase', destoerase

	# for n,d in enumerate(destoerase):
	# 	#print destoerase[-n-1]
	# 	descriptorvector.pop(destoerase[-n-1])

	#print 'dvector', descriptorvector
	#descriptorlist=usefuldescriptors	
	
	#este es el final aqui se consolidan todos los descriptores en una sola linea
	

	return(descriptorvector)

def extract(filename, size):
#extract all patterns from a .txt file to a list of patterns
#input the complete file name (absolute or relative to your local directory)
#and the size of the patterns you want to extract
	biglist=[]
	with open(filename) as raw:
	        rawlist=[]
	        for rawline in raw:
	        	#print rawline
	        	rawlist.append(rawline)
	        #print rawlist
	        
	        for index,l in enumerate(rawlist):
	        	line=l[:len(l)-1]
	        	#print line
	        	n= line.split(" ")[0].replace(',','')
	        	#print 'n', n
	        	if n == 'name':
	        		
	        		pattern=[]
	        		length = int(line[len(line)-4:].replace(';',''))#extract the length from the file
	        		#print 'length', length
	        		pattern.append(line[6:len(line)-4]) #append the name of the pattern
	        		#print 'pattern', pattern
	        		
	        		if length > size:
	        			length=size #force everything to be "size" steps


	        		for x in range(length):
	        			#print x,index
	        			rawstep=rawlist[x+1+index][:len(rawlist[x+1+index])-2].split(", ")[1]
	        			
	        			step=rawstep.split(" ")
	        			#print 'step', step 
	        			for i,event in enumerate(step):
	        				#print x, step, event
	        				step[i]=int(event)
	        			# event=int(event)
	        			#print event
	        			# print event.split(", ")
	        			pattern.append(step)
	        		#print pattern
				biglist.append(pattern)
	        # print 'endddd'
	return biglist

def CronbachAlpha(itemscores):
#compute "the expected correlation of two tests that measure the same construct".
#alpha>=0.9 -> excellent, >=0.8->good, >=0.7 ->acceptable, >=0.6 ->questionable
    itemscores = np.asarray(itemscores)
    itemvars = itemscores.var(axis=1, ddof=1)
    tscores = itemscores.sum(axis=0)
    nitems = len(itemscores)

    return nitems / (nitems-1.) * (1 - itemvars.sum() / tscores.var(ddof=1))

descriptorList16=['noi', 'loD', 'midD', 'hiD', 'stepD', 'lowness', 'midness', 'hiness', 
	'lowsync', 'midsync', 'hisync', 'losyness', 'midsyness', 'hisyness', 
	'beatdiv', 'polysync',
	'B1_lo','B2_lo','B3_lo','B4_lo','B1_mid','B2_mid','B3_mid','B4_mid',
	'B1_hi','B2_hi','B3_hi','B4_hi']
	#This is the complete list of descriptors computed in the 'compute' function 

#5th element: 1:kick, 2:snare, 3:ch, 4:oh, 5:rs, 6:cp, 7:lc, 8:hc
GM_dict={
	35:['Acoustic Bass Drum','low',36, 'K', 1],
	36:['Bass Drum 1','low',36, 'K', 1],
	37:['Side Stick','mid',37, 'RS', 6],
	38:['Acoustic Snare','mid',38, 'SN', 2],
	39:['Hand Clap','mid',39, 'CP', 5],
	40:['Electric Snare','mid',38, 'SN', 2],
	41:['Low Floor Tom','low',45, 'LT', 7],
	42:['Closed Hi Hat','high',42, 'CH', 3],
	43:['High Floor Tom','mid',45, 'HT', 8],
	44:['Pedal Hi-Hat','high',46, 'OH', 4],
	45:['Low Tom','low',45, 'LT', 7],
	46:['Open Hi-Hat','high',46, 'OH', 4],
	47:['Low-Mid Tom','',47, 'MT', 7],
	48:['Hi-Mid Tom','',47, 'MT', 7],
	49:['Crash Cymbal 1','',49, 'CC', -1],
	50:['High Tom','',50, 'HT', 8],
	51:['Ride Cymbal 1','',51, 'RC', -1],
	52:['Chinese Cymbal','',52, '', -1],
	53:['Ride Bell','high',53, '', -1],
	54:['Tambourine','high',54, '', -1],
	55:['Splash Cymbal','high',55, '', -1],
	56:['Cowbell','high',56, '', -1],
	57:['Crash Cymbal 2','high',57,'', -1],
	58:['Vibraslap','',58, '',-1],
	59:['Ride Cymbal 2','high',59, '',-1],
	60:['Hi Bongo','high',60, 'LB', 8],
	61:['Low Bongo','mid',61, 'HB', 7],
	62:['Mute Hi Conga','high',62, 'MC', 8],
	63:['Open Hi Conga','high',63, 'HC', 8],
	64:['Low Conga','low',64, 'LC', 7],
	65:['High Timbale','',65, '',8],
	66:['Low Timbale','',66, '',7],
	67:['High Agogo','',67, '',-1],
	68:['Low Agogo','',68,'',- 1 ],
	69:['Cabasa','high',70, 'MA',-1],
	70:['Maracas','high',70, 'MA',-1],
	71:['Short Whistle','',71,'',-1],
	72:['Long Whistle','',72,',-1'],
	73:['Short Guiro','',73,'',-1],
	74:['Long Guiro','',74,'',-1],
	75:['Claves','',75,'',-1],
	76:['Hi Wood Block','high',76,'',8],
	77:['Low Wood Block','low',77,'',7],
	78:['Mute Cuica','',78,'',-1],
	79:['Open Cuica','',79,'',-1],
	80:['Mute Triangle','',80,'',-1],
	81:['Open Triangle','',81,'',-1],
	}

""" Computes the Fleiss' Kappa value as described in (Fleiss, 1971) """

combo2l8={
	#this is a function to convert a list of 4 numbers to a letter.
	#to be used with DrMarkov
	 '[0]': 'a',
	 '[1]': 'b',
	 '[2]': 'c',
	 '[1, 2]': 'd',
	 '[3]': 'e',
	 '[1, 3]': 'f',
	 '[2, 3]': 'g',
	 '[1, 2, 3]': 'h',
	 '[4]': 'i',
	 '[1, 4]': 'j',
	 '[2, 4]': 'k',
	 '[1, 2, 4]': 'l',
	 '[3, 4]': 'm',
	 '[1, 3, 4]': 'n',
	 '[2, 3, 4]': 'o',
	 '[1, 2, 3, 4]': 'p'
	}

def fleissKappa(mat):
    """ Computes the Kappa value
    	https://en.wikibooks.org/wiki/Algorithm_Implementation/Statistics/Fleiss'_kappa
        @param n Number of rating per subjects (number of human raters)
        @param mat Matrix[subjects][categories]
        @return The Kappa value """
    DEBUG = True
    n = checkEachLineCount(mat)   # PRE : every line count must be equal to n
    N = len(mat)
    k = len(mat[0])
    
    if DEBUG:
        print n, "raters."
        print N, "subjects."
        print k, "categories."
    
    # Computing p[]
    p = [0.0] * k
    for j in xrange(k):
        p[j] = 0.0
        for i in xrange(N):
            p[j] += mat[i][j]
        p[j] /= N*n
    if DEBUG: print "p =", p
    
    # Computing P[]    
    P = [0.0] * N
    for i in xrange(N):
        P[i] = 0.0
        for j in xrange(k):
            P[i] += mat[i][j] * mat[i][j]
        P[i] = (P[i] - n) / (n * (n - 1))
    if DEBUG: print "P =", P
    
    # Computing Pbar
    Pbar = sum(P) / N
    if DEBUG: print "Pbar =", Pbar
    
    # Computing PbarE
    PbarE = 0.0
    for pj in p:
        PbarE += pj * pj
    if DEBUG: print "PbarE =", PbarE
    
    kappa = (Pbar - PbarE) / (1 - PbarE)
    if DEBUG: print "kappa =", kappa
    
    return kappa

def checkEachLineCount(mat):
    """ Assert that each line has a constant number of ratings
        @param mat The matrix checked
        @return The number of ratings
        @throws AssertionError If lines contain different number of ratings """
    n = sum(mat[0])
    
    assert all(sum(line) == n for line in mat[1:]), "Line count != %d (n value)." % n
    return n

def icc(mat, icc_type='icc2'):
    ''' Calculate intraclass correlation coefficient for data within Brain_Data class
    
    ICC Formulas are based on:
    Shrout, P. E., & Fleiss, J. L. (1979). Intraclass correlations: uses in assessing rater reliability. 
    Psychological bulletin, 86(2), 420.

    icc1:  x_ij = mu + beta_j + w_ij
    icc2/3:  x_ij = mu + alpha_i + beta_j + (ab)_ij + epsilon_ij

    Code modifed from nipype algorithms.icc
    https://github.com/nipy/nipype/blob/master/nipype/algorithms/icc.py
    
    Args:
        icc_type: type of icc to calculate (icc: voxel random effect, icc2: voxel and column random effect, icc3: voxel and column fixed effect)

    Returns:
        ICC: intraclass correlation coefficient

    '''
    
    Y = mat.T
    [n, k] = Y.shape

    # Degrees of Freedom
    dfc = k - 1
    dfe = (n - 1) * (k-1)
    dfr = n - 1

    # Sum Square Total
    mean_Y = np.mean(Y)
    SST = ((Y - mean_Y) ** 2).sum()

    # create the design matrix for the different levels
    x = np.kron(np.eye(k), np.ones((n, 1)))  # sessions
    x0 = np.tile(np.eye(n), (k, 1))  # subjects
    X = np.hstack([x, x0])

    # Sum Square Error
    predicted_Y = np.dot(np.dot(np.dot(X, np.linalg.pinv(np.dot(X.T, X))), X.T), Y.flatten('F'))
    residuals = Y.flatten('F') - predicted_Y
    SSE = (residuals ** 2).sum()

    MSE = SSE / dfe

    # Sum square column effect - between colums
    SSC = ((np.mean(Y, 0) - mean_Y) ** 2).sum() * n
    MSC = SSC / dfc / n
    
    # Sum Square subject effect - between rows/subjects
    SSR = SST - SSC - SSE
    MSR = SSR / dfr

    if icc_type == 'icc1':
        # ICC(2,1) = (mean square subject - mean square error) / (mean square subject + (k-1)*mean square error + k*(mean square columns - mean square error)/n)
        # ICC = (MSR - MSRW) / (MSR + (k-1) * MSRW)
        NotImplementedError("This method isn't implemented yet.")
        
    elif icc_type == 'icc2':
        # ICC(2,1) = (mean square subject - mean square error) / (mean square subject + (k-1)*mean square error + k*(mean square columns - mean square error)/n)
        ICC = (MSR - MSE) / (MSR + (k-1) * MSE + k * (MSC - MSE) / n)

    elif icc_type =='icc3':
        # ICC(3,1) = (mean square subject - mean square error) / (mean square subject + (k-1)*mean square error)
        ICC = (MSR - MSE) / (MSR + (k-1) * MSE)

    return ICC

def correlationRank(mat):
#compute the correlation rank according to this article
#https://en.wikipedia.org/wiki/Inter-rater_reliability#Correlation_coefficients
#it is based on spearman rank correlation
#the general idea is to compute the agreement (Spearman) between each possible pair of raters
#and then take a mean from that. 

	#we assume that questions are rows and raters are columns
	#and that mat is a nupi array

	#we want to test how each rater (columns) correlates with the rest.
	rater_N=mat.shape[1]
	raters_correlations=[]
	for rater1 in range(rater_N):
		rater_correlations=[]
		for rater2 in range(rater_N):
			if rater1 != rater2:
				rating1 = mat[:,rater1]
				rating2 = mat[:,rater2]
				#print rating1, rating2, stats.spearmanr(rating1,rating2)
				rater_correlations.append(stats.spearmanr(rating1,rating2)[0])
		#print rater1, np.mean(rater_correlations)
		raters_correlations.append(np.mean(rater_correlations))
	return raters_correlations

def stress(m1,m2):
#compute the stress between two matrices of equal dimension
#if they have different dimensions i.e. != number of columns
#then fill extra columns with zeroes
	m1=np.matrix((m1))
	m2=np.matrix((m2))
	if np.shape(m1)==np.shape(m2):
		s=np.sqrt(abs(m1-m2))
		stress = sum(sum(s))
	else:
		if np.shape(m1)[1]<np.shape(m2)[1]:
			z=np.zeros((np.shape(m1)[0],np.shape(m1)[1]+(np.shape(m2)[1]-np.shape(m1)[1])))
			z[:,:-1] = m1
			s=np.sqrt(abs(z-m2))
			stress = np.sum(s)
		else:
			z=np.zeros((np.shape(m2)[0],np.shape(m2)[1]+(np.shape(m1)[1]-np.shape(m2)[1])))
			z[:,:-1] = m2
			s=np.sqrt(abs(z-m1))
			stress = np.sum(s)

	return stress

def GM2name(midi):
	#This function converts a MIDI number to the name of teh instrument
	return GM_dict[midi][0]

def GM2shortname(midi):
	#This function converts a MIDI number to the name of teh instrument
	return GM_dict[midi][3]

def GM2Group(midi):
	#This function converts a MIDI number to the instrumental group
	return GM_dict[midi][1]

def GMmap(midi):
	#this function receives a midi note and converts it to a simplified map.
	#In thismap we have only 1 kick, 1 snare, open or closed hihat... 1 tom etc
	#this is used to commply GM drums with a machine drum

	return GM_dict[midi][2]

def GM2eight(midi):
	#This funciotn receives a MIDI note number and outputs a remapped version of it 
	#to fit the Dr.Drums achitecture of 8 instrument drum patterns
	return GM_dict[midi][4]

def loadPatterns(name,pattlength):
#organize all patterns from .txt in a list of lists. each sublist is a pattern with sublist[0]=name

	biglist=[]
	with open(name) as raw:
	        rawlist=[]
	        for rawline in raw:
	        	#print rawline
	        	rawlist.append(rawline)
	        #print rawlist
	        
	        
	        for index,l in enumerate(rawlist):
	        	line=l[:len(l)-1]
	        	n= line.split(" ")[0].replace(',','')
	        	#print i, n
	        	if n == 'name':
	        		
	        		pattern=[]
	        		length = int(line[len(line)-4:].replace(';',''))
	        		#print 'length', length
	        		pattern.append(line[6:len(line)-4])
	        		#print pattern
	        		
	        		for x in range(pattlength): #we are going to force the length to a specific length in steps (i.e. 16)
	        		#for x in range(length):
	        			#print x,index
	        			
	        			rawstep=rawlist[x+1+index][:len(rawlist[x+1+index])-2].split(", ")[1]
	        			
	        			step=rawstep.split(" ")
	        			#print step 
	        			for i,event in enumerate(step):
	        				step[i]=int(event)
	        			# event=int(event)
	        			#print event
	        			# print event.split(", ")
	        			pattern.append(step)
	        		#print pattern
				biglist.append(pattern)
	        # print 'endddd'
	return biglist

def patts2Mtx(listofpatts):
#use this function to take a list of pattens and compute all descriptors from those patterns
	mtx=[]
	names=[]
	for pattern in listofpatts:
		mtx.append(compute(pattern)[1:])
		names.append(compute(pattern)[0])
	mtx=np.matrix(mtx)
	return names,mtx

def lassoMatch(target,data, alpha):
#compute a regression and find the most important descriptors to reach a target

	names=[0] #the names are the link between the target and the matrix of descriptors
	descriptormtx=[]
	coordinates=[] #here we will store the coordinates of each pattern
	output=[]
	#now make sure that the order of descriptormtx is the same as the order of target
	#and use also the iteration to cerate a list only with coordinates
	#the lasso regresion will be done for each axis (number of elements in the coordinates)
	for p in target:
		for n,name in enumerate(data[0]):
			if p[0]==data[0][n]:
				mtrx=data[1][n]
				mtrx=mtrx.tolist()
				mtrx=[x for x in mtrx]
				descriptormtx.append(mtrx[0])
		coordinates.append(p[1:])

	#x=np.array(descriptormtx)
	x=np.array(descriptormtx)
	x = x / x.max(axis=0) #divide each axis by the maximum value so all descriptors range go from 0 to 1
	
	#compute a lasso regression for each axis
	for axis in range(len(coordinates[0])):
		lassoresult=[]
		y=[]#this is going to be the target for this axis
		#print 'computing axis', axis
		for value in coordinates:
			y.append(value[axis])
		y=np.array(y)
		#perform the lasso analysis
		clf = linear_model.Lasso(alpha=alpha, copy_X=True, fit_intercept=True, 
			max_iter=1000, normalize=True, positive=False, precompute=False, tol=0.0001, warm_start=False)
		
		clf.fit(x,y)
		lassocoeffs=clf.coef_

		#make a list with the descriptors that were used
		for n,coef in enumerate(lassocoeffs):
			if coef != 0:
				lassoresult.append([descriptorList16[n],coef])
		#print 'axis',axis+1, lassoresult

		lassoforecast=np.dot(x,lassocoeffs) #make a forecast using the descriptors

		#print 'Spearman correlation:',stats.spearmanr(y,lassoforecast)[0], 'p value:', stats.spearmanr(y,lassoforecast)[1]
		#finally report the lasso results
		#print ''
		onlydescriptors=[q[0] for q in lassoresult]
		onlyweights=[q[1] for q in lassoresult]

		output.append([onlydescriptors,onlyweights,stats.spearmanr(y,lassoforecast)])


	return output

def lassoMatchSelect(target,data,desclista, alpha):
#compute a regression and find the descriptors that are useful for reaching a target
#using only specified descriptors in a list

	names=[0] #the names are the link between the target and the matrix of descriptors
	descriptormtx=[]
	coordinates=[] #here we will store the coordinates of each pattern
	output=[]
	filteredmtx=[]
	finaldescriptorlist=list(descriptorList16) #start with a complete list of descriptors copied from this original list
	#filter out the descriptors we do ont want from the descriptors in "data"
	#"data" has a list of pattern names and then a numpy matrix of descriptors
	#all descriptors in "data" have been computed by compute so we know the list
	#which is "descriptorList16". each column of data is a name from descriptorlist.
	#filter out the columns that are NOT part of descriptorlist16
	
	coltodelete=[] #list of columns to delete
	for c,d in enumerate(descriptorList16):
	 	if d not in desclista:
	 		#print "d",d, "desclista", desclista
	 		coltodelete.append(c)

	#print "coltodelete",coltodelete
	filteredmtx=data[1] #this is the resulting matrix after erasing unused descriptors
	for n,c in enumerate(coltodelete):
		filteredmtx=np.delete(filteredmtx,c-n,1)
		del finaldescriptorlist[c-n]
	#print"filteredmtx", filteredmtx
	#print "fdl",finaldescriptorlist
	#now make sure that the order of descriptormtx is the same as the order of target
	#and use also the iteration to cerate a list only with coordinates
	#the lasso regresion will be done for each axis (number of elements in the coordinates)
	for p in target:
		for n,name in enumerate(data[0]):
			if p[0]==data[0][n]:
				mtrx=filteredmtx[n]
				mtrx=mtrx.tolist()
				mtrx=[x for x in mtrx]
				descriptormtx.append(mtrx[0])
		coordinates.append(p[1:])
	#print "descriptormtx",descriptormtx
	#x=np.array(descriptormtx)
	x=np.array(descriptormtx)
	x = x / x.max(axis=0) #divide each axis by the maximum value so all descriptors range go from 0 to 1
	
	#compute a lasso regression for each axis
	for axis in range(len(coordinates[0])):
		lassocoeffs=[]
		lassoresult=[]
		y=[]#this is going to be the target for this axis
		#print 'computing axis', axis
		for value in coordinates:
			y.append(value[axis])
		y=np.array(y)
		#perform the lasso analysis
		clf = linear_model.Lasso(alpha=alpha, copy_X=True, fit_intercept=True, 
			max_iter=1000, normalize=True, positive=False, precompute=False, tol=0.0001, warm_start=False)
		
		clf.fit(x,y)
		lassocoeffs=clf.coef_
		#make a list with the descriptors that were used
		#print 'lassocoeffs', lassocoeffs
		for n,coef in enumerate(lassocoeffs):
			if coef != 0:
				#print "index",n
				lassoresult.append([finaldescriptorlist[n],coef])
		#print 'axis',axis+1, lassoresult

		lassoforecast=np.dot(x,lassocoeffs) #make a forecast using the descriptors

		#print 'Spearman correlation:',stats.spearmanr(y,lassoforecast)[0], 'p value:', stats.spearmanr(y,lassoforecast)[1]
		#finally report the lasso results
		#print ''
		onlydescriptors=[q[0] for q in lassoresult]
		onlyweights=[q[1] for q in lassoresult]

		output.append([onlydescriptors,onlyweights,stats.spearmanr(y,lassoforecast)])


	return output

def patts2space(targetCoords,patts,desclista):
#input a set of patterns with coordinates, the list representation of the patterns,
#a list of descriptors and create MDS and PCA spaces
	
	#compute all descriptors
	descmatrix=patts2Mtx(patts)
	#filter the columns of descriptors with the desclista
	
	finaldescriptorlist=list(descriptorList16) #start with a complete list of descriptors copied from this original list
	#filter out the descriptors we do ont want from the descriptors in "data"
	#"data" has a list of pattern names and then a numpy matrix of descriptors
	#all descriptors in "data" have been computed by compute so we know the list
	#which is "descriptorList16". each column of data is a name from descriptorlist.
	#filter out the columns that are NOT part of descriptorlist16
	
	coltodelete=[] #list of columns to delete
	for c,d in enumerate(descriptorList16):
	 	if d not in desclista:
	 		#print "d",d, "desclista", desclista
	 		coltodelete.append(c)

	#print "coltodelete",coltodelete
	filteredmtx=descmatrix[1] #this is going to be the resulting matrix after erasing unused descriptors
	
	#print "filteredmtx", filteredmtx
	for n,c in enumerate(coltodelete):
		#print "filteredmtx",filteredmtx
		filteredmtx=np.delete(filteredmtx,c-n,1) #erase columns
		del finaldescriptorlist[c-n]

	#use the resulting matrix of descriptors to compute PCA
	## first normalize
	#filteredmtx=np.array(filteredmtx) #convert to numpy
	
	filteredmtx = filteredmtx / filteredmtx.max(axis=0) #normalize
	


	pca = PCA(n_components=2)
	pca.fit(filteredmtx)
	PCA(copy=True, n_components=2)
	X = pca.transform(filteredmtx)
	#print 'X',X
	########plot the patterns in 2D based on the PCA
	#print 'coordenadas de cada punto:'
	#print X

	#print "patts",patts
	listofpatterns=[x[0] for x in patts]

	axis1_list=[]
	axis2_list=[]
	#print 'lop', listofpatterns

	for n, element in enumerate(X):
		axis1_list.append((listofpatterns[n],element[0]))
		axis2_list.append((listofpatterns[n],element[1]))

	#print 'axis1',axis1_list
	#print 'axis2',axis2_list 
	#compute the correlation with each axis of the targetCoords
	
	xtarget=[x[1] for x in targetCoords]
	ytarget=[x[2] for x in targetCoords]
	xforecast=[x[0] for x in X]
	yforecast=[x[1] for x in X]
	#collect stats
	pcadata=[X,stats.spearmanr(xtarget,xforecast), stats.spearmanr(ytarget,yforecast)]
	
	############################MDS##########################
	#use the resulting matrix of descriptors to compute MDS
	distances=np.zeros([len(filteredmtx), len(filteredmtx)]) #create an empty matrix with cols and rows = number of patts

	for n,p in enumerate(filteredmtx):
		for nn,pp in enumerate(filteredmtx):
			distances[n,nn]=np.linalg.norm(filteredmtx[n]-filteredmtx[nn])

	####now copmpute the mds
	seed = np.random.RandomState(seed=3)
	mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
	mdspos = mds.fit(distances).embedding_
	#perform pcs on the mds resulting data
	clf = PCA(n_components=2)
	mdspos = clf.fit_transform(mdspos)

	#print mdspos

	xmds=[x[0] for x in mdspos]
	ymds=[x[1] for x in mdspos]

	#compute the correlation with each axis of the targetCoords
	mdsdata=[mdspos,stats.spearmanr(xtarget,xmds), stats.spearmanr(ytarget,ymds)]
	return pcadata, mdsdata

def heatmap(pattern):
#draw a heatmap of a pattern in list format: [name of the pattern,[[36,38],[]]]
#the argument is the list and an optional argument of the size of te plot
	pattoplot=[]
	#GMD=generalMIDIdrum()
	hepa=[]    
	foundinstr=[]
	instrnames=['nothing']

	for step in pattern[1:]:
	    for e in step:
	        foundinstr.append(int(e))
	foundinstr=list(set(foundinstr))
	

	if 0 in foundinstr:
	    foundinstr.remove(0)
	foundinstr.sort()

	#print 'lista de instrumentos:', foundinstr
	for n,x in enumerate(foundinstr):
	    instrnames.append(GM2shortname(x)) #get the name of the instrument from the dictionary

	for instrument in foundinstr:
	    instrsequence=[]
	    #print 'instrument', instrument
	    instrsequence.append(instrument)
	    iseq=[]
	    for step in pattern[1:]:
	        #event=[]
	        #event=splitstring(step,2)
	        #print instrument, event
	            
	        if instrument in step:
	            iseq.append(1)
	            #print 'match'
	        else:
	            iseq.append(0)
	    #print 'instrument and sequence',GM2name(instrument), iseq
	    instrsequence.append(iseq)

	    # heat[int(instrument)] = totallist
	    hepa.append(instrsequence)
	#print"hepa", hepa

	a=np.zeros(len(iseq))

	for key,value in enumerate(hepa):
	    a=np.vstack((a,value[1]))        
	column_labels= instrnames
	#print column_labels
	row_labels = list(range(len(iseq)+1))[1:]

	fig, ax = plt.subplots()
	a=a[:,:16]
	heatmap = ax.pcolor(a, edgecolors='w', linewidths=1, cmap=plt.cm.Blues)

	ax.set_xticks(np.arange(a.shape[1])+0.5, minor=False)
	ax.set_yticks(np.arange(a.shape[1])+0.5, minor=False)

	ax.set_xticklabels(row_labels, fontsize=10)
	ax.set_yticklabels(column_labels, fontsize=10)
	#print 'columnlabels', ax
	#remove middle ticks
	for t in ax.xaxis.get_major_ticks():
	    t.tick1On = False
	    t.tick2On = False
	for t in ax.yaxis.get_major_ticks():
	    t.tick1On = False
	    t.tick2On = False
	tit=pattern[0].split('_')[0]
	fig.suptitle(tit, fontsize=20, position=(0.53,0.92))
	fig.set_size_inches(6, 3, forward=True)
	plt.subplots_adjust(top = 0.8, bottom = 0.4, left = 0.17)
	pylab.xlim([0,16])
	pylab.ylim([1,a.shape[0]])

	ax.set_aspect('equal')

	#comment plot and show
	#fig.savefig('styles/'+style+'/extractedpatt_'+str(png)+'.i')
	plt.show()
	return()

def makestyle(lista, length, folder,stylename):
#create "style knowledge" useful in Dr.Drums based on a specific collection of patterns.
#The collection can be in a .txt file or as .mid files.
#The output is a bunch of .txt files approproate for Dr.Drums to use.


	orders=range(10)
	length=16
	stylename=stylename
	folder='styles'

	#start from a list of lists where the first element of the sublist is the name of the pattern and the next 
	#are lists of onsets at each step

	tnoname=[y[1:] for y in lista]
	#print tnoname
	#t_allsteps=[]
	allsteps2l=[]
	for p in tnoname:
		for step,s in enumerate(p):
			#t_allsteps.append(s)
			#print s
			s2eight=[]
			for m in s:
				if m != 0:
					s2eight.append(GM2eight(m)) #Remap all MIDI notes to only 8 instruments (-1 if instrument not mapable)
				else:
					s2eight.append(0) #if the step is empty append a 0
			lowpack=[]
			hipack=[]
			for n in s2eight: # divide the event in the step into 2 lists of 4 numbers (lowpack and hipack)
				if n != -1:
					if n < 5:
						lowpack.append(n)
					else:
						hipack.append(n-4)
			if len(hipack)==0:
				hipack.append(0)
			if len(lowpack)==0:
				lowpack.append(0)
			hipack=set(hipack)
			lowpack=set(lowpack)
			hipack=sorted(hipack)
			lowpack=sorted(lowpack)
			#print str(lowpack), str(hipack)
			#print step, rtb.combo2l8[str(lowpack)]+rtb.combo2l8[str(hipack)]
			allsteps2l.append(combo2l8[str(lowpack)]+combo2l8[str(hipack)]) # here we have a list of steps with max 8 instruments
	
	

	#from here on is the process of wrapping and creating the styles
	for order in orders:
		for index in range(length):
			fileout = open(folder+'/'+stylename+'-'+str(order)+'-'+str(index), "w")
			totalpatts=len(allsteps2l)/length
			stepdict={}
			print >>fileout, "order,", str(order)+";"
			print >>fileout, "step,", str(index)+";"
			
			for patt in range(totalpatts):
				#patt es el patron que queremos explorar(zero based)
				nuindex= index+length*patt
				nuend=length*patt
				past=[]
				for o in range(order):
					past.append(allsteps2l[((index-o-1)%length)+(patt*length)])
				past.reverse()
				past="".join(str(x) for x in past)
				#print nuindex, past,allsteps2l[nuindex]
				#now make a summary of the pasts
				if past not in stepdict:
					stepdict[past]=[allsteps2l[nuindex]]
				else:
					stepdict[past].append(allsteps2l[nuindex])
			for key, value in stepdict.iteritems():
				lc=Counter(value)
				pastout=[]
				for k,v in lc.iteritems():
					pastout.append([k,float(v)/len(lc)])
				#pastout=" ".join(str(x) for x in pastout)	
				line=[item for sublist in pastout for item in sublist]
				line=" ".join(str(x) for x in line)
				print >>fileout, key+',',str(line)+';'
			fileout.close()
	return 

def rs_gen(listofpatterns):
# use this function to generate a rhythm space given a set of patterns.
# we will use the methodology described in the paper (in print)
# For each pattern extract the descriptors found experimentally as a vector, normalize each column of descriptors,
# measure eucliedan distance, create a symetric matrix, compute MDS, get the 2D coordinates of each pattern.

	rsDesc=['lowsync', 'midD', 'hisyness', 'hiD', 'hiness', 'stepD', 'noi'] #the set of descriptors to be extracted form the patterns
	#rsDescIdx=[8,2,13,3,7] #the indexes of the only descriptors we want to use
	descmatrix=patts2Mtx(listofpatterns) # compute all descriptors
	finaldescriptorlist=list(descriptorList16) # make list with all descriptors
	coltodelete=[] # empty list to save the columns to delete
	for c,d in enumerate(descriptorList16): #iterate all descriptors
	 	if d not in rsDesc:
	 		coltodelete.append(c) #make a list of columns to delete
	filteredmtx=descmatrix[1] #this is going to be the resulting matrix after erasing unused descriptors
	for n,c in enumerate(coltodelete): # iterate columns to delete and delete
		#print "filteredmtx",filteredmtx
		filteredmtx=np.delete(filteredmtx,c-n,1) #erase columns
		del finaldescriptorlist[c-n]
	filteredmtx = filteredmtx / filteredmtx.max(axis=0) #normalize the filtered matrix
	############################MDS##########################
	#use the resulting matrix of descriptors to compute MDS
	distances=np.zeros([len(filteredmtx), len(filteredmtx)]) #create an empty matrix with cols and rows = number of patts
	for n,p in enumerate(filteredmtx): #iterate every row of the descriptor matrix and compute distance
		for nn,pp in enumerate(filteredmtx):
			distances[n,nn]=np.linalg.norm(filteredmtx[n]-filteredmtx[nn]) #save in matrix
	seed = np.random.RandomState(seed=3) #parameters of the MDS
	mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
	mdspos = mds.fit(distances).embedding_ #get positions using MDS
	clf = PCA(n_components=2) #setup PCA
	mdspos = clf.fit_transform(mdspos) #Rotate points using PCA to achieve better alignment

	names =[x[0] for x in listofpatterns] #make list of names
	return names,mdspos

def rs_plot(names,coords,title):
#this function receives a list of names and a list of 2D coords and plots each point in space with its name
	x=coords.T[0]
	y=coords.T[1]
	area=10
	colors='r'
	
	for i,name in enumerate(names):
		plt.annotate(name,(x[i],y[i]), size=10, color='grey', alpha=0.5)
	plt.suptitle(title)
	plt.scatter(x, y, s=area, c=colors, alpha=1)
	plt.show()

	return

def midifolder2list(foldername):
# this function converts all midi files in a folder into lists
# the idea is that this list is fed to the makestyle function.
# this function looks for a local folder named /midi and then 
# for a subfolder which is called from the function
	allpatterns=[]
	allfiles=os.listdir("midi/"+foldername)
	for filename in allfiles: # store in filename the name of each of the files
		#print filename 


		mid=mido.MidiFile("midi/"+foldername+"/"+filename)

		#time: inside a track, it is delta time in ticks. A delta time is how long to wait before the next message. This must be an integer

		acc=0
		for i, track in enumerate(mid.tracks):
			grid={}
		    #print('Track {}: {}'.format(i, track.name))
			for msg in track:
				useful=str(msg)
				#print useful[0]
				if useful[0]!='<':
					
					note=int(useful.split()[2][5:7])
					acc=msg.time+acc
					if msg.type is 'note_on':
						temp=[]
						if acc/24 in grid:

							temp=grid[acc/24]
							temp.append(note)
							grid[acc/24]=temp
						else:
							temp.append(note)
							#print type(note),temp, note
							grid[acc/24]=temp
		#print grid
		steps=list(grid.keys())
		totalsteps= ((max(steps)/16)+1)*16 #find the rounded length in steps of 1/16th notes
		for x in range(totalsteps):
			if grid.get(x) == None:
				grid[x]=[0]
		#	print x,grid.get(x)
		onsets=list(grid.values())
		#print foldername+'_'+filename,onsets
		onsets.insert(0,foldername+'_'+filename)
		allpatterns.append(onsets)
	return allpatterns





