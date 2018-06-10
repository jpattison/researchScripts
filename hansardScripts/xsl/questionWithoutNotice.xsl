<!-- <?xml version="1.0"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
	<xsl:output method="text"/>
	<xsl:template match="/">

		<xsl:for-each select="hansard/session.header">
			<xsl:copy-of select="."/>

		</xsl:for-each>



	</xsl:template>
</xsl:stylesheet><?xml version="1.0"?> -->


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
<xsl:template match="/">
	<xsl:for-each select="//debate[debateinfo/title='QUESTIONS WITHOUT NOTICE']/subdebate.1[question and answer]">
		<xsl:for-each select="question">
			<xsl:if test="count(preceding-sibling::question) = 0">
				<xsl:for-each select="node()//span[@class='HPS-MemberQuestion']">
					<xsl:for-each select="ancestor::body/p">
						<xsl:if test="not(.//span[contains(@class, 'Interjecting') or contains(@class, 'Office')])">
							<xsl:copy-of select="."/>
						</xsl:if>
					</xsl:for-each>
				</xsl:for-each>
			</xsl:if>
		</xsl:for-each>
	</xsl:for-each>
</xsl:template>
</xsl:stylesheet>