#!/usr/bin/env python

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


import argparse
import os, os.path
import json
import csv
from contextlib import redirect_stdout


commentSymbol = ["//", "#", "--", "%", "'"]
openCommentSymbol = [ "'''", "/*", "=begin","{-", "<!--"]
closingCommentSymbol = ["'''", "*/", "=end", "-}","-->" ]
headers =  ['Filename', 'Language' ,'lines','blank','comment','code']
row_format ="|  {:<106} |" + "  {:<23} |" + "{:>8} |" * ((len(headers)) - 2)
borderLenght = 178
data = []
language_results = {}

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", help="Folder path to conduct line of code count.", required=True)
    parser.add_argument("-x", "--exclude", help="File extentions to exclude.", nargs="+", required=False)
    return parser.parse_args()

args = get_arguments()
folder = args.folder
exclude = set(args.exclude or [])

print("Scanning files...")

def get_files_to_check(dir, excluded):
    filesToCheck = [os.path.join(root, f) for root, _, files in os.walk(dir)
                    for f in files if os.path.isfile(os.path.join(root, f)) and not any(ext in f for ext in excluded)]
    # filesToCheck = []
    # for root, _, files in os.walk(dir):
    #     for f in files:
    #         fullpath = os.path.join(root, f)
    #         if os.path.isfile(fullpath) and not any(ext in f for ext in excluded):
    #                 filesToCheck.append(fullpath)
    if not filesToCheck:
        print ('No files found.')
        quit()
    return filesToCheck

filesToScan = get_files_to_check(folder, exclude)
totalFiles = len(filesToScan)
lineCount = 0
totalBlankLineCount = 0
totalCommentLineCount = 0

with open('./lib.json') as json_data:
    jData = json.load(json_data)

def get_language_results(file_extension):
    extensions = set(ext for meta in jData.values() for ext in meta.get("extensions", []))
    return  [file_name for file_name, meta in jData.items() if file_extension in extensions and file_extension in meta.get("extensions", [])]

print("Loading...")

with open('result.txt', 'w') as res, \
    open('result.csv', 'w', newline='\n') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(headers)
    with redirect_stdout(res):
        print("-" * borderLenght)
        print(row_format.format(*headers))
        print("-" * borderLenght)

        for fileToCheck in filesToScan:
            try:
                with  open(fileToCheck, 'r', encoding='ISO-8859-1') as f:
                    
                    
                    fileLineCount = 0
                    fileBlankLineCount = 0
                    fileCommentLineCount = 0
                    lineIsAnOpenCommentBlock = False

                    for line in f:
                        lineCount += 1
                        fileLineCount += 1
                        
                        lineWithoutWhitespace = line.strip()
                        if not lineWithoutWhitespace:
                            totalBlankLineCount += 1
                            fileBlankLineCount += 1
                        if lineWithoutWhitespace.startswith(tuple(commentSymbol)): # For single line comments
                            totalCommentLineCount += 1
                            fileCommentLineCount += 1
                        elif lineWithoutWhitespace.startswith(tuple(openCommentSymbol)): # For comment blocks
                            totalCommentLineCount += 1
                            fileCommentLineCount += 1
                            if not lineWithoutWhitespace.endswith(tuple(closingCommentSymbol)): # If comment block is open or closed
                                lineIsAnOpenCommentBlock = True
                        elif lineIsAnOpenCommentBlock:
                            totalCommentLineCount += 1
                            fileCommentLineCount += 1
                            if lineWithoutWhitespace.endswith(tuple(closingCommentSymbol)):
                                lineIsAnOpenCommentBlock = False

                    _, fileExt = os.path.splitext(fileToCheck)
                    if fileExt not in language_results:
                        language_results[fileExt] = get_language_results(fileExt)
                    lang = language_results[fileExt]

                    row = [fileToCheck, lang[0] if len(lang) > 0 else "Unsupported File", str(fileLineCount),str(fileBlankLineCount) ,  str(fileCommentLineCount), str(fileLineCount - fileBlankLineCount - fileCommentLineCount) ]
                    
                    writer.writerow(row)
                    
                    print(f"{row_format.format(os.path.basename(row[0]), *row[1:])}")

            except OSError:
                    row =[fileToCheck, "Unsupported File", "","" ,  "", "" ]
                    writer.writerow(row)
                    print(f"{row_format.format(os.path.basename(row[0]), *row[1:])}")
        
        print("-" * borderLenght)
        print ('')
        print ('Totals')
        print ('--------------------')
        print (f'Files:         {totalFiles}')
        print (f'Lines:         {lineCount}')
        print (f'Blank lines:   {totalBlankLineCount}')
        print (f'Comment lines: {totalCommentLineCount}')
        print (f'Code lines:    {lineCount - totalBlankLineCount - totalCommentLineCount}')
    
#Console output Summary
print("Success!")
print ('')
print ('Summary')
print ('--------------------')
print ('Files:         ' + str(totalFiles))
print ('Lines:         ' + str(lineCount))
print ('Blank lines:   ' + str(totalBlankLineCount))
print ('Comment lines: ' + str(totalCommentLineCount))
print ('Code lines:    ' + str(lineCount - totalBlankLineCount - totalCommentLineCount))
