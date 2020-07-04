 # -*- coding: utf-8 -*-
import torch, torchvision
import detectron2
from detectron2.utils.logger import setup_logger
import cv2
import pandas as pd
import os
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
import euclid
import database
import Cloud
import datetime
import pytz
from gcloud import storage
from datetime import datetime
import subprocess 
from subprocess import run
count = 0
class detectron:
    
    def __init__(self):
        
        self.comp = 'cuda:0' if (torch.cuda.is_available()) else 'cpu'
        print(self.comp)
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE=self.comp
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_C4_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9  # set threshold for this model
        
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_C4_3x.yaml")
        self.predictor = DefaultPredictor(self.cfg)
        self.euc = euclid.Dist()
        self.db = database.DataBase()
        #self.cloud =Cloud.Cloud()
        tz = pytz.timezone('Asia/Kolkata')
        tz = datetime.now(tz)
        self.date = str(tz.strftime('%d-%m-%y_%H:%M'))
        
    def streaming_live(self):
        '''
        Function to read pre_existing file.

        Returns
        -------
        None.

        '''
        
        
        #self.download_blob()
        print("[INFO] starting video file thread...")
        #files = self.cloud.list_files('input_social_dist','unprocessed')
        for root, dirs, files in os.walk('/var/www/html/input_social_dist/unprocessed/'):
            for file in files:
                #self.cloud.download_blob('input_social_dist',file,'./'+file)
                
                self.image_proc(os.path.join(root,file)) 
                run(['bash','/var/www/html/move_files.sh',file])
            
#            self.cloud.upload_blob('input_social_dist','processed/'+file.replace('unprocessed/',""),'./'+file)
#            self.cloud.delete_blob('input_social_dist',file)
#        for root, dirs, files in os.walk('./frames'):
#            for file in files:
#                file_name = os.path.join(root, file)
#                print(file_name)
                #self.cloud.upload_blob('output_social_dist','frames_'+self.date+'/'+file,file_name)    
        #run(['bash','clean_up.sh'])
    def image_proc(self, file):
        '''
        Function to preprocess for computation with Detectron2.

        Parameters
        ----------
        file : A video file.

        Returns
        -------
        None.

        '''
        
        cap = cv2.VideoCapture(file)
        file_name = file.replace('/var/www/html/input_social_dist/unprocessed/','')
        file_name = file_name.replace('.mp4','')
        print('Video founds.')
        FPS=cap.get(cv2.CAP_PROP_FPS)
        print('FPS: ', FPS)
        run(['sudo','mkdir','/var/www/html/output_social_dist/'+file_name+'_frames_'+self.date])
        run(['sudo','chmod','757','/var/www/html/output_social_dist/'+file_name+'_frames_'+self.date])
        while (cap.isOpened()):
            print('Position:', int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
            cap.set(cv2.CAP_PROP_POS_FRAMES, FPS+int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
            ret,frame = cap.read()
            if frame is not None:
                self.load_asap(frame, 'output_social_dist/'+file_name+'_frames_'+self.date)
            else:
                cap.release()
        df = pd.DataFrame(self.euc.count_data)
        df['video_file_name'] = file_name
        df = df.to_records(index=False).tolist()
        self.db.store_into_table(df)
        
#        self.save_count(df, file_name)
        
    def save_count(self, df, file_name):
        '''
        

        Parameters
        ----------
        df : DataFrame storing frame_id and count per each frame.       
       
        file_name : Name of the video file.

        Returns
        -------
        None.

        '''
        
        try:
            df.to_csv('/home/devagastya0/bcor/op/'+file_name+'.csv',index=False)
        except:
            print(file_name + ' file could not be saved.')    
                                
    # def video_to_frame(self):
    #     cap = cv2.VideoCapture('sample.mp4')
    #     cnt=0
    #     FPS=cap.get(cv2.CAP_PROP_FPS)
    #     if (cap.isOpened()== False): 
    #         print("Error opening video stream or file")
    #     global sum
    #     ret,first_frame = cap.read()
    #     print('Frames initialising...')
    #     while(cap.isOpened()):
    #         cap.set(cv2.CAP_PROP_POS_FRAMES, FPS+int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
    #         print('Position:', int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
    #         ret, frame = cap.read()
    #         if ret == True:
    #             start = datetime.now()
    #             sum+=1
    #             self.load_asap(frame)
    #             #cv2.imwrite('frames/'+str(cnt)+'.png', frame)
    #             cnt=cnt+1
    #             end = datetime.now()
    #             print('{}: count, {} time'.format(sum,(end-start)))
    #             if(cnt==37):
    #                 break
    #         else: 
    #             break
    #     print('Frames initialised.')
      
    def load_asap(self, img,directory):
        '''
        Function to process each frame/image on Detectron2.
    
        Function
        Parameters
        ----------
        img : Image/Frame to be processed.

        Returns
        -------
        None.

        '''
        global count  
        count+=1
        outputs = self.predictor(img)
        p1 ,p2, d = self.euc.find_closest(outputs, img)
        if len(p1) != 0:
            self.euc.change_2_red(img, p1, p2,count, directory)
            
    
    
    
