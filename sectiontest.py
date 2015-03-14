from section import *
import unittest

HEADER = ":test:"
LINE1 = "Hello."
LINE2 = "Jim"
BODYASSTRING = LINE1 + "\n" + LINE2
TOSTRING = HEADER + "\n" + LINE1 + "\n" + LINE2

class SectionTest( unittest.TestCase ):
    
    def setUp( self ):
        self.s = Section( HEADER )
        self.s.append( LINE1 )
        self.s.append( LINE2 )

    def testCreate( self ):
        """Check that Section creation works"""
        assert self.s.getHeader() == HEADER
        assert self.s.body[0] == LINE1
        assert self.s.body[1] == LINE2
        
    def testIncludesTerm( self ):
        assert self.s.includesTerm( "ello" ) is False
        assert self.s.includesTerm( "Hello" )
        
    def testReplaceTerm( self ):
        self.s.replaceTerm( "Hello", "Hi" )
        assert self.s.includesTerm( "Hi" )
        self.s.replaceTerm( "Hi", "Hello" )
        assert self.s.includesTerm( "Hello" )
        
    def testSub( self ):
        self.s.sub( r"H[a-z]*", "Hi" )
        assert self.s.includesTerm( "Hi" )
        
    def testGetBodyAsString( self ):
        assert self.s.getBodyAsString() == BODYASSTRING
        
    def testToString( self ):
        assert self.s.toString() == TOSTRING
        
    def testIsHeader( self ):
        assert isHeader( ":Test:\n" )
        assert isHeader( ":Test: \n" )
        
        assert isHeader( " :Test:\n" ) is False     
        assert isHeader( " :Test: " ) is False
        assert isHeader( ": Test: " ) 
        assert isHeader( ":Test : " )
        
if __name__ == "__main__":
    unittest.main()
    