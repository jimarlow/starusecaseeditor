from simpleDocument import *
import unittest
import os

testFileContents = """:Name:
TestSimpleDocument

:Parents:
None

:Actors:
Librarian

:Brief description:
The Librarian adds a new book to the library catalog.

:Preconditions:
The Librarian is logged on to OLAS.

:Flow of events:
The Librarian selects "add book".
The system asks for the BookDetails.
include( Test)
The Librarian enters the BookDetails.
include( Test3 )
The system adds the the new Book to the catalog.

:Postconditions:
A new Book has been added to the catalog.

:Alternative flows:
1. CancelAddBook
2. BookAlreadyExists"""

header = ":Flow of events:"

body = [ 'The Librarian selects "add book".', 'The system asks for the BookDetails.', 'include( Test)', 'The Librarian enters the BookDetails.', 'include( Test3 )', 'The system adds the the new Book to the catalog.' ]

testFileName = "\\TestSimpleDocument.tmp"

testFileExtension = "tmp"

sectionHeaders = [ ":Name:", ":Parents:", ":Actors:", ":Brief description:", ":Preconditions:", ":Flow of events:", ":Postconditions:", ":Alternative flows:" ]

term1 = "Librarian"
term2 = "Libra"
term3 = "TrusedLibrarian"
regex = r"[Bb]ook"
replacement = "Kook"

class SimpleDocumentTest( unittest.TestCase ):
    
    def setUp( self ):
        self.simpleDocumentPath = os.getcwd() + testFileName
        f = open( self.simpleDocumentPath, "w" )
        f.write( testFileContents )
        f.close()
        
    def testSetUp( self ):
        print self.simpleDocumentPath
        
    def testLoad( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        assert s.toString() == testFileContents
        
    def testGetSection( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        section = s.getSection( header )
        assert section.getHeader() == header
        assert section.getBody() == body
        
    def testGetPath( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        assert self.simpleDocumentPath == s.getPath()
        
    def testGetDirectory( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        assert os.getcwd() == s.getDirectory()
        
    def testGetExtension( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        assert testFileExtension == s.getExtension()
        
    def testGetSectionHeaders( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        assert sectionHeaders == s.getSectionHeaders()

    def testIncludesTerm( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        assert s.includesTerm( term1 )
        assert s.includesTerm( term2 ) is False

    def testRepalceTerm( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        s.replaceTerm( term1, term3 )
        assert s.includesTerm( term3 )
     
    def testSub( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        s.sub( regex, replacement )
        assert s.includesTerm( "KookDetails" )
        assert s.includesTerm( "BookDetails" ) is False
        
    def testToAndFromString( self ):
        s = SimpleDocument( self.simpleDocumentPath )
        assert s.toString() == testFileContents
        s.fromString( testFileContents )
        assert s.toString() == testFileContents

if __name__ == "__main__":
    unittest.main()
