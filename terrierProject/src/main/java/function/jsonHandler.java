package function;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.*;

public class jsonHandler {


    private static final String FILENAME = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/sentenceNoProperNouns/2007-08-14.json";


    public static void main(String[] args) throws IOException {

        BufferedReader br = null;
        FileReader fr = null;

        try {
            fr = new FileReader(FILENAME);
            br = new BufferedReader(fr);

            String sCurrentLine;
            while ((sCurrentLine = br.readLine()) != null) {
                System.out.println(sCurrentLine);
            }


        } catch (IOException e) {

            e.printStackTrace();

        } finally {

            try {

                if (br != null)
                    br.close();

                if (fr != null)
                    fr.close();

            } catch (IOException ex) {

                ex.printStackTrace();

            }

        }

    }

}