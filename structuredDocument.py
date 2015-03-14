import os
from section import *
from simpleDocument import *
import xml.dom.minidom

SCHEMA_HEADER = ":Schema:"
SCHEMA_EXTENSION = ".sss"

class StructuredDocument( SimpleDocument ):
    """
    Rules that define StructuredDocuments:
    1. A StructuredDocument is a kind of SimpleDocument that has a schema that defines its structure.
    2. The first Section in a StructuredDocument is ALWAYS the schema Section for that document.
    3. The schema Section header is ALWAYS ":Schema:".
    4. The second Section is ALWAYS the title Section.
    5. The title of a StructuredDocument is ALWAYS the first line of the body of the
    title section.
    """
    
    def __init__( self, path ):
        """
        Create a new StructuredDocument. 
        """
        SimpleDocument.__init__( self, path )
        self.schema = None
        if self.schemaPathExists():
            self.schema = SimpleDocument( self.getSchemaPath() )
        else:
            raise Exception( "StructuredDocument schema path " + self.getSchemaPath() + " does not exist" )
        
    @classmethod
    def newFromSchema( cls, schemaPath, name, extension ):
        """
        Create a new StructuredDocument with the given name and extension from the specified schemaPath. 
        """
        if not os.path.exists( schemaPath ):
            raise Exception( "StructuredDocument schema path " + schemaPath + " does not exist" )
        obj = cls( schemaPath )
        obj.changeTitle( name )
        obj.path = obj.getDirectory() + "\\" + name + "." + extension        
        obj.save()
        return obj
        
    def exportToXMLFile( self, directory, styleSheetName = None ):
        """
        Export the StructuredDocument to an XML file. 
        """
        f = open( directory + "\\" + self.getTitle() + ".xml", "w" )
        f.write( self.toXMLString( styleSheetName ) )
        f.close()
        
    def toXMLString( self, styleSheetName = None ):
        """
        Get an XML string from the StructuredDocument. 
        """
        doc = xml.dom.minidom.Document()
        root = doc.createElement( self.getSchemaName().strip( ":" ).lower().split( "." )[0] )
        doc.appendChild( root )
        if styleSheetName:
            styleSheet = doc.createProcessingInstruction( "xml-stylesheet", "type=\"text/xsl\" href=\"" + styleSheetName + "\"" )
            doc.insertBefore( styleSheet, doc.documentElement )
        for s in self.sections:
            element = doc.createElement( s.getHeader().strip( ":" ).lower().replace( " ", "_" ) )
            root.appendChild( element )
            for l in s.getBody():
                lineNode = doc.createElement( "line" )
                element.appendChild( lineNode )
                textNode = doc.createTextNode( l )
                lineNode.appendChild( textNode )
        return doc.toprettyxml()
        
    def getTitle( self ):
        """
        The title of a structured document is the first line of the body of
        the second Section in the document. 
        The first Section is always the schema.
        """
        return self.sections[1].body[0]
    
    def getTitleHeader( self ):
        """
        The title header of a structured document second Section in the document. 
        The first Section is always the schema.
        """
        return self.sections[1].getHeader()
    
    def getSchemaName( self ):
        """
        Get the name of the schema.
        """
        schemaSection = self.getSection( SCHEMA_HEADER )
        if schemaSection: 
            return schemaSection.body[0]
        
    def deleteFile( self ):
        """
        Delete the file associated with this StructuredDocument.
        """
        if os.path.exists( self.path ):
            os.remove( self.path )
            
    def changeTitle( self, newTitle ):
        """
        Change the title of the StructuredDocument.
        """
        self.sections[1].body[0] = newTitle
 
    def getSchemaPath( self ):
        """
        Return the path to the schema for this StructuredDocument.
        """
        return self.getDirectory() + "\\" + self.getSchemaName()
    
    def schemaPathExists( self ):
        """
        Return true if the path to the schema for this StructuredDocument exists.
        """
        return os.path.exists( self.getSchemaPath() )
    
    def getExtraSectionHeaders( self ):
        """
        Return a list of the Section headers not in the schema.
        """
        ret = []
        s1 = set( self.schema.getSectionHeaders() )
        s2 = set( self.getSectionHeaders() )
        for e in (s2 - s1):
            ret.append( e )
        return ret
        
    def getMissingSectionHeaders( self ):
        """
        Return a list of the Section headers in the schema but not in the StructuredDocument.
        """
        ret = []
        s1 = set( self.schema.getSectionHeaders() )
        s2 = set( self.getSectionHeaders() )
        for e in (s1 - s2):
            ret.append( e )
        return ret
       

if __name__ == "__main__":  

    print "StructuredDocument tests\n"

##    s1 = StructuredDocument( "C:\\Code\\Python\\STAR\\AddBookToCatalog.uc" )
    s2 = StructuredDocument.newFromSchema( "C:\\Code\\Python\\STAR\\TestUseCaseModel\\UseCase.sss", "TestUC", "junk" )
    print s2.getExtension()
    print s2.toString()
##    s2.exportAsXML( "test" )
    print s2.toXMLString()


##    s3 = StructuredDocument.newFromSchema( "C:\\Code\\Python\\STAR\\TestUseCaseModel\\UseCaseERROR.sss", "TestUC", "junk" )

##    print s1.schemaPathExists()
##    print s1.getSchemaName()
##    print s1.getSchemaPath()
##    print "Title = " + s1.getTitle()
##    print "Title header = " + s1.getTitleHeader()
    