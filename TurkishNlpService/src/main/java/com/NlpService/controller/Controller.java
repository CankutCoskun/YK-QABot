package com.NlpService.controller;

import com.NlpService.NlpPipeLine;
import com.NlpService.repository.DocumentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;


@RestController
public class Controller {

    private DocumentRepository documentRepository;

    @Autowired
    public Controller(DocumentRepository documentRepository) {
        this.documentRepository = documentRepository;
    }

    @RequestMapping(value = "/nlpPipeLine/singleInput" ,method = RequestMethod.GET)
    @ResponseBody
    public List<String> getProcessedTokens( @RequestParam(value = "rawInput") String rawInput){

        NlpPipeLine nlpPipeLine = new NlpPipeLine();
        List<String> processedTokens = nlpPipeLine.processInput(rawInput);
        return processedTokens;

    }

    @RequestMapping(value = "/nlpPipeLine/document", method = RequestMethod.GET)
    @ResponseBody
    public List<List<String>> getProcessedDoc(@RequestParam(value = "docPathName") String docPathName){
        NlpPipeLine nlpPipeLine = new NlpPipeLine();

        List<List<String>> docsLemmas = null;

        try {
            docsLemmas = nlpPipeLine.processDocument(docPathName);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return docsLemmas;
    }
/*
    @RequestMapping(value = "" ,method = RequestMethod.POST)
    public void postProcessedTokens(@RequestBody AddUserRequest addUserRequest)
    {
        Document doc = new Document();
        doc.setContent(addUserRequest.getContent());
        documentRepository.save(doc);
    }*/

}
