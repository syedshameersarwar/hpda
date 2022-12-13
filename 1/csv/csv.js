const fs = require("fs");

const fileName = process.argv[2];

const data = fs.readFileSync(fileName, "utf8");

const rows = data.split("\n").filter(l => l.trim().length > 0);

const sums = [];

for (const row of rows.slice(1)) {
  const cols = row.trim().split(",");
  if (row.length > 0) {
    for (let i = 0; i < cols.length; i++) {
      sums[i] = (sums[i] || 0) + parseFloat(cols[i]);
    }
  }
}


const means = sums.map((sum) => parseFloat(sum / (rows.length - 1)));

console.log(means);
