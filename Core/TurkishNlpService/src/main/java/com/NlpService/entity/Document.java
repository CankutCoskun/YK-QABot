package com.NlpService.entity;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Document {
    @Id
    @GeneratedValue
    private long id;

    private String content;

    public void setId(Long id) {
        this.id = id;
    }

    public long  getId() {
        return id;
    }


    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

}