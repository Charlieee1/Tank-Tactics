// Web page
const path = require('path')

const express = require('express')
const webserver = express()
webserver.use(express.static(path.join(__dirname, 'webpage')))
//webserver.use((req, res) =>
//   res.sendFile('/webpage/index.html', { root: __dirname })
// )
//webserver.use((req, res) =>
//   res.sendFile('/main.js', {root: __dirname})
// )
webserver.listen(3000, () => console.log(`Listening on ${3000}`))

// Actual good stuffs
//const { spawn } = require('child_process');
//const script = "main.py"
//
//function handleDataFromClient(data, client) {
//	let pythonProcess = spawn('python', [script, data])
//  console.log(`Running python with input: ${data}`)
//
//	pythonProcess.stdout.on('data', (output) => {
//		pythonProcess.kill('SIGINT')
//		console.log(`python return value: ${output}`);
//		if output == "error" {
//			client.send(output)
//		} else {
//			sendDataToEachClient(output)
//		}
//	});
//
//	//pythonProcess.stderr.on('data', (error) => {
//	//  console.error(`python error: ${error}`);
//	//});
//
//	//pythonProcess.on('close', (code) => {
//	//  console.log(`child process exited with code ${code}`);
//	//});
//}

// Web socket
const { WebSocketServer } = require('ws')
const sockserver = new WebSocketServer({ port: 443 })

function sendDataToEachClient(data) {
	console.log(`Distributing message: ${data}`)
	sockserver.clients.forEach(client => {
		client.send(`${data}`)
	})
}

sockserver.on('connection', ws => {
 console.log('New client connected!')
 ws.send('Connection established!')
 ws.on('close', () => console.log('Client has disconnected!'))
 ws.on('message', data => {
   sendDataToEachClient(data)
 })
 ws.onerror = function () {
   console.log('websocket error')
 }
})
