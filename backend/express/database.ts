import { Sequelize } from "sequelize";

// import 'dotenv/config.js'; //read .env file and make it available in process.env

export const database = new Sequelize(
  "sqlite:database.db",  
  {
    storage: './database.db',
    dialect: 'sqlite',
    logging: false
  }
);


// -- synchronize schema (creates missing tables) --
// Per ambienti di sviluppo rapido, sync({ alter: true }) ti risparmia il lavoro manuale.
// force: true
// { alter: true}
// database.sync({ alter: true}).then( () => {
//   console.log("Database synced correctly");
// }).catch( err => {
//   console.error("Error with database synchronization: " + err.message);
// });