const path = require('path');

// Set up logger
const logger = require('./logger');
logger('Started!');

const os = require('os');
const networkInterfaces = os.networkInterfaces();
let ipAddress = '';
for (let interface in networkInterfaces) {
    for (let address of networkInterfaces[interface]) {
        if (address.family === 'IPv4' && !address.internal) {
            ipAddress = address.address;
            break;
        }
    }
}
console.log(`Ip address of server: ${ipAddress}`);

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
	pythonProcess.stdout.on('data', (full_output) => {
		// I should find out the data type sometime...
		//output = output.toString();
		full_output = full_output.toString().split("\n");

		for(let i=0;i<full_output.length;i++) {
			output = full_output[i]
			console.log(`python process ${id} return value: ${output}`);
			logger(`python process ${id} return value: ${output}`);

			// Starting to read things (data output)
			let instruction = output.split(" ")[0];
			if (instruction == "error") { // This is if the python process reports an error in something (server side)
				// Potential security vulnerability if we reveal things - oh wait it's open source
				// And then I realized that this is for corrupted or otherwise incorrect data files on the server
				//client.send(output);
				pythonProcess.kill('SIGINT');
				logger(`python process ${id} terminated`); // We don't want to mix up different processes while reading the logs
				// We don't wanna use up all the server's memory and have id's going past the integer limit :)
				freeId(id);
			} else if (instruction == "invalid_input") { // This is if the player tries to do something illegal (move across the entire map, for instance)
				// Will be not possible to do if using the UI normally
				pythonProcess.kill('SIGINT');
				logger(`python process ${id} terminated`);
				// Let's not use up the server's resources, shall we?
				freeId(id);
			} else if (instruction == "data_update") { // This should be one of the main things that run
				// It will run if the client sends a valid instruction
				sendDataToEachClient(output);
			} else if (instruction == "client_info") { // This should be one of the main things that run
				// If the program needs to send data only to the client that sent the instruction
				client.send(`${instruction}`);
			} else if (instruction == "exit") { // This should be one of the main things that run
				// If the python process needs to exit (debugging or done processing the client instruction)
				pythonProcess.kill('SIGINT');
				logger(`python process ${id} terminated`);
				freeId(id);
			} else { // Not sure why or how this would happen
				pythonProcess.kill('SIGINT');
				logger(`python process ${id} terminated`);
				freeId(id);
			}
		}
	});

	pythonProcess.stderr.on('data', (error) => {
		// We don't worry about this - but log it anyways
		logger(`python process ${id} error: ${error}`);
		pythonProcess.kill('SIGINT');
		freeId(id);
		//console.error(`python error: ${error}`);
	});

	pythonProcess.on('close', (code) => {
	  logger(`python process exited with code ${code}`);
	});
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
		handleDataFromClient(data, ws);
		//sendDataToEachClient(data);
	})
	// This is confusing to read - it is two words "on error"
	ws.onerror = function () {
		console.log('websocket error');
	}
});
