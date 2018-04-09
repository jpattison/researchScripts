package function;

import org.terrier.indexing.Collection;
import org.terrier.indexing.SimpleFileCollection;
import org.terrier.indexing.TRECCollection;
import org.terrier.matching.ResultSet;
import org.terrier.querying.Manager;
import org.terrier.querying.QueryExpansion;
import org.terrier.querying.SearchRequest;
import org.terrier.structures.Index;
import org.terrier.structures.IndexOnDisk;
import org.terrier.structures.MetaIndex;
import org.terrier.structures.indexing.Indexer;
import org.terrier.structures.indexing.classical.BasicIndexer;
import org.terrier.utility.ApplicationSetup;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class query {

    public static void main(String[] args) throws IOException {

        System.setProperty("terrier.home", "/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/");

        //Collection coll = new TRECCollection("C:\\Users\\Jeremy\\Documents\\ResearchProjectData\\house_hansard\\2014");
        // NOte note entirely sure about above, i dont think we're really using it properly
        Indexer indexer = new BasicIndexer("/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/var/index", "data");
        Index index = IndexOnDisk.createIndex("/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/var/index", "data");
        System.out.println("We have indexed " + index.getCollectionStatistics().getNumberOfDocuments() + " documents");


//        // Directory containing files to index
//        String aDirectoryToIndex = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/output/";
//
//        // Configure Terrier
//        ApplicationSetup.setProperty("indexer.meta.forward.keys", "filename");
//        ApplicationSetup.setProperty("indexer.meta.forward.keylens", "200");
//
//        Indexer indexer = new BasicIndexer("/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/var/autoIndex", "data");
//        //Collection coll = new SimpleFileCollection(Arrays.asList(aDirectoryToIndex), true);
//
//        Collection coll = new TRECCollection(); //Arrays.asList(aDirectoryToIndex), true);
//        indexer.index(new Collection[]{coll});
//        //indexer.close();
//
//        Index index = Index.createIndex("/Users/jeremypattison/LargeDocument/ResearchProjectData/terrier-core-4.2/var/autoIndex", "data");

        MetaIndex metaIndex = index.getMetaIndex();


        System.out.println("We have indexed " + index.getCollectionStatistics().getNumberOfDocuments() + " documents");




        Manager queryingManager = new Manager(index);

        String fileLocation = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/textSnippits/2014-05-14.txt";
//
        String everything = "the austerity is killing the country";

//        try(BufferedReader br = new BufferedReader(new FileReader(fileLocation))) {
//            StringBuilder sb = new StringBuilder();
//            String line = br.readLine();
//
//            while (line != null) {
//                sb.append(line);
//                sb.append(System.lineSeparator());
//                line = br.readLine();
//            }
//            everything = sb.toString();
//        }




        SearchRequest srq = queryingManager.newSearchRequestFromQuery(everything);
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



		queryingManager.runSearchRequest(srq);
		ResultSet results = srq.getResultSet();
		int[] docIds = results.getDocids();

		System.out.println("printing stuff");

		System.out.println("We got {0} results".format(String.valueOf(results.getExactResultSize())));

//		for (int temp : docIds) {
//            System.out.println(String.valueOf(temp));
//
//
//        }


        // Print the results
        System.out.println(results.getExactResultSize()+" documents were scored");
        System.out.println("the following meta keys were identified");

        String[] displayKeys = metaIndex.getKeys();

            for (String temp : displayKeys) {
                System.out.println(temp);

        }



        System.out.println("The top "+results.getResultSize()+" of those documents were returned");
        System.out.println("Document Ranking");
        for (int i =0; i< results.getResultSize(); i++) {
            int docid = results.getDocids()[i];
            double score = results.getScores()[i];
//            System.out.println("   Rank "+i+": "+docid+" "+metaIndex.getItem("filename", docid)+" "+score);
            System.out.println("   Rank "+i+": "+docid+" "+metaIndex.getItem("docno", docid)+" "+score);

        }

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

