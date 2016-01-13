create database if not exists tieba;
use tieba;

create table if not exists user (
    id int not null auto_increment,
    baidu_id binary(32) default '',
    name char(128) not null unique,
    admin_type enum('none', 'admin', 'little_admin', 'img_admin') default 'none',
    following_num smallint default 0,
    followed_num smallint default 0,
    tieba_age float default 0,
    posts_num int default 0,
    primary key (id)
)default charset=utf8;

create table if not exists fan (
    id int not null auto_increment,
    baidu_id binary(32) default '',
    name char(128) not null unique,
    admin_type enum('none', 'admin', 'little_admin', 'img_admin') default 'none',
    following_num smallint default 0,
    followed_num smallint default 0,
    tieba_age float default 0,
    posts_num int default 0,
    primary key (id)
)default charset=utf8;

create table if not exists follow (
    id int not null auto_increment,
    baidu_id binary(32) default '',
    name char(128) not null unique,
    admin_type enum('none', 'admin', 'little_admin', 'img_admin') default 'none',
    following_num smallint default 0,
    followed_num smallint default 0,
    tieba_age float default 0,
    posts_num int default 0,
    primary key (id)
)default charset=utf8;

create table if not exists comment (
    id bigint not null,
    reply_id bigint not null,
    author_name char(128) not null,
    body text,
    post_time datetime,
    primary key (id)
)default charset=utf8;

create table if not exists post (
    id bigint not null,
    author_name char(128) not null,
    tieba_name char(128) not null,
    title char(128) not null,
    body text,
    post_time datetime,
    reply_num int default 0,
    tag char(32) default '',
    index tag (tag),
    primary key (id)
)default charset=utf8;

create table if not exists reply (
    author_name char(128) not null,
    body text,
    id bigint not null,
    title char(128) not null,
    post_time datetime,
    post_id bigint not null,
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
    tag char(32) default '',
    primary key (id),
    index tag (tag)
)default charset=utf8;

create table if not exists user_follow_tieba (
    user_name char(128) not null,
    tieba_name char(128) not null,
    primary key (user_name, tieba_name)
)default charset=utf8;

create table if not exists user_manage_tieba (
    user_name char(128) not null,
    tieba_name char(128) not null,
    primary key (user_name, tieba_name)
)default charset=utf8;

create table if not exists user_follow_user (
    from_user_name char(128) not null,
    to_user_name char(128) not null,
    primary key (from_user_name, to_user_name)
)default charset=utf8;

create table if not exists user_followed_user (
    from_user_name char(128) not null,
    to_user_name char(128) not null,
    primary key (from_user_name, to_user_name)
)default charset=utf8;

