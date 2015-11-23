import subprocess
import os
import sys
import re
import getopt

def main(argv):
    Setup global variables
    repoFileLocation = ''

    argumentString = "svnautoupgrade.py -f fromLocation"
    try:
        opts, args = getopt.getopt(argv,"hf:",["flocation="])
    except getopt.GetoptError:
        print(argumentString)
        sys.exit(2)

    if(len(opts) == 0):
        print(argumentString)
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print(argumentString)
            sys.exit()
        elif opt in ("-f","--flocation"):
            repoFileLocation = arg

    if not os.path.isfile(repoFileLocation):
        print("The repository location is not found.")
        sys.exit()

    with open(repoFileLocation, 'r+') as f:
        fileNames = [line.strip() for line in f ]
        for fileName in fileNames:
            if fileName and fileName != '':
                print("Processing: {}".format(fileName))
                if not os.path.exists(fileName):
                    print("The location {} is not found".format(fileName))
                else:
                    svnType = ''
                    for subdir2, dirs, files in os.walk(fileName):
                        for f in files:
                            if f == "fs-type":
                                fsFile = open(os.path.join(subdir2, f), 'r+')
                                svnType = fsFile.readline()

                    if svnType:
                        print("This is a repo! {}".format(svnType)
                        print("Upgrading")
                        proc = subprocess.call(['svnadmin', 'upgrade', fileName], stdout=subprocess.PIPE)
                    else:
                        print("This is not a svn directory {}".format(fileName))

if __name__ == '__main__':
    main(sys.argv[1:])
