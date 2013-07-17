import sys
import re
import argparse

## entr_filter.py <entrained file name> <whitelist file name>
##
## This loads the file of entrained variables, along with the whitelist, then prints out
## any entrained variables that are not covered by the whitelist.
##


entrainedByPatt = re.compile('Script ([^ ]+) \(([^:]+):(\d+)\) has variables entrained by ([^ ]+) \(([^:]+):(\d+)\) ::([^\r\n]*)\r?$')

# 1: outer function script name
# 2: outer function file name
# 3: outer function line number
# 4: inner function name
# 5: inner function file name
# 6: inner function line number
# 7: list of symbols


# For now, there's no ability to only whitelist for certain inner functions.
whitelistPatt = re.compile('outer ([^ ]+) \(([^:]+):(\d+)\) inner \* ::([^\r\n]*)\r?$')

# 1: outer function script name
# 2: outer function file name
# 3: outer function line number
# 4: list of symbols

# You can also start a line with '#' in the white list, and it will be ignored.



def scriptToString(s):
    return '{0} ({1}:{2})'.format(s[0], s[1], s[2])

wildcardWhitelist = set(['*'])

def cancelify (entrainedVars, whitelist):
    for outer, innerMap in entrainedVars.iteritems():
        innerWhitelist = whitelist.get(outer, set([]))

        # If this outer function is wildcarded
        if innerWhitelist == wildcardWhitelist:
            print 'WILD CARD!'
            continue
        print 'OUTER', outer
        print '\t', innerMap
        print '\t', innerWhitelist


#        sys.stdout.write('outer {0}\n'.format(scriptToString(outer)))
#        sys.stdout.write('inner {0}\n'.format(scriptToString(inner)))

#        print '\tentrained: ', evars



#########

def relativizePath(path, relativeTo):
    if path.startswith(relativeTo):
        return path[len(relativeTo):]
    print 'Script path', path, 'does not have base path', relativeTo, 'as a prefix'
    exit(-1)


def parseEntrainedFile(f, basePath):
    entrainedVars = {}

    for l in f:
        em = entrainedByPatt.match(l)
        if not em:
            print 'Failed to match line:'
            print l
            continue
        outer = (em.group(1), relativizePath(em.group(2), basePath), em.group(3))
        inner = (em.group(4), relativizePath(em.group(5), basePath), em.group(6))
        evars = set(em.group(7).split())

        if not outer in entrainedVars:
            entrainedVars[outer] = {}
        innerMap = entrainedVars[outer]
        if inner in innerMap:
            print 'Should not have gotten the outer/inner pair',
            print scriptToString(outer), scriptToString(inner), 'twice'
            exit(-1)
        innerMap[inner] = evars

    return entrainedVars


def loadEntrainedFile(entrainedFileName, basePath):
    try:
        entrFile = open(entrainedFileName, 'r')
    except:
        print 'Error opening entrained variable file', fname
        exit(-1)

    results = parseEntrainedFile(entrFile, basePath)
    entrFile.close()

    return results


###############

def parseWhitelistFile(f):
    whitelist = {}
    for l in f:
        wlm = whitelistPatt.match(l)
        if not wlm:
            # Ignore comments
            if l.startswith('#'):
                continue
            # We should also ignore lines that are entirely whitespace.
            print 'Failed to match line:'
            print l
            continue
        outer = (wlm.group(1), wlm.group(2), wlm.group(3))
        evars = set(wlm.group(4).split())

        if outer in whitelist:
            print 'We only support a single white list entry for an outer function because I am lazy'
            exit(-1)
        whitelist[outer] = evars

    return whitelist


def loadWhitelist(whitelistFileName):
    try:
        whitelistFile = open(whitelistFileName, 'r')
    except:
        print 'Error opening whitelist file', fname
        exit(-1)
    return parseWhitelistFile(whitelistFile)


###########

if len(sys.argv) < 3:
    print 'Not enough arguments.'
    exit()

basePath='/Users/amccreight/mz/'

entrainedVars = loadEntrainedFile(sys.argv[1], basePath)
whitelist = loadWhitelist(sys.argv[2])

cancelify(entrainedVars, whitelist)





