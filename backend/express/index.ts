import express from "express";
import morgan from "morgan";
import cors from "cors";
import { database } from './database';
import { trackRouter } from "./routers/trackRouter";

const SERVER_PORT = 3000;

const app = express(); // Crea un'applicazione Express

app.use(express.json()); // Parse incoming requests with a JSON payload
app.use(morgan('dev')); // log
app.use(cors());

//Routes
app.use("/tracks", trackRouter);

database.sync({ alter: true })
  .then(() => console.log('✅ Database synced'))
  .catch(e => console.error('❌ Sync error:', e));

app.listen(SERVER_PORT);

console.log("Server are listening at:", SERVER_PORT);
console.log("http://localhost:"+SERVER_PORT);