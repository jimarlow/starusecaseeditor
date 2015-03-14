import re

SECTIONREGEXP = "^:[a-zA-Z0-9_ ]*: *$"  
    
class Section( object ):
    """
    This is a simple section class that comprises a header and a body.
    The header is of form :Header: and the body is a list of strings.
    """
    
    def __init__( self, header ):
        """Create a new Section with the given header and an empty body."""
        self.header = header.strip()
        self.body = []
        
    def append( self, line ):
        """Append the line to the body of this Section."""
        self.body.append( line.rstrip() )
        
    def getHeader( self ):
        """Return the header of this Section."""
        return self.header
        
    def getBody( self ):
        """Return the body of this Section as a list of strings."""
        return self.body
    
    def getBodyAsString( self ):
        """Return the body of this Section as a single string."""
        return "\n".join( self.body )
    
    def toString( self ):
        """Return this Section as a single string."""
        return "\n".join( [ self.header, self.getBodyAsString() ] )
    
    # Need to use re to find whole words
    def includesTerm( self, term ):
        """Return true if the body of this Section includes term."""
        wholeWordPattern = r"(\b|_)(" + term + r")(\b|_)"
        return ( re.search( wholeWordPattern, self.getBodyAsString() ) != None )
    
    def replaceTerm( self, oldTerm, newTerm ):
        """Substitute newTerm for oldTerm in the body of this Section."""
        wholeWordPattern = r"\b(" + oldTerm + r")\b"
        self.sub( wholeWordPattern, newTerm )
    
    def sub( self, regex, replacement ):
        """Substitute replacement for regex in the body of this Section."""
        for i in range( len( self.body ) ):
            self.body[ i ] = re.sub( regex, replacement, self.body[ i ] )
     
def isHeader( header ):
    """Return true if the string is a header according to SECTIONREGEXP "^:[a-zA-Z0-9_ ]*: *$"."""
    return re.match( SECTIONREGEXP, header ) != None
      
