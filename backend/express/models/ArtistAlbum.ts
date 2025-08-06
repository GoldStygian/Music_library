// src/models/ArtistAlbum.ts
import { DataTypes, Model } from 'sequelize';
import { database } from '../database';

export class ArtistAlbum extends Model {
  public artistId!: string;
  public albumId!: string;
  public owner!: boolean;
}

ArtistAlbum.init({
  artistId: {
    type: DataTypes.UUID,
    allowNull: false,
    field: 'artista_id',
    primaryKey: true
  },
  albumId: {
    type: DataTypes.UUID,
    allowNull: false,
    field: 'album_id',
    primaryKey: true
  },
  owner: {
    type: DataTypes.BOOLEAN,
    allowNull: false,
    field: 'proprietario'
  }
}, {
  sequelize: database,
  tableName: 'artista_album',
  timestamps: false
});
