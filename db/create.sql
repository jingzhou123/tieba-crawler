create database if not exists tieba;
use tieba;

create table if not exists user (
    id int not null auto_increment,
    name char(128) not null unique,
    admin_type enum('none', 'admin', 'little_admin', 'img_admin') default 'none',
    following_num smallint default 0,
    followed_num smallint default 0,
    tieba_age tinyint default 0,
    posts_num int default 0,
    primary key (id)
)default charset=utf8;

create table if not exists post (
    id int not null auto_increment,
    author_id int not null,
    tieba_id int not null,
    reply_id int default 0,
    title char(128) not null,
    body text not null,
    post_time datetime not null,
    reply_num int default 0,
    primary key (id)
)default charset=utf8;

create table if not exists tieba (
    id int not null auto_increment,
    name char(128) not null unique,
    followed_num int default 0,
    admin_num smallint default 0,
    posts_num int default 0,
    slogan char(128) default '',
    belong_dir char(128) default '',
    primary key (id)
)default charset=utf8;

create table if not exists user_follow_tieba (
    user_id int not null,
    tieba_id int not null,
    primary key (user_id, tieba_id)
)default charset=utf8;

create table if not exists user_manage_tieba (
    user_name char(128) not null,
    tieba_name char(128) not null,
    primary key (user_name, tieba_name)
)default charset=utf8;

create table if not exists user_follow_user (
    from_user_id int not null,
    to_user_id int not null,
    primary key (from_user_id, to_user_id)
)default charset=utf8;

create table if not exists user_followed_user (
    from_user_id int not null,
    to_user_id int not null,
    primary key (from_user_id, to_user_id)
)default charset=utf8;

