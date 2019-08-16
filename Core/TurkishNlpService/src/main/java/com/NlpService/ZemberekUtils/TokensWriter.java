package com.NlpService.ZemberekUtils;


import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Arrays;
import java.util.List;


public class TokensWriter {

    private String filePath;
    private boolean appendOption = false;

    public TokensWriter(String filePath){
        this.filePath = filePath;
    }

    public TokensWriter(String filePath, Boolean a){
        this.filePath = filePath;
        appendOption = a;
    }

    public void writeTo_TXT(String Content){

        String[] str_arr = Content.split(" ");
        List<String> lines = Arrays.asList(str_arr);

        Path file = Paths.get(filePath + "tokens_processed.txt");

        try {

            if(!file.toFile().exists()|| !appendOption){
                Files.write(file, lines, StandardCharsets.UTF_8, StandardOpenOption.CREATE);
            }
            else{Files.write(file, lines, StandardCharsets.UTF_8, StandardOpenOption.APPEND);}


        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void writeTo_TXT (List<String> doc){

        File file = new File(filePath + "tokens_processed.txt");


        FileWriter writer = null;

        try {
            writer = new FileWriter(file, appendOption);
            BufferedWriter bw = new BufferedWriter(writer);
            for (String word : doc){
                bw.write(word + " ");
            }

            bw.write("\n");
            bw.close();
            writer.close();

        } catch (IOException e) {
            System.err.format("IOException: %s%n", e);
            e.printStackTrace();
        }

    }

    public void writeTo_CSV(){}



}
