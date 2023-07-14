const express = require('express');
const app = express();
const fs = require('fs');
const csv = require('csv-parser');
const cors = require('cors');

const corsOptions = {
    origin: 'http://localhost:3001',
};
app.use(cors(corsOptions));

async function processCSV(filePath) {
    return new Promise((resolve, reject) => {
        const results = [];
        fs.createReadStream(filePath)
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            resolve(results);
        })
        .on('error', (err) => {
            reject(err);
        }
    )});
};

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.get("/api/companies", (req, res) => {
    console.log("GET /api/companies");
    const filePath = "companies.csv";
    processCSV(filePath)
    .then(data => {
        res.send(data);
    })
    .catch(err => {
        console.log(err);
        res.status(500).send("Internal Server Error");
    });
});

const port = process.env.PORT || 3002;
app.listen(port, () => console.log(`Listening on port ${port}...`));
