import requests
import time
import sys
import json
import hashlib
api_key = "d6a36be789ebe72209296733ca4d4d06"
#file_name = sys.argv[1]
#print(file_name)

#function to compute hash values of the input file
def getHashValues(file_name):
	hasher = hashlib.md5()
	afile = open("./" + file_name, 'rb')
	buf = afile.read()
	hasher.update(buf)
	file_hash_md5 = hasher.hexdigest().upper() 
	#print(file_hash_md5)

	hasher = hashlib.sha1()
	afile = open("./" + file_name, 'rb')
	buf = afile.read()
	hasher.update(buf)
	file_hash_sha1 = hasher.hexdigest().upper() 
	#print(file_hash_sha1)

	hasher = hashlib.sha256()
	afile = open("./" + file_name, 'rb')
	buf = afile.read()
	hasher.update(buf)
	file_hash_sha256 = hasher.hexdigest().upper() 
	#print(file_hash_sha256)	
	return file_hash_md5, file_hash_sha1, file_hash_sha256

#function to upload file and return the unique data id
def uploadFile(file_name):
	file_upload_url = "https://api.metadefender.com/v2/file"
	file_upload_headers = {"apikey" : api_key}
	file_to_upload = {"file" : (file_name, open("./" + file_name, "rb"))}
	file_upload_response = requests.post(url = file_upload_url, headers = file_upload_headers, files = file_to_upload)
	file_upload_jsonres = file_upload_response.json()
	data_id = file_upload_jsonres['data_id']
	return data_id

#function to get scan report by passing the unique data_id obtained by uploading the file
def getScanReport(data_id):
	scan_report_url = "https://api.metadefender.com/v2/file/" + data_id
	scan_report_headers = {"apikey" : api_key, "file_metadata" : "1"}
	#scan_report_params = {"dataId" : data_id}
	scan_report_response = requests.get(url = scan_report_url, headers = scan_report_headers)
	#check is the progress percent is 100%
	scan_report_jsonres = scan_report_response.json()
	#print("scanning....")
	while(scan_report_jsonres["scan_results"]["progress_percentage"] != 100):
		scan_report_response = requests.get(url = scan_report_url, headers = scan_report_headers)
		scan_report_jsonres = scan_report_response.json()
		#time.sleep(5)
		#print(scan_report_jsonres["scan_results"]["progress_percentage"])
	return scan_report_jsonres	



def callScanAPI(file_name):
	#compute hash values of the file
	file_hash_md5, file_hash_sha1, file_hash_sha256 = getHashValues(file_name)
	#print(file_hash_md5)
	#print(file_hash_sha1)
	#print(file_hash_sha256)

	#retrieve scan reports using a data hash 
	hash_report_url = "https://api.metadefender.com/v2/hash/" + file_hash_sha1
	headers = {"apikey" : api_key, "file_metadata" : "1"}
	hash_report_resp = requests.get(url = hash_report_url, headers = headers)
	hash_report_jsonres = hash_report_resp.json()
	#return (hash_report_jsonres)
	#data_id = hash_report_jsonres[file_hash_sha1]
	'''
	hash_report_url = "https://api.metadefender.com/v2/hash/"
	headers = {"apikey" : api_key, "include_scan_details" : "1"}
	data = {"hash" : [file_hash_md5, file_hash_sha256, file_hash_sha1]}
	hash_report_resp = requests.post(url = hash_report_url, headers = headers, data = json.dumps(data))
	hash_report_jsonresp = hash_report_resp.json()
	data_id = hash_report_jsonresp[0]["data_id"]
	'''
	#print(data_id)

	#check if the response is null or not
	#if data_id == "Not Found":
	if file_hash_sha1 in hash_report_jsonres:
		#response is null, upload the file and perform the scan
		#print("Scan report not available in cache, its a first time scan")
		data_id = uploadFile(file_name)
		#print(data_id)
		scan_report_jsonres = getScanReport(data_id)
		result = {
			"report_available_in_cache" : "no",
			"filename" : scan_report_jsonres["file_info"]["display_name"], 
			"overall_status" : scan_report_jsonres["scan_results"]["scan_all_result_a"],
			#"scan_results" : scan_report_jsonres["scan_results"]
		}
		tempList = []
		for key in scan_report_jsonres["scan_results"]["scan_details"].keys():
			tempDict = {
				"threat_found" : scan_report_jsonres["scan_results"]["scan_details"][key]["threat_found"],
				"scan_result" : scan_report_jsonres["scan_results"]["scan_details"][key]["scan_result_i"],
				"def_time" : scan_report_jsonres["scan_results"]["scan_details"][key]["def_time"]
			}	
			tempList.append({key : tempDict})
			#result[key] = tempDict
		result["scan_results"] = tempList

		#print(scan_report_jsonres)
		return result
		#print("filename: " + file_name)
		'''
		if scan_report_jsonres[0]["total_detected_avs"] == 0:
			print("overall_status: Clean")
		else:
			print("overall_status: Threats Detected")
		print(scan_report_jsonres[0]["scan_details"])
		'''
	else:
		#response is not null, return the result
		#print("Scan report already available in cache")
		#print("filename: " + file_name)
		#print(hash_report_jsonres)
		result = {
			"report_available_in_cache" : "yes",
			"filename" : hash_report_jsonres["file_info"]["display_name"], 
			"overall_status" : hash_report_jsonres["scan_results"]["scan_all_result_a"],
			#"scan_results" : hash_report_jsonres["scan_results"]["scan_details"]
		}
		tempList = []
		for key in hash_report_jsonres["scan_results"]["scan_details"].keys():
			tempDict = {
				"threat_found" : hash_report_jsonres["scan_results"]["scan_details"][key]["threat_found"],
				"scan_result" : hash_report_jsonres["scan_results"]["scan_details"][key]["scan_result_i"],
				"def_time" : hash_report_jsonres["scan_results"]["scan_details"][key]["def_time"]
			}	
			tempList.append({key : tempDict})
			#result[key] = tempDict
		result["scan_results"] = tempList
		#return hash_report_jsonres
		return result
		'''
		if hash_report_jsonres[0]["total_detected_avs"] == 0:
			print("overall_status: Clean")
		else:
			print("overall_status: Threats Detected")
		print(hash_report_jsonres[0]["scan_details"])
		'''
