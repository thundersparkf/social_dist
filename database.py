#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:26:02 2020

@author: dev
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd
import configparser
from configparser import ConfigParser

class DataBase:
    def __init__(self, host='', database='sys', user='root', password='Agastya2001#'):
        db_config = ConfigParser()
        db_config.read('config.ini')
        
        self.host=str(db_config.get('database', 'host'))
        self.database=str(db_config.get('database', 'database'))
        self.user=str(db_config.get('database', 'user'))
        self.password=str(db_config.get('database', 'password'))
        
        
    def connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(host=self.host,
                                                 database=self.database,
                                                 user=self.user,
                                                 password=self.password)
            
        except Error as error:
            print("Failed to connect: {}".format(error))
            
        finally:
            return connection
            

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
            connection = self.connect()
            mySql_insert_query = """INSERT INTO bcm_social_distance_data (frame_id, count, video_file_name, created_on) VALUES (%s,%s ,%s,%s) """
            records_to_insert = df
            cursor = connection.cursor()
            cursor.executemany(mySql_insert_query,records_to_insert)
            connection.commit()
            
        except Error as e:
            print('Error:\n{}'.format(e))
            
        finally:
            if connection is not None and connection.is_connected():
                connection.close()

