create database if not exists `pywall`;
create user 'pywall'@'localhost' identified by 'pywall';
grant all privileges on `pywall`.* to 'pywall'@'localhost';
use pywall;
create table `wall` (message varchar(255), posted_by varchar(255), posted_on datetime) ENGINE=InnoDB;
flush privileges
