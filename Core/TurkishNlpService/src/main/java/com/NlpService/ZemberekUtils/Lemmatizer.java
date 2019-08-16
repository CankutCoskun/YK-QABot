package com.NlpService.ZemberekUtils;

import zemberek.morphology.TurkishMorphology;
import zemberek.morphology.analysis.SingleAnalysis;
import zemberek.tokenization.Token;

import java.util.ArrayList;
import java.util.List;


public class Lemmatizer {

    private TurkishMorphology morphology = TurkishMorphology.createWithDefaults();


    public List<String> lemmatize(List<Token> tokens){

        List<String> tokens_str = new ArrayList<String>();

        for (Token tkn : tokens){

            if(tkn.getType() == Token.Type.Word || tkn.getType() == Token.Type.WordWithSymbol
                    || tkn.getType() == Token.Type.WordAlphanumerical){
                //System.out.println(tkn.getText());
                tokens_str.add(tkn.getText());
            }
        }

        ///Covert to string to disambiguate

        String listString = "";

        for (String s : tokens_str)
        {
            listString += s + "\t";
        }


        List<SingleAnalysis> analyses = morphology
                .analyzeAndDisambiguate(listString)
                .bestAnalysis();


        List<String> lemmas = new ArrayList<String>();
        for(SingleAnalysis singleAnalysis : analyses ) {

                String lem = singleAnalysis.getLemmas().get(0);
            if ( lem != "UNK")
                lemmas.add(singleAnalysis.getLemmas().get(0));
        }

        return lemmas;
    }


}
