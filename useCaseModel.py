from structuredDocumentSet import *
import string

INCLUDE_USE_CASE_REGEX = re.compile( r"([iI]nclude\(\s*)([a-zA-Z0-9_]*)(\s*\))" )

# The schema names
ACTOR_SCHEMA = "Actor.sss"
USE_CASE_SCHEMA = "UseCase.sss"
ALTERNATIVE_FLOW_SCHEMA = "AlternativeFlow.sss"
EXTENSION_USE_CASE_SCHEMA = "ExtensionUseCase.sss"
# The schema extensions
SCHEMA_EXTENSION = ".sss"
ACTOR_EXTENSION = ".act"
USE_CASE_EXTENSION = ".uc"
ALTERNATIVE_FLOW_EXTENSION = ".alt"
EXTENSION_USE_CASE_EXTENSION = ".ext"

def parseAlternativeFlowName( name ):
    """Alternative flows are named as follows: UseCaseName_AlternativeFlowName"""
    return name.rsplit( "_", 1 )   

class ModelElement( StructuredDocument ):
    
    def __init__( self, path, model ):
        StructuredDocument.__init__( self, path )
        self.model = model
        self.treeItem = None
        self.report = ""
        
    # Create a new ModelElement from a schema            
    @classmethod
    def new( cls, schemaPath, name, extension, model ):
        if not os.path.exists( schemaPath ):
            raise Exception( "StructuredDocument schema path " + schemaPath + " does not exist" )
        obj = cls( schemaPath, model )
        obj.changeTitle( name )
        obj.path = obj.getDirectory() + "\\" + name + "." + extension        
        obj.save()
        return obj
                
    def changeName( self, name ):
        self.deleteFile()
        self.changeTitle( name )
        self.save()
        
    def setTreeItem( self, treeItem ):
        self.treeItem = treeItem
        
    def getTreeItem( self ):
        return self.treeItem
    
    def isTreeItem( self, treeItem ):
        return self.treeItem == treeItem
    
    def getName( self ):
        return self.getTitle()  
    
    def getParentNames( self ):
        if self.getBody( ":Parents:" ):
            parentNames = self.getBody( ":Parents:" )
            try:
                parentNames.remove( "None" )
            except:
                pass
            return parentNames
        else:
            return []
    
    def hasParent( self, parent ):
        if parent.__class__ != str:
            parent = parent.getName()
        return parent in self.getParentNames()
    
    def reportExtraSectionHeaders( self ):
        extraHeaders = self.getExtraSectionHeaders()
        if extraHeaders != []:
            self.report = self.report + "These sections are NOT in the schema " + ", ".join( extraHeaders ) + "\n"
        return self.report 
    
    def reportMissingSectionHeaders( self ):
        # Missing headers
        missingHeaders = self.getMissingSectionHeaders()
        if missingHeaders != []:
            self.report = self.report + "These sections are missing " + ", ".join( missingHeaders ) + "\n"
        return self.report
    
    def reportMissingParents( self ):
        missingParents = []
        for p in self.getParentNames():
            if p not in self.model.getUseCaseNames():
                missingParents.append( p )
        if missingParents != []:
            self.report = self.report  + "These parents are missing from the model " + ", ".join( missingParents ) + "\n"  
        return self.report              
    
    def getQualityReport( self ):
        self.report = ""
        self.reportExtraSectionHeaders()
        self.reportMissingSectionHeaders()
        self.reportMissingParents()
        return self.report
    
class UseCase( ModelElement ):
    
    def __init__( self, path, model ):
        ModelElement.__init__( self, path, model )
    
    def getActorNames( self ):
        return self.getBody( ":Actors:" )
    
    def getIncludedUseCaseNames( self ):
        includedUseCaseNames = []
        for line in self.toString().splitlines():
            match = re.search( INCLUDE_USE_CASE_REGEX, line )    
            if match:
                includedUseCaseNames.append( match.group(2) )
        return includedUseCaseNames
    
    def getIncludingUseCaseNames( self ):
        """Return the names of all of the use cases that include this one."""
        includingUseCases = []
        for i in self.model.getAllUseCases():
            if self.getName() in i.getIncludedUseCaseNames():
                includingUseCases.append( i.getName() )           
        return includingUseCases
    
    def reportIncludingUseCases( self, report ):
        includingUseCases = self.getIncludingUseCaseNames( self )
        if includingUseCases != []:
            self.report = self.report + "This use case is included by " + ", ".join( includingUseCases ) + "\n" 
        return self.report 
    
    def reportMissingActors( self ):
        misingActors = []
        for p in self.getActorNames():
            if p not in self.model.getActorNames():
                misingActors.append( p )
        if misingActors != []:
            self.report = self.report  + "These actors are missing from the model " + ", ".join( misingActors ) + "\n"                

    def reportMissingIncludedUseCases( self ):
        misingIncludedUseCases = []
        for p in self.getIncludedUseCaseNames():
            if p not in self.model.getUseCaseNames():
                misingIncludedUseCases.append( p )
        if misingIncludedUseCases != []:
            self.report = self.report  + "These included use cases are missing from the model " + ", ".join( misingIncludedUseCases ) + "\n"                

    def getQualityReport( self ):
        ModelElement.getQualityReport( self )
        self.reportMissingActors()
        self.reportMissingIncludedUseCases()
        return self.report
            
class ExtensionUseCase( UseCase ):
    
    def __init__( self, path, model ):
        UseCase.__init__( self, path, model )   
                     
class AlternativeFlow( UseCase ):
    
    def __init__( self, path, model ):
        UseCase.__init__( self, path, model )   
       
    def getBaseUseCaseName( self ):
        return parseAlternativeFlowName( self.getName() )[0]

    def getAlternativeFlowName( self ):
        return parseAlternativeFlowName( self.getName() )[1]
        
    def changeBaseUseCaseName( self, name ):
        self.changeName( name + "_" + self.getAlternativeFlowName() )        

    def changeAlternativeFlowName( self, name ):
        self.changeName( self.getBaseUseCaseName() + "_" + name )    
        
    def reportMissingBaseUseCase( self ):
        misingBaseUseCase = []
        p = self.getBaseUseCaseName()
        if p not in self.model.getUseCaseNames():
            misingBaseUseCase.append( p )
        if misingBaseUseCase != []:
            self.report = self.report  + "This base use case is missing from the model " + ", ".join( misingBaseUseCase ) + "\n"   
            
    def getQualityReport( self ):
        UseCase.getQualityReport( self )
        self.reportMissingBaseUseCase()
        return self.report
 
class Actor( ModelElement ):
    
    def __init__( self, path, model ):
        ModelElement.__init__( self, path, model )
        
class UseCaseModel( object ):
    
    def __init__( self, directory ):
        self.modelName = os.path.basename( directory )
        self.directory = directory + "\\"
        self.load()
        
    def load( self ):
        self.useCases = StructuredDocumentSet( self.directory, USE_CASE_EXTENSION ) 
        self.extensionUseCases = StructuredDocumentSet( self.directory, EXTENSION_USE_CASE_EXTENSION ) 
        self.alternativeFlows = StructuredDocumentSet( self.directory, ALTERNATIVE_FLOW_EXTENSION )        
        self.actors = StructuredDocumentSet( self.directory, ACTOR_EXTENSION )
        
    def removeItem( self, item ):
        for d in self.getActorNames():
            if d.getName() == item.getName():
                self.actors.deleteDocument( d.getName() )
                return True
        for d in self.getUseCases():
            if d.getName() == item.getName():
                 self.useCases.deleteDocument( d.getName() )
                 return True
        for d in self.getAlternativeFlows():
            if d.getName() == item.getName():
                 self.alternativeFlows.deleteDocument( d.getName() )
                 return True
        return False
                  
    def itemHasChildren( self, item ):
        for i in self.getItems():
            if i.hasParent( item ):
                return True           
        return False
    
    def itemIsIncluded( self, item ):
        for i in self.getAllUseCases():
            if item.getName() in i.getIncludedUseCaseNames():
                return True           
        return False
    
    def itemHasAlternativeFlows( self, item ):
        return self.getAlternativeFlowsForUseCase( item.getName() ) != []

    def newActor( self, name ):
        item = Actor.new( self.directory + ACTOR_SCHEMA, name, ACTOR_EXTENSION, self )
        self.actors.append( item )
        item.save()
        return item

    def newUseCase( self, name ):
        item = UseCase.new( self.directory + USE_CASE_SCHEMA, name, USE_CASE_EXTENSION, self )
        self.useCases.append( item )
        item.save()
        return item

    def newExtensionUseCase( self, name ):
        item = UseCase.new( self.directory + EXTENSION_USE_CASE_SCHEMA, name, EXTENSION_USE_CASE_EXTENSION, self )
        self.extensionUseCases.append( item )
        item.save()
        return item
    
    def newAlternativeFlow( self, name ):
        item = AlternativeFlow.new( self.directory + ALTERNATIVE_FLOW_SCHEMA, name, ALTERNATIVE_FLOW_EXTENSION, self )
        self.alternativeFlows.append( item )
        item.save()
        return item    
        
    def getModelName( self ):
        return self.modelName
        
    def getItem( self, name ):
        ret = self.getUseCase( name )
        if ret:
            return ret
        ret = self.getExtensionUseCase( name )
        if ret:
            return ret
        ret = self.getAlternativeFlow( name )
        if ret:
            return ret
        ret = self.getActor( name )
        if ret:
            return ret
        
    def getUseCase( self, name ):
        ret = self.useCases.getDocument( name )
        if ret:
            ret.__class__ = UseCase
            ret.model = self
        return ret
 
    def getExtensionUseCase( self, name ):
        ret = self.extensionUseCases.getDocument( name )
        if ret:
            ret.__class__ = ExtensionUseCase
            ret.model = self
        return ret
   
    def getAlternativeFlow( self, name ):
        ret = self.alternativeFlows.getDocument( name )
        if ret:
            ret.__class__ = AlternativeFlow
            ret.model = self
        return ret    

    def getActor( self, name ):
        ret = self.actors.getDocument( name )
        if ret:
            ret.__class__ = Actor
            ret.model = self
        return ret    

    def getUseCases( self ):
        for d in self.useCases.documents:
            d.__class__ = UseCase
            d.model = self
            yield d
    
    # See if an actor is currently being used by a use case        
    def actorIsInUse( self, actor ):
        for u in self.getAllUseCases():
            if actor.getName() in u.getActorNames():
                return True
        return False

    # Get the use cases that are using an actor        
    def getUsingUseCaseNamesForActor( self, actor ):
        usingUseCaseNames = []
        for u in self.getAllUseCases():
            if actor.getName() in u.getActorNames():
                usingUseCaseNames.append( u.getName() )
        for u in self.getAlternativeFlows():
            if actor.getName() in u.getActorNames():
                usingUseCaseNames.append( u.getName() )
        return usingUseCaseNames


    def getExtensionUseCases( self ):
        for d in self.extensionUseCases.documents:
            d.__class__ = ExtensionUseCase
            d.model = self
            yield d
            
    def getAllUseCases( self ):
        for d in self.useCases.documents:
            d.__class__ = UseCase
            d.model = self
            yield d
        for d in self.extensionUseCases.documents:
            d.__class__ = ExtensionUseCase
            d.model = self
            yield d

    def getAlternativeFlows( self ):
        for d in self.alternativeFlows.documents:
            d.__class__ = AlternativeFlow
            d.model = self
            yield d      
            
    def getActors( self ):
        for d in self.actors.documents:
            d.__class__ = Actor
            d.model = self
            yield d  

    # Returns everything in the model
    def getItems( self ):
        for d in self.actors.documents:
            d.__class__ = Actor
            d.model = self
            yield d
        for d in self.useCases.documents:
            d.__class__ = UseCase
            d.model = self
            yield d
        for d in self.alternativeFlows.documents:
            d.__class__ = UseCase
            d.model = self
            yield d                    

    def getUseCaseNames( self ):
        return self.useCases.getDocumentTitles()

    def getExtensionUseCaseNames( self ):
        return self.extensionUseCases.getDocumentTitles()

    def getAllUseCaseNames( self ):
        return self.getUseCaseNames() + self.getExtensionUseCaseNames()
    
    def getAlternativeFlowNames( self ):
        return self.alternativeFlows.getDocumentTitles()    
    
    def getActorNames( self ):
        return self.actors.getDocumentTitles() 

    def getAlternativeFlowsForUseCase( self, name ):
        alternativeFlows = []
        for af in self.getAlternativeFlows():
            if af.getBaseUseCaseName() == name:
                alternativeFlows.append( af )
        return alternativeFlows

    def getOrphanAlternativeFlows( self, name ):
        orphans = []
        for af in self.getAlternativeFlows():
            if af.getBaseUseCaseName() not in self.getUseCaseNames():
                orphans.append( af )
        return orphans    
    
    def replaceTerm( self, old, new ):
        [ u.replaceTerm( old, new ) for u in self.getUseCases() ] 
        [ u.replaceTerm( old, new ) for u in self.getActors() ]
        [ u.replaceTerm( old, new ) for u in self.getExtensionUseCases() ]
        [ u.replaceTerm( old, new ) for u in self.getAlternativeFlows() ]
            
    def containsName( self, name ):
        return ( name in self.getUseCaseNames() ) or ( name in self.getExtensionUseCaseNames() ) or ( name in self.getAlternativeFlowNames() ) or ( name in self.getActorNames() )
    
if __name__ == "__main__":  

    print "UseCaseModel tests\n"
    
    sd = UseCaseModel( "C:\\Code\\Python\\STAR\\TestUseCaseModel\\" )
    print sd.getAlternativeFlowNames()
    print sd.getUseCaseNames()
    print "Alternative flows ", sd.getAlternativeFlowNames()
    print sd.getActorNames()
    temp = sd.getUseCase( "AddBookToCatalog" )
    print temp.getActorNames()
    print temp.getIncludedUseCaseNames()
    
