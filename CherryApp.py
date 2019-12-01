# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 18:11:25 2019

@author: pandu ranga
"""
import os

import redis
#import pandas as pd
import numpy as np
import cherrypy


class Equity(object):
    
    baseHtml = """<html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
          <body>
            <div align='center'>  
                <div id='title'>
                  <h2 align='center'>Equity Search</h2>
                </div>  
                <div id='form'>  
                <form method="post" action="getCompanyDetails">
                  Company Name: <input type="text" value="" name="name" 
                                  placeholder="Enter company name" required/>
                  &emsp;                
                  <input type="submit" value='Get me now!'/>
                </form>
                
                <p>or</p>
                
                <form method="get" action="getTopTenEquities">
                    Category:
                    <select name="category">
                      <option value="OPEN">Open</option>
                      <option value="CLOSE">Close</option>
                      <option value="HIGH" selected>High</option>
                      <option value="LOW">Low</option>
                    </select>   &emsp;
                    
                    Top:
                    <select name="top">
                      <option value=10 selected>10</option>
                      <option value=20>20</option>
                      <option value=50>50</option>
                      <option value=100>100</option>
                    </select>   &emsp;
                    
                    <input type="submit" value='Get Top 10 Equities'/>
                </form>
                </div>
            </div>    
          """
    
    #EDIT THE URL AND PORT
    host = u'localhost'
    port = 6379
    
    def makeRedisConn(self):
        conn = redis.Redis(host = self.host, port = self.port)
        return conn
    
    
    @cherrypy.expose
    def index(self):
        return self.baseHtml+"</body></html>"

    @cherrypy.expose
    def getTopTenEquities(self,category='HIGH',top=10):
        
        try:
            result = self.baseHtml+"<br/>"
            
            conn = self.makeRedisConn()
            res = conn.keys()
            
            highVals = []
            topTen = []
            count = 0
            
            for eachKey in res:
                buff = float(conn.hget(eachKey,category).decode("utf-8"))
                highVals.append(buff)
            
            highVals = np.array(highVals)
            highVals = np.argsort(highVals)[::-1][:int(top)]
            
            topTen = [res[i] for i in highVals]
            
            result += """<div align='center' id='equityTable'>
                         <table>
                         <col width="80">
                          <tr>
                            <th>S.No.</th>  
                            <th>CompanyName</th>
                            <th>CompanyCode</th>
                            <th>Open</th>
                            <th>Close</th>
                            <th>High</th>
                            <th>Low</th>
                          </tr>"""
                          
            for key in topTen:
                count += 1
                buff = conn.hgetall(key)
                
                result += '<tr>'
                result += '<td>'+ str(count) + '</td>'
                result += '<td>'+ key.decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'SC_CODE'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'OPEN'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'CLOSE'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'HIGH'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'LOW'].decode("utf-8") +'</td>'
                result += '</tr>'
            
            result += '</table>'
            result += '<p><b>Number of records found :'+ str(count) +'</b></p>'
            result += '</div>'
            result += '</body>'
            result += '</html>'              
            
            return result
        
        except:
            return "Error Occured!!"
            
        
        
        
    
    @cherrypy.expose
    def getCompanyDetails(self,name=''):
        
        try:
            result = self.baseHtml+"<br/>"
            
            result += """<div align='center' id='equityTable'>
                     <table>
                     <col width="80">
                      <tr>
                        <th>S.No.</th>  
                        <th>CompanyName</th>
                        <th>CompanyCode</th>
                        <th>Open</th>
                        <th>Close</th>
                        <th>High</th>
                        <th>Low</th>
                      </tr>"""    
            
            conn = self.makeRedisConn()
           
            queryStr = ''
            count = 0
            queryStr = '*'+name.upper()+'*'
            
            for key in conn.scan_iter(queryStr):
                count += 1
                buff = conn.hgetall(key)
                
                result += '<tr>'
                result += '<td>'+ str(count) + '</td>'
                result += '<td>'+ key.decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'SC_CODE'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'OPEN'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'CLOSE'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'HIGH'].decode("utf-8") +'</td>'
                result += '<td>'+ buff[b'LOW'].decode("utf-8") +'</td>'
                result += '</tr>'
            
            result += '</table>'
            result += '<p><b>Number of records found :'+ str(count) +'</b></p>'
            result += '</div>'
            result += '</body>'
            result += '</html>'
            
            return result                
        except:
            return "Error Occured!!"  
        
        

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
      }  
    cherrypy.quickstart(Equity(), '/', conf)