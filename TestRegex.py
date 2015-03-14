#!/usr/bin/env python
#Boa:PyApp:main
import re

modules ={}

def main():
    subject = "Include( HelloJim )"

    includeUseCaseRegex = re.compile( r"([iI]nclude\(\s*)([a-zA-Z0-9_]*)(\s*\))" )
    match = re.search( includeUseCaseRegex, subject )    
    if match:
        print match.group(1)
        print match.group(2)
        print match.group(3)
    else:
        result = ""

if __name__ == '__main__':
    main()
