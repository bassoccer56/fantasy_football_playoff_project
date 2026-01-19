const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Fantasy Football API is Running!');
});

// Change this line
app.listen(port, '0.0.0.0', () => {
  console.log(`API listening at http://0.0.0.0:${port}`);
});