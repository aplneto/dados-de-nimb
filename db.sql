CREATE TABLE IF NOT EXISTS servidores (
    guild_name TEXT,
    guild_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS rolagens (
    apelido TEXT,
    dados TEXT,
    g_id INTEGER,
    c_id INTEGER,
    FOREIGN KEY (g_id) REFERENCES guild_id,
    PRIMARY KEY(apelido, g_id)
);

CREATE TABLE IF NOT EXISTS favoritas (
    apelido TEXT,
    dados TEXT,
    u_id INTEGER,
    FOREIGN KEY (u_id) REFERENCES usr_id,
    PRIMARY KEY (apelido, u_id)
);

CREATE TABLE IF NOT EXISTS usrs (
    usr_id INTEGER PRIMARY KEY,
    usr_name TEXT
);