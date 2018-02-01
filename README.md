# CodyCloud-Client
It is build for a better managing of NGROK_Server

## Usage Examples:
* python3 main.py &  
* nohup python3 main.py &  
* (or like this if you just used the "setup.py" installer)  
  service codycloud start  

## How to Setup
- make sure you have a ***ngrok client*** exe in ***./bin*** folder(creat a ***./bin*** folder if it dosen't exist)
- make sure you have edited a ***config file*** of ***ngrok client*** 
- make sure you have edited the ***configs/codyclient.json*** correctly
- run "setup.py" file as root user acount and follow the step

## Config File Example (configs/codycloud.json)
>{  
  "ngrok_clients":{  
    "ebian_ngrok":{  
      "log_level":"ERROR",  
      "log_path":"logs/ngrok/ebian/ngrok.log",  
      "tunnels":{  
        "ssh":2200  
      },  
      "config_path":"configs/ebian_ngrok.cfg"  
    }  
  },  
  "server_addr":"example.com",  
  "server_port":2220,  
  "log_level":"DEBUG",  
  "base_key":"BasicLiveKey"  
>}  

## How to stop this service
- Create a file named **"CMD_STOP"** in the **"cache"** folder
- If the service stopped, there should be a file named **"FB_STOPPED"** in the **"cache"** folder
- or like this if you just used the "setup.py" installer  
    service codyclient stop
