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


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", help="Folder path to conduct line of code count.", required=True)
    parser.add_argument("-x", "--exclude", help="File extentions to exclude.", nargs="+", required=False)
    return parser.parse_args()

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

def get_language_results(fileToCheck, language_results):
    
    with open('./lib.json') as json_data:
        jData = json.load(json_data)

    _, fileExt = os.path.splitext(fileToCheck)
    if fileExt not in language_results:
        extensions = set(ext for meta in jData.values() for ext in meta.get("extensions", [])) 
        language_results[fileExt] = [file_name for file_name, meta in jData.items() if fileExt in extensions and fileExt in meta.get("extensions", [])]
    
    return language_results[fileExt], language_results 
    # # create an empty set to hold the file extensions
    # extensions = set()

    # # iterate over each nested dictionary in jData.values()
    # for meta in jData.values():
    #     # retrieve the extensions list from the current nested dictionary
    #     ext_list = meta.get("extensions", [])
    #     # iterate over each file extension in the extensions list
    #     for ext in ext_list:
    #         # add the extension to the set of unique extensions
    #         extensions.add(ext)

    # file_names = []
    # for file_name, meta in jData.items():
    #     if fileExt in extensions and fileExt in meta.get("extensions", []):
    #         file_names.append(file_name)


def file_loc_counter(fileToCheck, commentSymbols):
    with  open(fileToCheck, 'r', encoding='ISO-8859-1') as f:
        fileLineCount = 0
        fileBlankLineCount = 0
        fileCommentLineCount = 0
        lineIsAnOpenCommentBlock = False

        for line in f:
            fileLineCount += 1
            
            lineWithoutWhitespace = line.strip()
            if not lineWithoutWhitespace:
                fileBlankLineCount += 1
            # For single line comments
            if lineWithoutWhitespace.startswith(tuple(commentSymbols.get("commentSymbol"))):
                fileCommentLineCount += 1
            # For comment blocks
            elif lineWithoutWhitespace.startswith(tuple(commentSymbols.get("openCommentSymbol"))): 
                fileCommentLineCount += 1
                # If comment block is open set lineIsAnOpenCommentBlock=True
                if not lineWithoutWhitespace.endswith(tuple(commentSymbols.get("closingCommentSymbol"))): 
                    lineIsAnOpenCommentBlock = True
            # For open comment blocks
            elif lineIsAnOpenCommentBlock:
                fileCommentLineCount += 1
                # If line includes a closing comment tag set lineIsAnOpenCommentBlock=False
                if lineWithoutWhitespace.endswith(tuple(commentSymbols.get("closingCommentSymbol"))):
                    lineIsAnOpenCommentBlock = False
    return fileLineCount, fileBlankLineCount, fileCommentLineCount

def output_summary(totalFiles, lineCount, totalBlankLineCount, totalCommentLineCount):
    #Console output Summary
    print ('Totals')
    print ('--------------------')
    print ('Files:         ' + str(totalFiles))
    print ('Lines:         ' + str(lineCount))
    print ('Blank lines:   ' + str(totalBlankLineCount))
    print ('Comment lines: ' + str(totalCommentLineCount))
    print ('Code lines:    ' + str(lineCount - totalBlankLineCount - totalCommentLineCount))

def main():
    lineCount = 0
    totalBlankLineCount = 0
    totalCommentLineCount = 0
    language_results = {}
    
    #code comment tags
    commentSymbols = {
    'commentSymbol' : ["//", "#", "--", "%", "'"],
    'openCommentSymbol' : [ "'''", "/*", "=begin","{-", "<!--"],
    'closingCommentSymbol' : ["'''", "*/", "=end", "-}","-->" ],
    }

    #table styling
    headers =  ['Filename', 'Language' ,'lines','blank','comment','code']
    row_format ="|  {:<106} |" + "  {:<23} |" + "{:>8} |" * ((len(headers)) - 2)
    borderLenght = 178

    
    # basic input example 
    # print("Total Line of Code counter Script!")
    # folder = input("Please Input Folder Directory: ")
    # excluded = input("Inpute Excluded file extentions (comma ',' separated): ")
    # exclude = set(excluded.split(',') or [])

    args = get_arguments()
    folder = args.folder
    exclude = set(args.exclude or [])
    
    print("Scanning files...")

    filesToScan = get_files_to_check(folder, exclude)
    totalFiles = len(filesToScan)
    
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
                        fileLineCount, fileBlankLineCount, fileCommentLineCount = file_loc_counter(fileToCheck, commentSymbols)
                        lineCount += fileLineCount
                        totalBlankLineCount += fileBlankLineCount
                        totalCommentLineCount += fileCommentLineCount

                       
                        lang, language_results = get_language_results(fileToCheck, language_results)

                        row = [fileToCheck, lang[0] if len(lang) > 0 else "Unsupported File", str(fileLineCount),str(fileBlankLineCount) ,  str(fileCommentLineCount), str(fileLineCount - fileBlankLineCount - fileCommentLineCount) ]
                        
                        writer.writerow(row)
                        
                        print(f"{row_format.format(os.path.basename(row[0]), *row[1:])}")

                except OSError:
                        row =[fileToCheck, "Unsupported File", "","" ,  "", "" ]
                        writer.writerow(row)
                        print(f"{row_format.format(os.path.basename(row[0]), *row[1:])}")
            
            print("-" * borderLenght)
            print ('')
            output_summary(totalFiles, lineCount, totalBlankLineCount, totalCommentLineCount)
    
    print("Success...")
    output_summary(totalFiles, lineCount, totalBlankLineCount, totalCommentLineCount)

main()