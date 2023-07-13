// logger.js
const fs = require('fs');
const path = require('path');

const logDir = './logs';
const logFile = path.join(logDir, 'log.txt');

// Create logs directory if it doesn't exist
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}

// Rename old log file
if (fs.existsSync(logFile)) {
  let i = 0;
  while (fs.existsSync(path.join(logDir, `log${i}.txt`))) {
    i++;
  }
  fs.renameSync(logFile, path.join(logDir, `log${i}.txt`));
}

// Create new log file
fs.writeFileSync(logFile, '');

// Create logger function
function logger(message) {
  const date = new Date();
  const formattedDate = date.toLocaleString('en-GB', { timeZone: 'UTC' });
  const lines = message.split('\n');
  const space = ' '.repeat(formattedDate.length + 3);
  for (let i = 0; i < lines.length; i++) {
    if (i === 0) {
      fs.appendFileSync(logFile, `[${formattedDate}] ${lines[i]}\n`);
    } else {
      fs.appendFileSync(logFile, `${space}${lines[i]}\n`);
    }
  }
}

module.exports = logger;
