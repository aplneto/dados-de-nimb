CREATE TABLE IF NOT EXISTS servidores (
    guild_name TEXT,
    guild_id INTEGER NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS rolagens (
    apelido TEXT,
    dados TEXT,
    g_id INTEGER,
    FOREIGN KEY (g_id) REFERENCES guild_id,
    PRIMARY KEY(apelido, g_id)
)