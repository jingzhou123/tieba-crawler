create database if not exists tieba;
use tieba;

create table if not exists user (
    user_id int not null auto_increment,
    user_name char(128) not null unique,
    tieba_name char(128) default '',
    admin_type enum('none', 'admin', 'little_admin', 'img_admin') default 'none',
    following_num smallint default 0,
    followed_num smallint default 0,
    primary key (user_id)
)default charset=utf8;
