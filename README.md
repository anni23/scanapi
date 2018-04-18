***
# SCAN API - Implemented a rest api called scanapi to scan files for potential threats using Django restframework
***
## implementation Details
* Implemented a rest api called scanapi by using Django rest framework. This api takes in filename as a part of the request and then calls the metadefender.opswat.com api provided by OPSWAT.
* Using the Metadefender api, you can upload a file onto the cloud and scan the file for potential threats. Once you have uploaded and scanned a file, you can retrieve a json scan report, by calling the api.
* Metadefender api also provides a scan report caching mechanism, wherein, once you upload and scan a file, the report is cached in the cloud. 
* You can later retrieve a cached scan report, just by passing the hash of the file while calling the api.
* Scanapi makes use of all these facilities provided by Metadefender and provides a simple api that obtains response from Metadefender api, parses it and returns the response to the end user.
* If a file is being scanned for the first time, scanapi uploads and scans the file and then returns the report.
* If a file is rescanned, the scan api just retrieves the cached report by passing hash of the file to the Metadefender api.
***
## Source Code
#### The main source code that calls the metadefender api is in following directory:
```
/scanapi/webapp/scanfile.py
```
***
## Prerequisites
* #### Python3
* #### Git
***
## Two Approaches - There are two different ways in which this project can be executed.

* #### Make a call to scanapi, a rest api created by me that calls the Meta Defenfer api and return the results in json format. The results will be displayed on browser when scanapi is called.
* #### Run a simple python file and pass the file name of the file to be scanned as a command line argument. The output be will printed on the terminal itself.
***
## 1) Scanning the file by using rest api (scanapi) created by uisng the Django restframework.
## Initial Setup
***
Install pip.
```sh
$ sudo apt-get install python3-pip
```
Install Virtual Environment.
```sh
$ sudo pip3 install virtualenv
```
Create your project workspace folder (Lets say "opswat") and change directory to it. 
```sh
$ mkdir opswat
$ cd opswat
```
Clone the project from github into the opswat directory.
```sh
$ git clone https://github.com/anni23/scanapi.git
```
insert the apikey at line number 6 in the following python file:
opswat/scanapi/webapp/scanfile.py
```
Line 6 : api_key = "--put your apikey here--"
```
Create the virtual environment for your project.
```sh
$ virtualenv venv --no-site-packages
```
Activate the virtual environment.
```sh
$ source venv/bin/activate
```
install requests.
```sh
$ pip install requests
```
install django.
```sh
$ pip install django
```
install django rest-framework.
```sh
$ pip install djangorestframework
```
## Running the Django server
```sh
$ cd scanapi
$ python manage.py runserver
```
## Scanning the file
Put the file to be scanned in the following directory : opswat/scanapi/ 
Basically the  file to be scanned should be in the root directory of the Djando server.
```
Example : opswat/scanapi/file_name.txt 
``` 
## Viewing the results
Goto to any browser and type the following url:
```
http://localhost:8000/scanapi/file_name.extension
Example - http://localhost:8000/scanapi/sample.txt
```
***
## 2) Scanning the file by running a simple python program, which takes in filename as a command line argument.

## Initial Setup
Install pip.
```sh
$ sudo apt-get install python3-pip
```
Install Virtual Environment.
```sh
$ sudo pip3 install virtualenv
```
Create your project workspace folder (Lets say "opswat") and change directory to it. 
```sh
$ mkdir opswat
$ cd opswat
```
Clone the project from github into the opswat directory.
```sh
$ git clone https://github.com/anni23/scanapi.git
```
insert the apikey at line number 6 in the following python file:
opswat/scanapi/webapp/scanfile.py
```
Line 6 : api_key = "--put your apikey here--"
```
Create the virtual environment for your project.
```sh
$ virtualenv venv --no-site-packages
```
Activate the virtual environment.
```sh
$ source venv/bin/activate
```
install requests.
```sh
$ pip install requests
```
Uncomment the last two lines of code in the following file: 
opswat/scanapi/webapp/scanfile.py
```
file_name = sys.argv[1]
print(callScanAPI(file_name))
```
## Scanning the file
Put the file to be scanned in following directory:
opswat/scanapi/webapp/  
Basically, the file to be scanned should be in same directory as scanfile.py python file
```
Example : opswat/scanapi/webapp/file_name.txt 
``` 
## Viewing the results
Open the terminal
```sh
$ cd opswat/scanapi/webapp/
```
Type following command and hit enter:
```sh
$ python scanfile.py file_name.extension 
Example - $ python scanfile.py sample.txt
```
***

## Acknowledgments
[OPSWAT](https://www.opswat.com/)
***
## References
http://docs.python-requests.org/en/master/user/quickstart/
http://www.django-rest-framework.org/tutorial/quickstart/
https://www.youtube.com/watch?v=ejJ-2oz4AgI
https://www.geeksforgeeks.org/get-post-requests-using-python/
