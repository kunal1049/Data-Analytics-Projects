package com.bezkoder.spring.datajpa.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.bezkoder.spring.datajpa.model.Tutorial;

public interface TutorialRepository extends JpaRepository<Tutorial, Long> {
	
	List<Tutorial> findByWorkspaceContaining(String workspace);
	List<Tutorial> findByTitleContaining(String title);
}
