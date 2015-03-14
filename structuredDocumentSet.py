import glob
from structuredDocument import *

class StructuredDocumentSet( object ):
    """
    A StructuredDocumentSet comprises all StructuredDocuments in the specified directory 
    that have the specified extension.
    """        
    
    def __init__( self, directory, extension ):
        """
        Create a new StructuredDocumentSet and load all StructuredDocuments in the specified directory 
        that have the specified extension.
        These must be StructuredDocuments.
        """        
        self.loadDocuments( directory, extension )
        
    def loadDocuments( self, directory, extension ):
        """
        Load all StructuredDocuments in the specified directory that have the specified extension.
        These must be StructuredDocuments
        """
        self.documents = []
        self.directory = directory
        self.extension = extension
        [ self.documents.append( StructuredDocument( p ) ) for p in self.getDocumentPaths() ]
            
    def getDocument( self, title ):
        """
        Return a StructuredDocument given its title.
        """
        for d in self.documents:
            if d.getTitle() == title:
                return d
        return None
       
    def deleteDocument( self, title ):
        """
        Delete a StructuredDocument given its title.
        Also deletes the disk file for the StructuredDocument.
        """
        d = self.getDocument( title )
        d.deleteFile()
        self.documents.remove( d )  
        
    def append( self, document ):
        """
        Append a new StructuredDocument.
        """
        self.documents.append( document )
                    
    def getDocumentPaths( self ):
        """
        Return a list of all of the StructuredDocuments in self.directory that have self.extension.
        """
        return glob.glob( self.directory + "*" + self.extension )

    def getSchemaPaths( self ):
        """
        Return a list of all of the schemas in self.directory.
        """
        return glob.glob( self.directory + SCHEMA_EXTENSION )
    
    def getDocumentTitles( self ):
        """
        Return a list of all of the titles of the StructuredDocuments.
        """        
        return [ d.getTitle() for d in self.documents ]
    
if __name__ == "__main__":  

    print "StructuredDocumentSet tests\n"
    
    sd = StructuredDocumentSet( "C:\\Code\\Python\\STAR\\TestUseCaseModel\\", "uc" )
    print sd.getDocumentPaths()
    print sd.getSchemaPaths()
    print sd.documents[0].getSectionHeaders()