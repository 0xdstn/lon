#!/usr/bin/env python3

import os
import sys
from pathlib import Path

bookmarksPath = str(Path.home()) + '/.lon'

def parseLine(line):
    parsed = []

    parts = line.split(" [")
    
    parsed.append(parts[0]) # URL

    parts = parts[1].split('] ')

    parsed.append(parts[0]) # Title

    parsed.append(parts[1].split(',')) # Tags array

    parsed.append('[' + parts[1].replace(',','] [') + ']') # Tags list

    return parsed

def displayLink(line):
    parsed = parseLine(line)

    print('')
    print('TITLE: ' + parsed[1])
    print('URL:   ' + parsed[0])
    print('TAGS:  ' + parsed[3])

# CMD about
def about():
    info('Version:      1.0.1')
    info('Author:       ~dustin')
    info('Source:       https://github.com/0xdstn/lon')
    info('More info:    https://tilde.town/~dustin/projects/lon')

# CMD: help
def usage():
    print('Usage: lon [command]')
    print('')
    print('Commands:')
    print('  init                                Initialize your bookmarks')
    print('  list                                View a list of all your bookmarks')
    print('  tags                                View a list of all your tags')
    print('  search <term>                       Search for bookmarks containing the provided term')
    print('  tagged <tag>                        Search for bookmarks tagged with the provided tag')
    print('  add <url> "<title>" <tag1>,<tag2>   Add a bookmark with the provided details')

# CMD: init
def init():
    if os.path.exists(bookmarksPath) == False:
        bookmarksFile = open(bookmarksPath,'w')
        bookmarksFile.write('')
        bookmarksFile.close()
        print('')
        print('[+] Created ~/.lon')
    else:
        print('')
        print('[-] You already have a ~/.lon file')

# CMD: search <term>
def search(term):
    term = term.lower()
    for line in data:
        if term in line.lower():
            displayLink(line)

# CMD: tagged <tag>
def tagged(term):
    term = term.lower()
    for line in data:
        parts = line.split('] ')
        tags = [x.lower() for x in parts[1].split(',')]
        if term in tags:
            displayLink(line)

# CMD: list
def listLinks():
    for line in data:
        displayLink(line)

# CMD: tags
def listTags():
    counts = []
    tags = []

    for line in data:
        parsed = parseLine(line)
        for tag in parsed[2]:
            if tag in tags:
                counts[tags.index(tag)] = counts[tags.index(tag)] + 1;
            else:
                tags.append(tag)
                counts.append(1)

    print('')

    for x in sorted(range(len(counts)), reverse=True, key=lambda k: counts[k]):
        print(tags[x] + ' (' + str(counts[x]) + ')')

# CMD: add <url> <title> <tags>
def add(url, title, tags):
    line = url + ' [' + title + '] ' + tags

    bookmarksFile = open(bookmarksPath,'a')
    bookmarksFile.write(line + "\n")
    bookmarksFile.close()

    print('[+] Added')
    displayLink(line)

if len(sys.argv) > 1:
    cmd = sys.argv[1]
    
    if cmd == 'help': usage()
    elif cmd == 'init': init()
    elif cmd == 'about': about()
    else:
        if os.path.exists(bookmarksPath):
            with open(bookmarksPath) as f:
                data = [x.strip() for x in f.readlines()]
                f.close()

            if cmd == 'list': listLinks()
            elif cmd == 'tags': listTags()
            elif cmd == 'search' and len(sys.argv) == 3: search(sys.argv[2])
            elif cmd == 'tagged' and len(sys.argv) == 3: tagged(sys.argv[2])
            elif cmd == 'add' and len(sys.argv) == 5: add(sys.argv[2],sys.argv[3],sys.argv[4])
            else: 
                print('')
                print('[-] Command not found')
                print('')
                usage()
        else:
            print('')
            print('[-] You don\'t have a ~/.lon file. run "lon init" to create one.')
else:
    print('')
    print('[-] Command not provided')
    print('')
    usage()
