const express = require('express');
const path = require('path');

const app = express();

// Serve static files from the 'Bubble' directory
app.use(express.static(path.join(__dirname, 'Bubble')));

// Define routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/htmlCode/index.html'));
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});