# -*- coding: utf-8 -*-
import detector
import euclid
import matplotlib.pyplot as plt
import cv2
from  datetime import datetime
import os
import gcloud
from gcloud import storage
os.environ['KMP_DUPLICATE_LIB_OK']='True'
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket_name = "output_social_dist"
    source_file_name = "/home/devagastya0/bcor/saved/"
    destination_blob_name = "frame"+str(datetime.now())

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    
def main():
    
    obj = detector.detectron()
    obj.streaming_live()
    #call(['mv','gs://input_social_dist/unprocessed/sample.mp4','gs://input_social_dist/processed/sample_processed.mp4'])

    
    
def load_saved():
    for root, dirs, files in os.walk('gs://input_social_dist/unprocessed/'):
        for file in files:
            img = cv2.imread(os.path.join(root,file))
            plt.figure(figsize=[20,15])
            plt.imshow(img)
            plt.show()
            
if __name__=='__main__':
    main()
    #load_saved()
