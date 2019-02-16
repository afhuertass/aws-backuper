import boto3
import time, threading 
import os
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-credfile" , help = "Credentials File " , type = str , required = True)
parser.add_argument( "-folder" , help ="local folder to upload"  , type = str , required = True)
parser.add_argument( "-bucket" , help = "AWS bucket" , type = str  , required = True)
parser.add_argument("-time" , help ="delta time in minutes for updates" , type = int , required = True)
parser.add_argument("-versioning" , help ="Enables versioning for the bucket" , type = bool )

#dfolder = "./data"
#bucket_name = "aws-uh-bckup"
WAIT_SECONDS = 60 # execute each 5 minutes 

def upload_file( file_path , bucket = None ):

	
	key = file_path.split("/")[-1]
	print(" Uploading file:" , file_path )
	bucket.upload_file( file_path, key )
	print("Up!")
	return

def list_files(path):

    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append( file )
    return files 

def backup(folder  , bucket ):



	files = list_files( folder )
	print( files )
	for file in files:
		print(file)
		upload_file(  folder+"/"+file , bucket  )

	#threading.Timer( WAIT_SECONDS , backup(folder , bucket) ).start()
def enable_versioning( s3 , bucket_name ):
	# Enable versioning for the bucket
    bkt_versioning = s3.BucketVersioning(bucket_name)
    bkt_versioning.enable()
    print(bkt_versioning.status)

def parse_creds( cred ):

	data = []
	f = open(cred)
	for line in f:
		data.append( line.rstrip('\n') )
	f.close()
	tokens = dict()
	tokens["access_key"] = data[0]
	tokens["secret_key"] = data[1]
	tokens["session_token"] =data[2]
	
	return tokens 

def s3_from_file( path_cred ):

	tokens = parse_creds( path_cred )
	print( tokens )
	s3 = boto3.resource(
		"s3" , 
		aws_access_key_id = tokens["access_key"] , 
		aws_secret_access_key = tokens["secret_key"] , 
		aws_session_token = tokens["session_token"]
	 )

	return s3


if __name__ == "__main__":


	args = parser.parse_args()

	varsdict = vars( args )
	#print( vars(args) )
	s3 = s3_from_file( varsdict["credfile"])
	bucket = s3.Bucket( varsdict["bucket"] )
	seconds = varsdict["time"]*WAIT_SECONDS

	ticker = threading.Event()

	if varsdict["versioning"]:
		enable_versioning(s3 , varsdict["bucket"] )
		

	while not ticker.wait( seconds ):
		print(" Running backup on bucket {}".format( varsdict["bucket"]) )
		backup( varsdict["folder"] , bucket )
