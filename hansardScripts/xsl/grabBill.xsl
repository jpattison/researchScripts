

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
<xsl:template match="/">
	<xsl:for-each select="//debate[debateinfo/title='BILLS']/subdebate.1[subdebate.2]">
		<xsl:for-each select="subdebateinfo">
			<xsl:copy-of select="."/>
		</xsl:for-each>
	</xsl:for-each>
</xsl:template>
</xsl:stylesheet>