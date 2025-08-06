import { Router, Request, Response, NextFunction } from 'express';
import * as db from '../models/association';

export const trackRouter = Router();

trackRouter.get("/", async (req: Request, res: Response, next: NextFunction) => {
  try {
    const tracks = await db.Track.findAll();
    res.json(tracks);
  } catch (err) {
    next(err);
  }
});