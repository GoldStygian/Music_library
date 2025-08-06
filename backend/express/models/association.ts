// src/models/index.ts
import { database } from '../database';
import { Album } from './Album';
import { Artist } from './Artist';
import { ArtistAlbum } from './ArtistAlbum';
import { Track } from './Track';

// N:N tra Artist e Album
Artist.belongsToMany(Album, {
  through: ArtistAlbum,
  foreignKey: 'artista_id',
  otherKey: 'album_id'
});
Album.belongsToMany(Artist, {
  through: ArtistAlbum,
  foreignKey: 'album_id',
  otherKey: 'artista_id'
});

// 1:N tra Album e Track
Album.hasMany(Track, {
  foreignKey: 'album_id'
});
Track.belongsTo(Album, {
  foreignKey: 'album_id'
});

export {
  Album,
  Artist,
  ArtistAlbum,
  Track
};