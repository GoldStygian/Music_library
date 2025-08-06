// src/models/Track.ts
import { DataTypes, Model, Optional } from 'sequelize';
import { database } from '../database';

interface TrackAttributes {
  id: string;
  title: string;
  author: string;
  participating_artists?: string | null;
  albumId?: string | null;
  duration?: string | null;
  file_name: string;
  variant: number;
  play_count?: number;
}

// Optional fields for creation
type TrackCreationAttributes = Optional<TrackAttributes, 'id' | 'participating_artists' | 'albumId' | 'duration' | 'play_count'>;

export class Track extends Model<TrackAttributes, TrackCreationAttributes> implements TrackAttributes {
  public id!: string;
  public title!: string;
  public author!: string;
  public participating_artists!: string | null;
  public albumId!: string | null;
  public duration!: string | null;
  public file_name!: string;
  public variant!: number;
  public play_count!: number;

  public readonly createdAt!: Date;
  public readonly updatedAt!: Date;
}

Track.init({
  id: {
    type: DataTypes.UUID,
    primaryKey: true,
    defaultValue: DataTypes.UUIDV4
  },
  title: {
    type: DataTypes.STRING(200),
    allowNull: false,
    field: 'titolo'
  },
  author: {
    type: DataTypes.STRING(100),
    allowNull: false,
    field: 'autore'
  },
  participating_artists: {
    type: DataTypes.STRING(255),
    allowNull: true,
    field: 'artisti_partecipanti'
  },
  albumId: {
    type: DataTypes.UUID,
    allowNull: true,
    field: 'album_id'
  },
  duration: {
    type: DataTypes.STRING(100),
    allowNull: true,
    field: 'durata'
  },
  file_name: {
    type: DataTypes.TEXT,
    allowNull: false,
    field: 'file_name'
  },
  variant: {
    type: DataTypes.INTEGER,
    allowNull: false,
    field: 'variant',
    validate: {
      min: 1,
      max: 10
    }
  },
  play_count: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  }
}, {
  sequelize: database,
  tableName: 'traccia',
  timestamps: false,
  indexes: [
    {
      unique: true,
      fields: ['id', 'variant']
    }
  ]
});
