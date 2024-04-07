const express = require('express');
const path = require('path');
const app = express();
const port = 3002;

// Serve static files from the 'src' directory
app.use(express.static(path.join(__dirname, 'src')));

// Serve static images from the 'img' directory
app.use('/img', express.static(path.join(__dirname, 'src', 'img')));

// Define routes to serve specific HTML files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'src', 'htmlCode', 'index.html'));
});

app.get('/chatroom', (req, res) => {
  res.sendFile(path.join(__dirname, 'src', 'htmlCode', 'chatroom.html'));
});
app.get('/homePage', (req, res) => {
  res.sendFile(path.join(__dirname, 'src', 'htmlCode', 'homePage.html'));
});

app.get('/signup', (req, res) => {
  res.sendFile(path.join(__dirname, 'src', 'htmlCode', 'signUp.html'));
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
