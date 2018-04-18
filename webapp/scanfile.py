import requests
import time
import sys
import json
import hashlib
api_key = "" #PLEASE ENTER THE API KEY HERE.

#function to compute the hash values of the input file.
def getHashValues(file_name):
	#md5.
	hasher = hashlib.md5()
	afile = open("./" + file_name, 'rb')
	buf = afile.read()
	hasher.update(buf)
	file_hash_md5 = hasher.hexdigest().upper() 
	#sha1.
	hasher = hashlib.sha1()
	afile = open("./" + file_name, 'rb')
	buf = afile.read()
	hasher.update(buf)
	file_hash_sha1 = hasher.hexdigest().upper() 
	#sha256.
	hasher = hashlib.sha256()
	afile = open("./" + file_name, 'rb')
	buf = afile.read()
	hasher.update(buf)
	file_hash_sha256 = hasher.hexdigest().upper() 
	return file_hash_md5, file_hash_sha1, file_hash_sha256

#function to upload the file and return the unique data id.
def uploadFile(file_name):
	file_upload_url = "https://api.metadefender.com/v2/file"
	file_upload_headers = {"apikey" : api_key}
	file_to_upload = {"file" : (file_name, open("./" + file_name, "rb"))}
	file_upload_response = requests.post(url = file_upload_url, headers = file_upload_headers, files = file_to_upload)
	file_upload_jsonres = file_upload_response.json()
	data_id = file_upload_jsonres['data_id']
	return data_id

#function to get the scan report, by passing the unique data_id obtained by uploading the file.
def getScanReport(data_id):
	scan_report_url = "https://api.metadefender.com/v2/file/" + data_id
	scan_report_headers = {"apikey" : api_key, "file_metadata" : "1"}
	scan_report_response = requests.get(url = scan_report_url, headers = scan_report_headers)
	scan_report_jsonres = scan_report_response.json()
	#check if the progress percent is 100%
	while(scan_report_jsonres["scan_results"]["progress_percentage"] != 100):
		scan_report_response = requests.get(url = scan_report_url, headers = scan_report_headers)
		scan_report_jsonres = scan_report_response.json()
	return scan_report_jsonres	

#This function is the entry point to the program, it takes in file_name as an argument.
def callScanAPI(file_name):
	#First we compute hash values of the file.
	file_hash_md5, file_hash_sha1, file_hash_sha256 = getHashValues(file_name)
	
	#Then we call the api to retrieve the scan reports using the data hash. 
	hash_report_url = "https://api.metadefender.com/v2/hash/" + file_hash_sha1
	headers = {"apikey" : api_key, "file_metadata" : "1"}
	hash_report_resp = requests.get(url = hash_report_url, headers = headers)
	hash_report_jsonres = hash_report_resp.json()
	
	#Check if the scan report is already available in the cache or is it a first time scan. 
	if file_hash_sha1 in hash_report_jsonres:    #its a first time scan, upload the file and perform the scan.
		print("Scan report not available in cache, its a first time scan, it will take a while")
		data_id = uploadFile(file_name)
		scan_report_jsonres = getScanReport(data_id)
		#Parse the response.
		result = {
			"report_available_in_cache" : "no",
			"filename" : scan_report_jsonres["file_info"]["display_name"], 
			"overall_status" : scan_report_jsonres["scan_results"]["scan_all_result_a"],
		}
		tempList = []
		for key in scan_report_jsonres["scan_results"]["scan_details"].keys():
			tempDict = {
				"threat_found" : scan_report_jsonres["scan_results"]["scan_details"][key]["threat_found"],
				"scan_result" : scan_report_jsonres["scan_results"]["scan_details"][key]["scan_result_i"],
				"def_time" : scan_report_jsonres["scan_results"]["scan_details"][key]["def_time"]
			}	
			tempList.append({key : tempDict})
		result["scan_results"] = tempList
		return result
	else:   #Its a re-scan, the report is already available in cache, return the response acquired in previous step.
		#Parse the response.
		result = {
			"report_available_in_cache" : "yes",
			"filename" : hash_report_jsonres["file_info"]["display_name"], 
			"overall_status" : hash_report_jsonres["scan_results"]["scan_all_result_a"],
		}
		tempList = []
		for key in hash_report_jsonres["scan_results"]["scan_details"].keys():
			tempDict = {
				"threat_found" : hash_report_jsonres["scan_results"]["scan_details"][key]["threat_found"],
				"scan_result" : hash_report_jsonres["scan_results"]["scan_details"][key]["scan_result_i"],
				"def_time" : hash_report_jsonres["scan_results"]["scan_details"][key]["def_time"]
			}	
			tempList.append({key : tempDict})
		result["scan_results"] = tempList
		return result

#Uncomment the last two lines, if you want to scan the file by simply running this python code.
#Place the file you want to scan, in the same directory where this python file resides.
#Pass the file_name as command line argument. 

#file_name = sys.argv[1]
#print(callScanAPI(file_name))