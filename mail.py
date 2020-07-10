#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:48:38 2020

@author: dev
"""


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import configparser
from configparser import ConfigParser

class  Email:
    def __init__(self):
        '''
        Utilising the Sendgrid API to send email notifications.

        Returns
        -------
        None.

        '''
        email_config = ConfigParser()
        email_config.read('./config.ini')
        self.api_token = email_config.get('sendgrid_email','API_token')
        self.email = email_config.get('sendgrid_email','email')
    def message_send(self, num, date_time):
        '''
        

        Parameters
        ----------
        num : int
            Count of the people not following distancing guidelines in a video.
        time : Datetime object
            Time of processing the video files.

        Returns
        -------
        None.

        '''
        date_time = date_time.replace('_',' ')
        date_time = date_time.split()
        time = date_time[1]
        date = date_time[0]
        message = Mail(
        from_email =' noreply@chutti.work',
        to_emails = self.email,
        subject = 'Distancing protocol notification',
        html_content = 'Greetings.<br>We found <strong>'+str(num)+
                     '</strong> instances of social distancing lapses in Sriperumbudur, Chennai plant.<br><strong>Date: '+
                     date+'</strong><br><strong>Time: '+time+'</strong>')
        
        
        try:
            sg = SendGridAPIClient(self.api_token)
            response = sg.send(message)
            print('Message sent successfully.')
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)
        except Exception as e:
            print(e.message)
