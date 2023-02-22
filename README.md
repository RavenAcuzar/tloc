# This Python script counts the lines of code in the for a specified directory.
# It looks for all the files in the specified directory. 
# Optional: You have the option to exclude files by specifying its file extention
# using -x | --exclude [file extentions] flag.

# It outputs counts for total lines, blank lines, comment lines and code lines
# (total lines minus blank lines and comment lines).
# Results are generated in 2 separate files: result.txt, result.csv

# Example usage and output:
# > tloc.py --folder C:\path\to\poject\directory --exclude .git .vscode
# Scanning files...
# Loading...
# Success!
#
# Summary
# --------------------
# Files:         3653
# Lines:         644554
# Blank lines:   42261
# Comment lines: 9244
# Code lines:    593049

# Credits: language map https://github.com/blakeembrey/language-map/blob/main/languages.json
