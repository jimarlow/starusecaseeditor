<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:template match="*">
        <html>
            <head></head>
            <xsl:apply-templates></xsl:apply-templates>
        </html>
    </xsl:template>
    
 <xsl:template match="usecase/schema">
     <h2>Schema</h2>
     <p><xsl:value-of select="line"/></p>
</xsl:template>
    
 <xsl:template match="usecase/name">
     <h2>Name</h2>
     <p><xsl:value-of select="line"/></p>  
</xsl:template>
  
    <xsl:template match="usecase/parents">
    </xsl:template>
    
    <xsl:template match="usecase/actors">
    </xsl:template>
 
    <xsl:template match="usecase/brief_description">
    </xsl:template>
    
    <xsl:template match="usecase/preconditions">
    </xsl:template>
    
    <xsl:template match="usecase/flow_of_events">
        <xsl:for-each select="line"><p><xsl:value-of select="."/></p></xsl:for-each>  
    </xsl:template>
    
    <xsl:template match="usecase/postconditions">
    </xsl:template>
    
    <xsl:template match="usecase/alternative_flows">
    </xsl:template>
    
</xsl:stylesheet>
