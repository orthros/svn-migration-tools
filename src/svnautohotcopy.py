import subprocess
import os
import sys
import re
import getopt

def main(argv):
    isVerbose = False
    def log( stringValue ):
        if isVerbose:
            print(stringValue)
        return;

    upgradeNeededLog = open('upgradeNeededLog.txt', 'w+')
    def logUpgrade(stringValue):
        upgradeNeededLog.write(stringValue + "\n")
        upgradeNeededLog.flush()

    nonSvnDirLog = open('nonSvnDirLog.txt', 'w+')
    def logNonSVN(stringValue):
        nonSvnDirLog.write(stringValue + "\n")
        nonSvnDirLog.flush()

    #Setup global variables
    fromLocation = ''
    toLocation = ''
    includedDirectories = set()

    #Setup a temporary variable
    includedDirectoriesFile = ''

    argumentString = "svnautohotcopy.py -f fromLocation -t toLocation -d directoriesFile -u upgradeNeededLog -n nonSvnDirLog"
    try:
        opts, args = getopt.getopt(argv,"hf:t:d:u:n:v",["flocation=","tlocation=","dFiles=","ulog=","nlog=","verbose="])
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
        elif opt in ("-f", "--flocation"):
            fromLocation = arg
        elif opt in ("-t", "--tlocation"):
            toLocation = arg
        elif opt in ("-u", "--ulog"):
            upgradeNeededLog = open(arg, "w+")
        elif opt in ("-n", "--nlog"):
            nonSvnDirLog = open(arg, "w+")
        elif opt in ('-v', '--verbose'):
            isVerbose = arg.lower() == "true"
        elif opt in ('-d', '--directoriesFile'):
            includedDirectoriesFile = arg


    if not os.path.exists(fromLocation):
        print("The repository location is not found.")
        sys.exit()

    if not os.path.exists(toLocation):
        print("The to location doesn't exist.")
        sys.exit()

    #Parse our include file
    if includedDirectoriesFile:
        if not os.path.exists(includedDirectoriesFile):
            print("The include file does not exist")
            sys.exit()
        with open(includedDirectoriesFile, "r") as ins:
            for line in ins:
                includedDirectories.add(line)
    else:
        for tempDir in os.listdir(fromLocation):
            includedDirectories.add(tempDir)
    #Now if

    #Setup the regex to determine if it is fsfs or not
    regex = re.compile('^fsfs$', re.MULTILINE)

    #Start going through the fromLocation and begin work

    for subdir in os.listdir(fromLocation):
        print("\nWorking on subdir {}".format(subdir))
        loc = os.path.join(fromLocation, subdir)
        log("Our location is {}".format(loc))

        if subdir not in includedDirectories:
            print("\nSkipping subdir {} as it is not in our included directories".format(subdir))
            continue

        svnType = ""
        fsfsExists = False

        for subdir2, dirs, files in os.walk(loc):
            for f in files:
                #log(f)
                if f == "fs-type":
                    fsFile = open(os.path.join(subdir2, f), 'r+')
                    svnType = fsFile.readline()
                elif f == 'fsfs.conf':
                    fsfsExists = True

        if (svnType) and (svnType != ""):
            log("This is a svn repository")
            if not fsfsExists:
                #update the repository
                print("Need to upgrade this repo")
                logUpgrade(loc)
                #In my perfect world we'd upgrade it here and then just
                #hotcopy, but upograde is not safe to do if there are ongoing
                #transactions.
                #proc = subprocess.call(['svnadmin', 'upgrade', loc], stdout=subprocess.PIPE)
            else:
                log("Time to hotcopy!")
                log("toLocation {}".format(toLocation))
                log("subdir {}".format(subdir))

                toLoc = os.path.join(toLocation, subdir)
                print("Hotcoping to {}".format(toLoc))

                proc = subprocess.call(['svnadmin', 'hotcopy', loc, toLoc], stdout=subprocess.PIPE)
        else:
            logNonSVN(loc)

    upgradeNeededLog.close()
    nonSvnDirLog.close()


if __name__ == '__main__':
    main(sys.argv[1:])
