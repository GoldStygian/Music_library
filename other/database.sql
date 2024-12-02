CREATE TABLE artista (
    id UUID PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    sort_name VARCHAR(100),
    area VARCHAR(100)
);

CREATE TABLE album (
    id UUID PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data DATE,
    artista_id UUID REFERENCES artista(id)
);

CREATE TABLE artista_album (
    artista_id UUID REFERENCES artista(id),
	album_id UUID REFERENCES album(id)
);

CREATE TABLE traccia (
    id UUID PRIMARY KEY,
    titolo VARCHAR(200) NOT NULL,
    durata TIME,
    autore VARCHAR(100),
    artisti_partecipanti TEXT, -- Per gestire più artisti in una traccia
    type VARCHAR(50),
    posizione INTEGER,
    album_id UUID REFERENCES album(id)
);

CREATE TABLE playlist (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    utente_id INTEGER REFERENCES auth_user(id)
);

CREATE TABLE playlist_traccia (
    playlist_id INTEGER REFERENCES playlist(id),
    traccia_id UUID REFERENCES traccia(id),
    PRIMARY KEY (playlist_id, traccia_id) -- Chiave primaria composta
);