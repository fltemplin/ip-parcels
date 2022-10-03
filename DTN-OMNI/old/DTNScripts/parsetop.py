#!/usr/bin/python
################################################################################################
# Python script for parsing top.log files.
#
# Usage:  parsetop.py [filename]
#
#         file-name is the top input file to parse.
#         output is written to top.csv file in local directory.
#
# Note:  if no file name is specified, it is assumed to be top.log 
#        in the current directory.
#
################################################################################################


# Included packages.
import sys;          # System.
import re;           # Regular expressions.
from collections import defaultdict;  # Dictionary.


# Top class.
class CpuLoad:
   timestamp = "";
   load = 0.0;


# Setup some general variables.
topCount = 0; 
topFileName = "top.log";
outputFileName = "top.csv";
timestamp = "";
timestampIndex = 2;
timestampList = list ();
loadIndex = 8;
processIdIndex = 0;
processLoadResults = defaultdict (list); 


# Setup the regular expression patterns to match.
topPattern = re.compile('top -');
callgrindPattern = re.compile('callgrind-+');


# Get the top input file to parse.
args = len (sys.argv);
if (args > 1):
   topFileName = sys.argv[1];


#######################################
# Parse the file contents.
#######################################
# Open the top log file.
topFile = open (topFileName);

# Walk the file contents.
for currentLine in topFile:
   # Split the string into tokens.
   tokenList = currentLine.split ();
   # Check if we at a new top instance.
   if (topPattern.search (currentLine) is not None):
      # Set a new column. 
      topCount += 1;
      # Parse the time stamp.
      timestamp = tokenList[timestampIndex];
      # Save the timestamp.
      timestampList.append (timestamp);
   else:
      # Check for callgrind line.
      if (callgrindPattern.search (currentLine) is not None):
         # Parse the process ID.
         processId = tokenList[processIdIndex];
         # Parse the CPU load
         temp = CpuLoad ();
         temp.timestamp = timestamp;
         temp.load = tokenList[loadIndex];
         # Save the CPU load.
         processLoadResults[processId].append (temp);
      
#Close the file.
topFile.close ();


#######################################
# Write the results to a CVS file.
#######################################
# Open the output file for writing.
outputFile = open (outputFileName, 'w');

# Write the timestamps.
outputFile.write ("  " + '\t');
for timestamp in timestampList:
   outputFile.write (timestamp + '\t');
outputFile.write ('\n');

# Write the process ids and loads.
for pid in processLoadResults:
   # Writ the process id.
   outputFile.write (pid + '\t');
   pidList = processLoadResults[pid];
   for load in pidList:
      # Write the load.
      outputFile.write (load.load + '\t');
   outputFile.write ('\n');

# Close the output file.
outputFile.close ();


###########
# Done.
###########
print ("Top count = %d" % topCount);
print ("Completed.");

