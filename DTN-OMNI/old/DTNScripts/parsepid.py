#!/usr/bin/python
################################################################################################
# Python script for parsing process identifiers from dtn log files.
#
# Usage:  parsepid.py [filename]
#
#         file-name is the dtn log input file to parse.
#         output is written to pid.csv file in local directory.
#
# Note:  if no file name is specified, it is assumed to be console.log 
#        in the current directory.
#
################################################################################################


# Included packages.
import sys;          # System.
import re;           # Regular expressions.
from collections import defaultdict;  # Dictionary.


# Pid description class.
class PidDescription:
   pid = "";
   description = "";


# Setup some general variables.
pidFileName = "console.log";
outputFileName = "pid.csv";
pidResultList = list ();
pidIndex = 6;
descriptionIndex = 2;


# Setup the regular expression patterns to match.
mwbPattern = re.compile('MWB');
pidPattern = re.compile('pid');


# Get the top input file to parse.
args = len (sys.argv);
if (args > 1):
   pidFileName = sys.argv[1];


#######################################
# Parse the file contents.
#######################################
# Open the pid log file.
pidFile = open (pidFileName);

# Walk the file contents.
for currentLine in pidFile:
   # Look for the MWB string.
   if (mwbPattern.search (currentLine) is not None):
      # Look for the pid pattern.
      if (pidPattern.search (currentLine) is not None):
         # Split the string into tokens.
         tokenList = currentLine.split ();
         # Extract the pid and its description.
         pid = tokenList[pidIndex];
         description = tokenList[descriptionIndex];
         # Store the results.
         temp = PidDescription ();
         temp.pid = pid;
         temp.description = description;
         pidResultList.append (temp);

#Close the file.
pidFile.close ();


#######################################
# Write the results to a CVS file.
#######################################
# Open the output file for writing.
outputFile = open (outputFileName, 'w');

# Write the pid information.
for pid in pidResultList:
   outputFile.write (pid.pid + '\t' + pid.description + '\n');

# Close the output file.
outputFile.close ();


###########
# Done.
###########
print ("Completed.");

