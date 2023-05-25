const path = require('path');

// Set up logger
const logger = require('./logger');
logger('Started!');


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
// Don't forget to log everything that goes on :)
logger(`Listening on ${3000}`);


// Actual good stuffs (python integration)
const { spawn } = require('child_process');
// This is the main backend
const script = "python server/main.py";

// Set up uniqueID
const {getUniqueId, freeId} = require('./uniqueID');
// Testing if it works without errors
freeId(getUniqueId());

// Whenever a client sends some data to the server, this function will run the python backend to deal with the data
function handleDataFromClient(data, client) {
	// Spawning the python process and getting a unique id for the process
	let pythonProcess = spawn('python', [script, data]);
	let id = getUniqueId();
	
	console.log(`Running python with input: ${data}, and id: ${id}`);
	logger(`Running python with input: ${data}, and id: ${id}`);

	// If the python code figures something out, we want to be able to get something useful
	pythonProcess.stdout.on('data', (output) => {
		// I should find out the data type sometime...
		output = output.toString();
		// Let's not use up the server's resources, shall we?
		pythonProcess.kill('SIGINT');

		console.log(`python process ${id} return value: ${output}`);
		logger(`python process ${id} return value: ${output}`);

		// Starting to read things (data output)
		let instruction = output.split(" ")[0];
		if (instruction == "error") { // This is if the python process reports an error in something
			// Potential security vulnerability if we reveal things - oh wait it's open source
			// And then I realized that this is for corrupted or otherwise incorrect data files on the server
			//client.send(output);
		} else if (instruction == "invalid_input") { // This is if the player tries to do something illegal (move across the entire map, for instance)
		} else if (instruction == "data_update") { // This should be the main thing that runs
			// It will run if the client sends a valid instruction
			sendDataToEachClient(output);
		} else if (instruction == "none") { // If the python process needs to exit (debugging?)
		} else {} // Not sure why or how this would happen
		// We don't wanna use up all the server's memory and have id's going past the integer limit :)
		logger(`python process ${id} terminated`); // We don't want to mix up different processes while reading the logs
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
const { WebSocketServer } = require('ws');
const sockserver = new WebSocketServer({ port: 443 });

// Self explanatory
function sendDataToEachClient(data) {
	console.log(`Distributing message: ${data}`);
	logger(`Distributing message: ${data}`);
	sockserver.clients.forEach(client => {
		client.send(`${data}`);
	});
}

// For the actual websocket stuffs
sockserver.on('connection', ws => {
	console.log('New client connected!');
	ws.send('Connection established!');
	ws.on('close', () => console.log('Client has disconnected!'))
	ws.on('message', data => {
		handleDataFromClient(data);
		sendDataToEachClient(data);
	})
	// This is confusing to read - it is two words "on error"
	ws.onerror = function () {
		console.log('websocket error');
	}
});
