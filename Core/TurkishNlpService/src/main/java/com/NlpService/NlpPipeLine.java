package com.NlpService;

import com.NlpService.ZemberekUtils.Lemmatizer;
import com.NlpService.ZemberekUtils.Tokenizer;
import zemberek.tokenization.Token;

import java.io.*;
import java.util.*;

public class NlpPipeLine {

    private static void readData(String pathName, List<String> docs){

        File file = new File(pathName);

        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(file));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        String doc = "";

        do {
            try {
                if (!doc.contentEquals("")){
                    docs.add(doc);
                }
                doc = br.readLine();

            }catch (IOException e){
                e.printStackTrace();
            }
        }while (doc != null);
    }

    public List<List<String>> processDocument(String pathName) throws IOException {
        //Read content from a txt file separated by new line

        List<String> docs = new ArrayList<String>();
        readData(pathName, docs);

        System.out.println("Service is called for document: " + pathName + "\ndocument size: " );
        System.out.println( docs.size());

        Tokenizer tokenizer = new Tokenizer();
        Lemmatizer lemmatizer = new Lemmatizer();
        //TokensWriter tkWriter = new TokensWriter("---",true);

        int counter = 0;

        List<List<String>> allLemmas = new ArrayList<>();

        for (String doc: docs){
            List<Token> tokens = tokenizer.tokenize(doc);
            List<String> lemmas = lemmatizer.lemmatize(tokens);
            //lemmas.forEach(s-> System.out.println(s));
            counter++;
            //tkWriter.writeTo_TXT(lemmas);

            allLemmas.add(lemmas);

        }

        return allLemmas;

    }

    public List<String> processInput(String rawInput){

        System.out.println("Service is called for: " + rawInput );

        Tokenizer tokenizer = new Tokenizer();
        Lemmatizer lemmatizer = new Lemmatizer();

        List<Token> tokens = tokenizer.tokenize(rawInput);
        List<String> lemmas = lemmatizer.lemmatize(tokens);

        System.out.println("input: " + rawInput);
        System.out.println("returned tokens: ");
        System.out.println(lemmas);

        return lemmas;
    }
}
