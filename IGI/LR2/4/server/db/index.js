const mongoose = require('mongoose');

const connectionString = 'mongodb://mongo:27017/cinema'; //For use mongo on docker
//const connectionString = 'mongodb://localhost:27017/cinema';// For local testing

mongoose.connect(connectionString, { useNewUrlParser: true, useUnifiedTopology: true  }).catch((e) => {
  console.error('Connection error', e.message);
});

const db = mongoose.connection;

module.exports = db;
