// src/models/Artist.ts
import { DataTypes, Model } from 'sequelize';
import { database } from '../database';

export class Artist extends Model {
  public id!: string;
  public name!: string;
  public country?: string;
  public description?: string;
}

Artist.init({
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  name: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  country: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  }
}, {
  sequelize: database,
  tableName: 'artista',
  timestamps: false
});
