package function;

import org.terrier.indexing.Collection;
import org.terrier.indexing.TRECCollection;
import org.terrier.querying.Manager;
import org.terrier.querying.QueryExpansion;
import org.terrier.querying.SearchRequest;
import org.terrier.structures.Index;
import org.terrier.structures.IndexOnDisk;
import org.terrier.structures.indexing.Indexer;
import org.terrier.structures.indexing.classical.BasicIndexer;

import java.util.HashMap;
import java.util.Map;

public class query {

    public static void main(String[] args) {

        System.setProperty("terrier.home", "/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/");

        //Collection coll = new TRECCollection("C:\\Users\\Jeremy\\Documents\\ResearchProjectData\\house_hansard\\2014");
        // NOte note entirely sure about above, i dont think we're really using it properly
        Indexer indexer = new BasicIndexer("/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/var/index", "data");
        //indexer.index(new Collection[]{ coll });
        Index index = IndexOnDisk.createIndex("/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/var/index", "data");
        System.out.println("We have indexed " + index.getCollectionStatistics().getNumberOfDocuments() + " documents");
        Manager queryingManager = new Manager(index);
        SearchRequest srq = queryingManager.newSearchRequestFromQuery("austerity");
        srq.addMatchingModel("Matching", "BM25");

        //srq.setControl("start", sStart)
        srq.setControl("qe", "on");
        queryingManager.runPreProcessing(srq);
        queryingManager.runMatching(srq);
        queryingManager.runPostProcessing(srq);
        queryingManager.runPostFilters(srq);

        QueryExpansion qexpan = new QueryExpansion();
        qexpan.process(queryingManager, srq);
        printQueryExpansion(qexpan);



//		queryingManager.runSearchRequest(srq);
//		ResultSet results = srq.getResultSet();
//		String[] displayKeys = results.getMetaKeys();

        //System.out.print(qexpan.lastExpandedQuery);


    }


    public static void printQueryExpansion(QueryExpansion qexpan) {
        System.out.println("Now split stuff\n");
        String expansion = qexpan.lastExpandedQuery;
        String[] withScores = expansion.split("[\\s]");
        Map<String, Float> exp_words = new HashMap<String, Float>();

        System.out.println(withScores.length);
        for (String temp : withScores) {
            String[] parts = temp.split("\\^");
            Float value = Float.parseFloat(parts[1]);
            System.out.println(temp);
            exp_words.put(parts[0], value);

        }

        for (String key : exp_words.keySet()) {
            System.out.println(key);
        }
    }
}

