import os
from section import *

class SimpleDocument( object ):
    """
    Rules that define SimpleDocuments:
    1. A SimpleDocument comprises one or more Sections.
    2. Each Section has a header of the form :Header: and a body that is a list of strings.
    """
    
    def __init__( self, path ):
        """Create a new SimpleDocument at the given path. """
        self.path = path
        self.sections = []
        self.load( self.path )
        
    def load( self, path = None ):
        """Load a new SimpleDocument from the given path. """
        if path == None:
            path = self.path
        if os.path.exists( path ):
            f = open( path, "r" )
            lines = f.readlines()
            f.close()
            self.__createSections( lines )
                       
    def save( self ):
        """Save the SimpleDocument to its current path. """
        self.saveAs( self.path )
            
    def saveAs( self, path ):
        """Save the SimpleDocument to a new path. """
        self.path = path
        f = open( path, "w" )
        f.write( self.toString() )
        f.close()
        
    def __createSections( self, lines ):
        """Parse the SimpleDocument file to create the Sections in memory. """
        self.sections = []
        s = None
        for line in lines:
            l = line.strip()
            if l != "":
                if isHeader( l ):
                    s = Section( l )
                    self.sections.append( s )
                elif s:
                    s.append( l )
                    
    def getSection( self, header ):
        """Return the Section with the given header. """
        ret = [ s for s in self.sections if s.getHeader() == header ]
        if len( ret ) > 0:
            return ret[0]
        else:
            return None
        
    def getBody( self, header ):
        """Return the body of the Section with the given header. """
        if self.getSection( header ):
            return self.getSection( header ).getBody()
        else:
            return []
        
    def getSectionHeaders( self ):
        """Return a list of all Section headers as strings. """
        return [ s.getHeader() for s in self.sections ]
                    
    def includesTerm( self, term ):
        """Returns true of this SimpleDocument includes the term in any of it's Section bodies. """
        for s in self.sections:
            if s.includesTerm( term ): return True
        return False
    
    def replaceTerm( self, oldTerm, newTerm ):
        """Replaces the term throughout the SimpleDocument Section bodies. """
        [ s.replaceTerm( oldTerm, newTerm ) for s in self.sections ]
        self.save()
        
    def sub( self, regEx, replacement ):
        """Substitutes the replacement for the regEx throughout the SimpleDocument Section bodies. """
        [ s.sub( regEx, replacement ) for s in self.sections ]
        self.save()
            
    def toString( self ):
        """Returns the SimpleDocument as a single string. """
        return "\n\n".join( [ s.toString() for s in self.sections ] )   
    
    def fromString( self, string ):
        """Creates a new set of Sections from a string."""
        # May need keepends = True
        self.__createSections( string.splitlines() )  
                
    # Also updates the file       
    def updateFromString( self, string ):
        """Creates a new set of Sections from a string and saves the file."""
        self.deleteFile()
        self.fromString( string )
        self.save()
        
    def getPath( self ):
        """Returns the path where this SimpleDocument is saved/loaded. """
        return self.path
            
    def getDirectory( self ):
        """Returns the directory where this SimpleDocument is saved/loaded. """
        return os.path.dirname( self.path )
    
    def getExtension( self ):
        """Returns the extension for this SimpleDocument. """
        return os.path.split( self.path )[1].split( "." )[1]

