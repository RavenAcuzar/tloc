# tloc
This Python script counts the lines of code in the for a specified directory. It looks for all the files in the specified directory. It outputs counts for total lines, blank lines, comment lines and code lines
(total lines minus blank lines and comment lines).
##### Optional: You have the option to exclude files by specifying its file extention

## Usage
```
> python tloc.py -h

 usage: tloc.py [-h] -f FOLDER [-x EXCLUDE [EXCLUDE ...]]

 options:
   -h, --help            show this help message and exit
   -f FOLDER, --folder FOLDER
                         Folder path to conduct line of code count.
   -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                         File extentions to exclude.
```
#### Start counting line of code for a project directory (use -f or --folder)
```
> python tloc.py -f \path\to\project\directory
 Scanning...
 Loading...
 Success!
 Summary
 --------------------
 Files:         3653
 Lines:         644554
 Blank lines:   42261
 Comment lines: 9244
 Code lines:    593049
```
#### (Optional) Exclude specific files based on extension (use -x or --exclude)
```
> python tloc.py -f \path\to\project\directory -x .git .test .pdf .csv
```
## Result Generation
Results are automatically generated in separate CSV and TXT files.

## Credits
Language Map - https://github.com/blakeembrey/language-map/blob/main/languages.json



