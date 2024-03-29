create database opendata;
use opendata;

create table dataset_list(
    -> id int NOT NULL AUTO_INCREMENT,
    -> package_name varchar(250),
    -> PRIMARY KEY(id)
    -> );

create table tag_list(
    -> tag_id int NOT NULL AUTO_INCREMENT,
    -> tag varchar(250),
    -> PRIMARY KEY(tag_id)
    -> );

create table org_list(
        org_id int NOT NULL AUTO_INCREMENT,
    -> organization varchar(250),
    -> PRIMARY KEY(org_id)
    -> );

)

create table mydatasets(
    -> id int NOT NULL AUTO_INCREMENT,
    -> dataset varchar(250),
    -> PRIMARY KEY(id)
    -> );

CREATE TABLE datasets (
  -> id varchar(40) NOT NULL,
  -> package_id varchar(40) DEFAULT NULL,
  -> name varchar(250) DEFAULT NULL,
  -> description varchar(250) DEFAULT NULL,
  -> url varchar(400) DEFAULT NULL,
  -> format varchar(50) DEFAULT NULL,
  -> created date DEFAULT NULL,
  -> PRIMARY KEY (id)
  ->  );