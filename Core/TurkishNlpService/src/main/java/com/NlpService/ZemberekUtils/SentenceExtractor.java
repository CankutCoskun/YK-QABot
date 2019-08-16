package com.NlpService.ZemberekUtils;

import zemberek.tokenization.TurkishSentenceExtractor;

import java.util.List;

public class SentenceExtractor {

    private TurkishSentenceExtractor extractor = TurkishSentenceExtractor.DEFAULT;

    public SentenceExtractor() {

    }

    public List<String> extract(String input_text){

        return extractor.fromDocument(input_text);
    }


}
