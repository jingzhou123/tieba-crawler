insert ignore user (name) values('jz'), ('user_a');
insert ignore tieba (name) values('北京邮电大学');
insert ignore post values (default, 1, 1, default, 'title', 'body', '2015-12-3 11-11-11', 2),
                          (default, 1, 1, 1, 'reply', 'body', '2015-12-3 11-11-11', default),
                          (default, 2, 1, 1, 'reply', 'body', '2015-12-3 11-11-11', default);
insert ignore user_follow_tieba values(1, 1), (2, 1)

  
  
