# -*- coding: utf-8 -*-

import gcloud
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os

class Cloud:
    def __init__(self):
        credentials_dict = {
                            'type': 'service_account',
                            'client_id': '117054123733093849678',
                            'client_email': 'social-distancing-app-service@social-distancing-demo.iam.gserviceaccount.com',
                            'private_key_id': "484cfe6c39baf3681b6e81d223760207f87ec032",
                            'private_key': "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDRzzkGU8l1NBSL\nF1y3RWNbHNWowQoHbAsM2InOycT6phAKwADpFduGTfBsW+yP0Cbqu+C3v6TZptYI\n4SUsh1y/x9tGOlOHYGHH0+KOfzGRMLuCYsUUNsIEepOK/GvOalNGRUfqjmwZuEfs\n9PijxNPATrjj00Qqb/+RIrr1GpDu/qeKEj/CmIOeYkEtK4qcTH+hIXdvaFwYDYtt\n8vGLfOMHGzu7Lc3E3/G/H/mqcSDUfcD9WSRs5YIcu55oZFN24HV1AZBdiLqWndG2\njee4LRBn5jkFor1MpfmcQDk+YXQxTx+CbSA4SYWjJrKn5UnwbHp4oLt95rcZRe8o\ntmz18oXRAgMBAAECggEAAky21PaWzwhlb+ovTk7zZNdEZuzJaFrAeuvmBB86tSic\nJRIFBd5YdqNkuZCptMsqR15h0IHIPnPRWsLk/mpJaPdkKY6QGybCS5zAmfaTm4Ig\n5q/1ywqX8SagIWDc6aP0CmF4r/3O+i/b50v+wa9xnA+rf8vGrn8Qb7h6u3RcFv0s\nebXGbWsqWRNb82UC+UG6DWKK2Z8hK5dRI4AlUAQWeHCCQstBbF3H4rh57dQfZnM3\nsAdHb5R2F9NFAzFAp6RE0/ICga3M3OC32rIfGZWZSVgz6Ai1H+NNc5HaDJmAwqVX\ny0gzlh97PFWa+AuqPInxlP3fAm3MIN5qz/hJVfsYcQKBgQD40QfCf+SzvhtIc7xH\n9LKycrEzQIukekQGb9ihd0efSBIGSq5KQCGuPJUjOSlV4OxDPLpewbb/GJK69fX+\nxIbgUe0dwdhQnHq8MvqpqGuqpAcuV1gTLq408bPQUkgCbZUBQXmRkaNfxPw30RfD\n8lhgo+7AyQ4Z+dVqAttm8c45TQKBgQDX3eV+2sjNiHlzDPW44JwRNdRTVIbnWiOK\n4OWilTGlcbVygpu1i+q4sv/5YL/uJdXeAZy0u0Flz0lCFF7xL3d4UAqqE64VJ4v0\nlFVsfu9MPqXucUAneDetTzT+rcYKt7ErsTZ8H1GtPUHkkibf2LaRPcjn8uzY/rIW\nxQDtr+HclQKBgQDpOVXitGq1KH7+XK2hbPaLWgJLHjdGhux4dCJExz+1R6LNjvbr\n1k07usG4cH4UZ25OX//5je5wEqKG6MIaejBK18BA4lBWzzYkbkyS9rFlE7c/ctO1\nt03Hhr+bh2TEEd9Xe/3tuuu+ezBHSZDTNLgubbr/rfWv14R5iBAL4KADCQKBgART\n/J/4fwIv9E9sORkF19s4exNYpIPK+N919uS1nRM2Hm83UyvmrEQbwqobWH3L4Gfd\nHGk7P+psp4ldozGuw/RzlmMmldzyuAmlV7kfKmka8HTBbIneDS+6YNOiZFAesryv\nhuoiLp8MlV+h1omybKao2HheFIWdRbDTLluVpS+pAoGBAJNiyju8E1gbLtguWCsu\nEmSOC2f1iFcUtT5RcqLFD59RHu0QEKiBj1o7ktGcKVQWc/h4pqqtg7iX4oVAdCQU\n9/31XBZmlAsr9M4dNeueKFJCbDvWt+qBnOUbLzxu0c5EBGWpaFN+TQVnNHeSNx/P\nGpUJ3RH0U9CqgAr7hndKAsLf\n-----END PRIVATE KEY-----\n"
                            }
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict)       
        self.storage_client = storage.Client(credentials= credentials, project='social-distancing-demo')
  
         
    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        
        #bucket_name = "input_social_dist"
        #source_blob_name = "unprocessed/sample.mp4"
        #destination_file_name = "/Users/dev/Downloads/inp1.mp4"
    
        
    
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
            "Blob {} downloaded to {}.".format(
                destination_blob_name, source_file_name
            )
        )
    def delete_blob(self, bucket_name, blob_name, file_name):
        bucket = self.storage_client.bucket(bucket_name)
        bucket.delete_blob('unprocessed/'+file_name)