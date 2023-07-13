# Tank-Tactics
Implementation of the game showcased in [The Game Prototype That Had to Be Banned by Its Own Studio](https://www.youtube.com/watch?v=aOYbR-Q_4Hs) [NOT FINISHED]

## Build Instructions
For any operating system, install nodeJS.
### Windows
Navigate to your working directory and run the following commands:
```
git clone https://github.com/Charlieee1/Tank-Tactics.git
cd Tank-Tactics
npm_install.bat
```
To start the server, run the `start_server.bat` batch file:
```
start_server.bat
```
Open [localhost:3000/](http://localhost:3000/) in your browser. It will not open automatically.

### Linux
**These instructions have not been tested. Please note that you may need to run `chmod +x <.sh file>` to run the scripts.**  
  
Navigate to your working directory and run the following commands:
```
git clone https://github.com/Charlieee1/Tank-Tactics.git
cd Tank-Tactics
npm_install.sh
```
To start the server, run the `start_server.sh` file:
```
start_server.sh
```
Open [localhost:3000/](http://localhost:3000/) in your browser. It will not open automatically.

## TODO:
- Make backend functional
  - Add game reset
  - Add voting
  - Add ticking utilities
    - Action points rewarding
    - Voting result handling
    - Expiring session tokens
  - Add user account control system
    - Account creation
    - Logging in
    - Use temporary session tokens instead of passwords that are logged as plaintext (oops)
    - Logging out
- Make frontend
  
Percent complete: 20%  
**Will gladly accept contributions!**
