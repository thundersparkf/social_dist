#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:26:02 2020

@author: dev
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd

class DataBase:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host='35.244.12.188',
                                                     database='cnw_bcm_uat',
                                                     user='chuttiroot',
                                                     password='Root@chutti!@#')
            
        except Error as error:
            print("Failed to connect: {}".format(error))
            

    def store_into_table(self, df):
        '''
        

        Parameters
        ----------
        df : pandas dataframe
            Dataframe with the frame_id .

        Returns
        -------
        None.

        '''
        try:
    
            mySql_insert_query = """INSERT INTO bcm_social_distance_data (bcm_social_distance_data_id, frame_id, count, video_file_name) VALUES (%s, %s,%s ,%s) """
            records_to_insert = df
            print(mySql_insert_query)
            print(records_to_insert)
            cursor = self.connection.cursor()
            cursor.executemany(mySql_insert_query,records_to_insert)
            #cursor.executemany(mySql_insert_query, records_to_insert)
            self.connection.commit()
            print(cursor.rowcount, " Records inserted successfully into Laptop table")
            self.connection.close()
        except Error as e:
            print('Error:\n{}'.format(e))
            self.connection.close()

