const path = require('path');

// Web page
const express = require('express');
const webserver = express();
webserver.use(express.static(path.join(__dirname, 'webpage')));
//webserver.use((req, res) =>
//   res.sendFile('/webpage/index.html', { root: __dirname })
// )
//webserver.use((req, res) =>
//   res.sendFile('/main.js', {root: __dirname})
// )
webserver.listen(3000, () => console.log(`Listening on ${3000}`));

// Set up logger
const logger = require('./logger');
logger('Started!');

// Set up uniqueID
const {getUniqueId, freeId} = require('./uniqueID');
//const getUniqueID = require('./getUniqueID');
//const freeID = require('./freeID');
freeId(getUniqueId());

// Actual good stuffs
const { spawn } = require('child_process');
const script = "python server/main.py";

function handleDataFromClient(data, client) {
	let pythonProcess = spawn('python', [script, data]);
	let id = getUniqueId();
	console.log(`Running python with input: ${data}, and id: ${id}`);
	logger(`Running python with input: ${data}, and id: ${id}`);

	pythonProcess.stdout.on('data', (output) => {
		output = output.toString();
		pythonProcess.kill('SIGINT');
		console.log(`python process ${id} return value: ${output}`);
		logger(`python process ${id} return value: ${output}`);
		let instruction = output.split(" ")[0];
		if (instruction == "error") {
			client.send(output);
		} else if (instruction == "invalid_input") {
		} else if (instruction == "data_update") {
			sendDataToEachClient(output);
		} else if (instruction == "none") {
		} else {}
		freeId(id);
	});

	pythonProcess.stderr.on('data', (error) => {
		// We don't worry about this - but log it anyways
		logger(`python process ${id} error: ${error}`);
		pythonProcess.kill('SIGINT');
		freeId(id);
		//console.error(`python error: ${error}`);
	});

	//pythonProcess.on('close', (code) => {
	//  console.log(`child process exited with code ${code}`);
	//});
}

// Web socket
const { WebSocketServer } = require('ws')
const sockserver = new WebSocketServer({ port: 443 })

function sendDataToEachClient(data) {
	console.log(`Distributing message: ${data}`);
	logger(`Distributing message: ${data}`);
	sockserver.clients.forEach(client => {
		client.send(`${data}`);
	})
}

sockserver.on('connection', ws => {
	console.log('New client connected!');
	ws.send('Connection established!');
	ws.on('close', () => console.log('Client has disconnected!'))
	ws.on('message', data => {
		handleDataFromClient(data);
		sendDataToEachClient(data);
	})
	ws.onerror = function () {
		console.log('websocket error');
	}
})
