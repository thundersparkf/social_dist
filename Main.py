#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 20:30:42 2020

@author: dev
"""
import schedule
import time
import detector
import os
from torch.multiprocessing import set_start_method

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def job():
    print('Running...')
    obj = detector.detectron()
    obj.streaming_live()
    
def main():
    try:
        set_start_method('spawn')
    except RuntimeError:
        pass
    print('Initialised')
    schedule.every(3).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__=='__main__':
    main()

