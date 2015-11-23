# svn-migration-tools
Repository for some fairly universal scripts to aid in a subversion
migration process.

## Inspiration
Simply put, I needed to migrate two separate Subversion servers in a limited
amount of time. I knew I would have to migrate them again soon due to other
changes going on in the company, and didn't want to re do a lot of manual work.

## Summary of the files

### svnautohotcopy
This script was built with the intent to facilitate migrating Subversion
repositories from one machine to another.

In Windows you wanted to copy all of a server's repositories to your D: drive
you would enter
```
::Mount the target machine's C drive
pushd \\machineName\c$
::Call C: to change back to the script's directory
C:
::Execute the script
svnautohotcopy -f Z:\path_to_repos -t D:\
```

This will go through and hotcopy all of the repositories from the target machine.

If a directory is found that is not a repository, it will be logged to
"nonSvnDirLog.txt" by default.

If a directory cannot be copied because it does not contain a "fsfs.conf" file,
it's name will be logged to "upgradeNeededLog.txt" by default.

### svnautoupgrade
This script iterates through a file that _should_ contain a set of directories.
For each directory, if it is a subversion directory, it will run the
```svnadmin upgrade``` command on it

If your files are on another disk, run
```
pushd \\machineName\c$
::Call C: to change back to the script's directory
C:
::Execute the script
svnautoupgrade -f  C:\pathToFile.txt
```
