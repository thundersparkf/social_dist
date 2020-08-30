# -*- coding: utf-8 -*-

import gcloud
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os

class Cloud:
    def __init__(self):
        credentials_dict = {
                            'type': 'service_account',
                            'client_id': '',
                            'client_email': '',
                            'private_key_id': "",
                            'private_key': ""
        }
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict)       
        self.storage_client = storage.Client(credentials= credentials, project='social-distancing-demo')
  
         
    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        
        
    
        
    
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
    
        print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )
        
    def upload_blob(self, bucket_name, destination_blob_name, source_file_name):
        
    
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
    
        print(
            "Blob {} uploaded to {}.".format(
                destination_blob_name, source_file_name
            )
        )
    def delete_blob(self, bucket_name,  file_name):
        bucket = self.storage_client.bucket(bucket_name)
        bucket.delete_blob(file_name)
        
    def list_files(self, bucketName, bucketFolder):
        bucket = self.storage_client.bucket(bucketName)
        files = bucket.list_blobs(prefix=bucketFolder)
        fileList = [file.name for file in files if '.' in file.name]
        return fileList    
        
        
