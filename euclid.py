# -*- coding: utf-8 -*-
import numpy as np
import scipy
from scipy.spatial import distance
import subprocess
import cv2
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
class Dist:
    
    def __init__(self):
        self.count_data = []
        #self.cloud = Cloud.Cloud()
        self.date = str(datetime.now())
    
    def persons_find(self,outputs):
        '''
        

        Parameters
        ----------
        outputs : detectron2 outputs object 
                Output instance of the detectron2 predictor.

        Returns
        -------
        num : int
            Count of people inside the frane.
        person : list
            List of persons and coordinates.

        '''
        
        classes=outputs['instances'].pred_classes.cpu().numpy()
        ind = np.where(classes==0)[0]
        bbox=outputs['instances'].pred_boxes.tensor.cpu().numpy()
        person = bbox[ind]
        num = len(person)
        return num, person  
    
    
    def mid_point(self,img,person,idx):
        '''
        

        Parameters
        ----------
        img : uint8 
            Frames in the video.
        person : list
            List of persons and coordinates.
        idx : int, 
            id of the person object. 

        Returns
        -------
        mid : tuple of int
            midpoint coordinates for each person in frame.

        '''
        
        x1,y1,x2,y2 = person[idx]
        
        #compute bottom center of bbox
        x_mid = int((x1+x2)/2)
        y_mid = int(y2)
        mid   = (x_mid,y_mid)
        
        _ = cv2.circle(img, mid, 5, (255, 0, 0), -1)
        cv2.putText(img, str(idx), mid, cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)
        
        return mid
    def compute_distance(self,outputs, img):
        '''
        

        Parameters
        ----------
        outputs : detectron2 outputs object 
                Output instance of the detectron2 predictor.
        img : uint8
            Frames from the video.

        Returns
        -------
        dist : list
            Distance between each person within the threshold.

        '''
        
        self.num, self.person = self.persons_find( outputs)
        midpoints = [self.mid_point(img,self.person,i) for i in range(len(self.person))]
        dist = np.zeros((self.num,self.num))
        for i in range(self.num):
            for j in range(i+1,self.num):
                if i!=j:
                    dst = distance.euclidean(midpoints[i], midpoints[j])
                    dist[i][j]=dst
        return dist
    
    def find_closest(self, outputs, img,thresh=150):
        '''
        

        Parameters
        ----------
        outputs : detectron2 outputs object 
            Output instance of the detectron2 predictor.
        img : uint8
            Frames from the video.
        thresh : int, 
            value for minimum threshold distance between two people. The default is 150.

        Returns
        -------
        p1 : int
            Primary Person id.
        p2 : int
            Secondary Person id.
        d : float
            Distance between persons in arguments.

        '''
        
      
        p1, p2, d = [],[],[]
        dist = self.compute_distance(outputs, img)
        for i in range(self.num):
            for j in range(i,self.num):
                if( (i!=j) & (dist[i][j]<=thresh)):
                    p1.append(i)
                    p2.append(j)
                    d.append(dist[i][j])
        
        return p1,p2,d
     
    def change_2_red(self,img, p1,p2, count, directory):
        '''
        

        Parameters
        ----------
        img : uint8
            Frames from the video.
        p1 : int
            Primary Person id.
        p2 : int
            Secondary Person id.
        sum : int
            Count of frames saved.

        Returns
        -------
        None.

        '''
        
        risky = np.unique(p1+p2)
        for i in risky:
            x1,y1,x2,y2 = self.person[i]
            _ = cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2) 
            
            cv2.imwrite('/var/www/html/output_social_dist/'+directory+'/frame'+str(count)+'.png', img)
            
        dict1 = {'Frame_name':'/'+directory+'/frame'+str(count)+'.png','count':len(risky)}
        self.count_data.append(dict1)
