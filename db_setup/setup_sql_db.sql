create DATABASE TRANSFER_ME;
use TRANSFER_ME;

CREATE TABLE `TRANSFER_ME`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `role` INT ZEROFILL NOT NULL,
  `okta_id` VARCHAR(200) NOT NULL,
  `creation_time` DATETIME NULL,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `okta_id_UNIQUE` (`okta_id` ASC));

CREATE TABLE `TRANSFER_ME`.`article` (
  `article_id` INT NOT NULL AUTO_INCREMENT,
  `article_content` VARCHAR(5000) NULL,
  `user_id` INT NOT NULL,
  `like_count` INT ZEROFILL NULL,
  `view_count` INT ZEROFILL NULL,
  `click_count` INT ZEROFILL NULL,
  `post_time` DATETIME NULL,
  `last_updated_time` DATETIME NULL,
  `article_title` VARCHAR(500) NULL,
  `school_from` INT ZEROFILL NULL,
  `school_to` INT ZEROFILL NULL,
  `major` INT ZEROFILL NULL,
  `graduate_year` INT ZEROFILL NULL,
  `degree_type` INT ZEROFILL NULL,
  `is_spam` INT ZEROFILL NULL,
  `is_approved` TINYINT ZEROFILL NULL,
  PRIMARY KEY (`article_id`),
  UNIQUE INDEX `article_id_UNIQUE` (`article_id` ASC));

CREATE TABLE `TRANSFER_ME`.`comment` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `comment_content` VARCHAR(1000) NULL,
  `user_id` INT NOT NULL,
  `article_id` INT NOT NULL,
  `post_time` DATETIME NULL,
  `like_count` INT ZEROFILL NULL,
  `quote_id` INT NULL,
  `is_spam` INT ZEROFILL NULL,
  PRIMARY KEY (`comment_id`),
  UNIQUE INDEX `comment_id_UNIQUE` (`comment_id` ASC));

CREATE TABLE `TRANSFER_ME`.`user_article_interaction` (
  `user_id` INT NOT NULL,
  `article_id` INT NOT NULL,
  `like` TINYINT ZEROFILL NOT NULL,
  `mark_spam` TINYINT ZEROFILL NULL,
  `user_article_interaction_id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`user_article_interaction_id`),
  UNIQUE INDEX `user_article_interaction_id_UNIQUE` (`user_article_interaction_id` ASC));
