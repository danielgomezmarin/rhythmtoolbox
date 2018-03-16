
This toolbox is produced in the context of my PhD research on drum rhythm analysis and generation, where I found the need to process, model and test different aspects of drum rhythm datasets. Perhaps one of the main contributions of this toolbox is the possibility to compute descriptors for symbolic drum patterns, which are the result of a theoretical and experimental approach to drum rhythm study based on polyphonic rhythm perception and cognition studies (see section 3.4 of my thesis https://drive.google.com/open?id=1Z5Wn5VkWI3Tov16frWZYOt6sr8p_ASIs).


This toolbox is composed of two files, **_rhythmtoolbox.py_** and **_rhythmtoolbox-examples.py_**. The rhythmtoolbox.py file is a Python script compiling many different functions used to parse rhythms form MIDI files, load collections of rhythms, extract symbolic descriptors, quantify process and visualize the data. These functions are explained below. In order to improve the usefulness of this library  I have created a help file called rhythmtoolbox-examples.py where different procedures are exemplified, based on the functions in the rhythmtoolbox.py script.

The philosophy behind the functions in the toolbox is to take low level processing behind the scenes so that the actual processing can be based on very few lines of code. It is based on very common Python libraries, specifically  numpy, scipy, sklearn, matplotlib, pylab, collections, mido and os.

## List of functions:
**compute(pattern)**
Compute a set of rhythmic descriptors for one polyphonic pattern. A pattern must be a list of lists: the fists element is the name of the pattern, the other elements are lists, each list is a 16th step of the pattern. Each of this lists contains MIDI numbers of the onsets present on that step. For a theoretical explanation on these descriptors see section 3.4 of my thesis https://drive.google.com/open?id=1Z5Wn5VkWI3Tov16frWZYOt6sr8p_ASIs.

The descriptors computed are
- noi: number of instruments.
- loD, midD, hiD: The total number of onsets (density) in the three different frequency streams: low, mid and high.
- stepD: The percentage of the steps in the pattern that have onsets.
- lowness, midness, hiness: The densities of the different frequency streams divided by the number of steps that contain onsets.
- lowsync, midsync, hisync: syncopation value of each frequency stream.
- losyness, midsyness, hisyness: The syncopation value of each frequency stream divided by the number of onsets on that stream.
- beatdiv: the divisions of the beat (only ternary or binary).
- polysync: the polyphonic syncopatino value computed after Witek et al (http://journals.plos.org/plosone/article/file?type=supplementary&id=info:doi/10.1371/journal.pone.0094446.s012)


**extract(filename, size)**
Extract all patterns from a .txt file to a list of patterns. Input the complete filename (absolute or relative to your local directory)
and the size of the patterns you want to extract. This is useful when the symbolic patterns are represented as a list of lists. Each sublist representing the onsets present at each step, and a 0 if the step is silent.


**CronbachAlpha(itemscores)**
Compute the expected correlation of two tests that measure the same construct.


**fleissKappa(mat)**
Computes the Kappa value https://en.wikibooks.org/wiki/Algorithm_Implementation/Statistics/Fleiss'_kappa.

**correlationRank(mat)**
Compute the correlation rank according to this article https://en.wikipedia.org/wiki/Inter-rater_reliability#Correlation_coefficients
It is based on spearman rank correlation, computing the agreement (Spearman) between each possible pair of raters and then take a mean from that.

**stress(m1,m2)**
Compute the stress between two matrices of equal dimension, if they have different dimensions i.e. != number of columns then fill extra columns with zeros.

**GM2name(midi)**
This function converts a MIDI instrument number to the General MIDI Level 1 Percussion Key Map name of the instrument.


**GM2shortname(midi)**
This function converts a MIDI instrument number to a single letter name based on the General MIDI Level 1 Percussion Key Map of the instrument.

**GM2Group(midi)**
This function converts each MIDI instrument number based on the General MIDI Level 1 Percussion Key Map to an instrumental group, mapping it to Low, Mid or High.

**GMmap(midi)**
This function receives a midi note and converts it to a simplified mapping of only 8 possible outputs: kick, snare, clap, rimshot, closed hihat, open hihat, low conga, high conga symbolized by single letters.


**GM2eight(midi)**
This function receives a MIDI note number and outputs a remapped version of it to fit the Dr.Drums architecture of 8 instrument drum patterns. The output is a number from 1 to 8.

**loadPatterns(name,pattlength)**
Parse all patterns in a .txt file in the format of a list of lists. each sublist is a pattern with sublist[0]=name.

**patts2Mtx(listofpatts)**
Use this function to take a list of patterns and compute all descriptors from those patterns.

**lassoMatch(target,data, alpha)**
Compute a Lasso regression and find the most important descriptors to reach a target.

**lassoMatchSelect(target,data,desclista, alpha)**
Compute a Lasso regression and find the descriptors that are useful for reaching a target, using only specified descriptors in a list.

**patts2space(targetCoords,patts,desclista)**
Input a set of patterns with coordinates, the list representation of the patterns, a list of descriptors and create MDS and PCA spaces.

**heatmap(pattern)**
Draw a heatmap of a long pattern in list format: [name of the pattern,[[36,38],[]],...]. The argument is the list and an optional argument of the size of the plot. This is useful to plot a group of patterns condensed in a single view, where a cell (instrument, step) has a color depending on the recurrence of finding onsets of that instrument in hat same step.

**makestyle(lista, length, folder,stylename)**
This function analyzes a collection of patterns to extract style knowledge from it. This "style knowledge" used for generative purposes in the generative drum sequencer called Dr.Drums, also developed as part of this thesis. The collection of patterns used as input can be in a .txt file or as .mid files. The output is a bunch of .txt files appropriate for Dr.Drums to use.

*rs_gen(listofpatterns)*
Use this function to generate a rhythm space given a set of patterns. The methodology is described in the CMMR 2017 paper (http://bit.ly/2IutMbF). For each pattern extract the useful descriptors (found experimentally as described in the paper) as a vector, normalize each column of descriptors, measure Euclidean distance, create a symmetric matrix, compute MDS, get the 2D coordinates of each pattern.


*rs_plot(names,coords,title)*
This function receives a list of names and a list of 2D coords and plots each point in space with its name.

*midifolder2list(foldername)*
This function converts all midi files in a folder into lists. The idea is that this list is fed to the makestyle function. This function looks for a local folder named /midi and then for a subfolder which is called from the function.


