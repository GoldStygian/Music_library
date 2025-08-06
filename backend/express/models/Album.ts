// src/models/Album.ts
import { DataTypes, Model } from 'sequelize';
import { database } from '../database';

export class Album extends Model {
  public id!: string;
  public title!: string;
  public release_date?: string;
}

Album.init({
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  title: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  release_date: {
    type: DataTypes.STRING(100),
    allowNull: true
  }
}, {
  sequelize: database,
  tableName: 'album',
  timestamps: false
});
