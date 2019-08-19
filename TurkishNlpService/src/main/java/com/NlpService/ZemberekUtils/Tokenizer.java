package com.NlpService.ZemberekUtils;

import zemberek.tokenization.Token;
import zemberek.tokenization.TurkishTokenizer;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class Tokenizer {

    private TurkishTokenizer tokenizer = TurkishTokenizer.DEFAULT;

    private List<String> stopWords = new ArrayList<String>();

    private List<String> initStopWords()throws IOException {


        String fname =  "stopwords_tr.txt";
        ClassLoader classLoader = ClassLoader.getSystemClassLoader();
        File stopWordsText = new File(classLoader.getResource(fname).getFile());
        //File is found

        if (stopWordsText.exists()){

            try (BufferedReader br = new BufferedReader(new FileReader(stopWordsText))) {
                for (String line; (line = br.readLine()) != null; ) {
                    // process the line.
                    stopWords.add(line);
                }
                // line is not visible here.
            } catch (IOException e) {
                e.printStackTrace();
            }

            //System.out.println(stopWords);
            return stopWords;

        }

        else {
           throw new IOException("stopwords file could not found");
        }

    }

    public boolean stringContainsNumber( String s )
    {
        return Pattern.compile( "[0-9]" ).matcher( s ).find();
    }

    private boolean isStopWord(String word) {

        if (stopWords.contains(word))
            return true;

        return false;

    }

    public List<Token> tokenize(String text) {

        List<Token> tokens = tokenizer.tokenize(text);

        try {
            initStopWords();
        } catch (IOException e) {
            e.printStackTrace();
        }

        int idx = 0;

        while (idx < tokens.size()) {
            if (isStopWord(tokens.get(idx).getText()) || stringContainsNumber(tokens.get(idx).getText())) {
                //System.out.println("Removed stop words " + tokens.get(idx).getText());
                tokens.remove(idx);
            }
            else
                idx++;
        }

        return tokens;
    }
}
