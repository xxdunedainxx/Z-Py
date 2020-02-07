CREATE database static_host_mgmt;
use static_host_mgmt;

CREATE TABLE static_host_site (
    uid int NOT NUll AUTO_INCREMENT,
    name varchar(333) NOT Null,
    required_permission varchar(333),
    whenGenerated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(uid)
)ENGINE=MyISAM;


CREATE TABLE user (
    username varchar(333),
    email varchar(333),
    password varchar(333) DEFAULT null, # null if auth is from non-local source (AD for example)
    uid int NOT NUll AUTO_INCREMENT,
    enabled int DEFAULT 1,
    source varchar(333),
    whenGenerated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(uid)
)ENGINE=MyISAM;

CREATE TABLE user_source (
    value varchar(333),
    # 1 == enabled, 0 == off
    enabled int DEFAULT 1,
    PRIMARY key(value)
)ENGINE=MyISAM;

# Source values
INSERT INTO user_source (value, enabled) VALUES ('AD', 1);
INSERT INTO user_source (value, enabled) VALUES ('local', 1);

# default  user table insert
INSERT INTO user (username, email, password, enabled, source) VALUES ('admin', 'admin@email.com', 'changeme',1, 'local');

# permissions == 'admin', 'write', 'read'

CREATE TABLE permission (
    uid int NOT NULL,
    value varchar(333) DEFAULT "read",
    CONSTRAINT perm PRIMARY KEY(value,uid)
)ENGINE=MyISAM;

INSERT INTO permission (uid, value) VALUES (1,"admin");
