import { Router } from "express";
import path from "path";
import { fileURLToPath } from "url";
// import { ResetController } from "../controllers/ResetController.js";

// export const rootRouter = new express.Router();
export const rootRouter = Router();
const __dirname = path.dirname(fileURLToPath(import.meta.url));