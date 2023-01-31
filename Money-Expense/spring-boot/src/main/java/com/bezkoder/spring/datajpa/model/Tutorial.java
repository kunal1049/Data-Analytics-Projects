package com.bezkoder.spring.datajpa.model;

import javax.persistence.*;

import lombok.Data;

@Data
@Entity
@Table(name = "tutorials")
public class Tutorial {

	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private long id;

	@Column(name = "title")
	private String title;

	@Column(name = "description")
	private String description;
	
	@Column(name = "workspace")
	private String workspace;
	
	public Tutorial() {
		
	}
	
	public Tutorial(String title, String description, String workspace) {
		this.title = title;
		this.description = description;
		this.workspace = workspace;
	}

	@Override
	public String toString() {
		return "Tutorial [id=" + id + ", title=" + title + ", desc=" + description + ", workspace=" + workspace + "]";
	}

}
