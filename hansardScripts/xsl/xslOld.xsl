<?xml version="1.0"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
<xsl:template match="/">

	<xsl:for-each select="//debate[debateinfo/title='QUESTIONS WITHOUT NOTICE']/subdebate.1[question and answer]">
		<xsl:for-each select="question">
			<xsl:if test="count(preceding-sibling::question) = 0">
				<xsl:for-each select=".//para">
					<xsl:if test="not(./ancestor::interjection)">
						<xsl:value-of select="."/>
					</xsl:if>
				</xsl:for-each>
			</xsl:if>
		</xsl:for-each>
	</xsl:for-each>



</xsl:template>
</xsl:stylesheet>