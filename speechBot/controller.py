#!/usr/bin/env python
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import json
import flask
import runUserSpeechToTextCmds as backend
from flask import jsonify
from flask import request
from flask import Response
from flask_cors import CORS

app = flask.Flask( __name__ )
CORS(app)
app.config[ "DEBUG" ] = True

actionMap = {
    ( "information", "for" ): "dir",
    ( "info", "for" ): "dir",
    ( "dir", "for" ): "dir",
    ( "project", "status", "for" ): "mut",
    ( "information", "of" ): "dir",
    ( "info", "of" ): "dir",
    ( "dir", "of" ): "dir",
    ( "project", "status", "of" ): "mut",
    ( "cvp", "status", "for" ):"cvp",
}

@app.route( '/api/bot/', methods=[ 'GET' ] )
def home():
   return "<h1>Welcome to Chatbot</h1><p>This site is a prototype API for Chatbot.</p>"

@app.route( '/api/bot/runCmd', methods=[ 'POST' ] )
def runCmd():
   print "runCmd: ", request.json
   if request.method == 'POST' and request.headers[ 'Content-Type' ] == 'application/json':
      cmd = request.json[ "request" ]
      reqActionTokens = cmd.split( ' ' )
      action = ""
      actionKey = ()
      maxMatch = 0

      for key in actionMap:
         tempMatch = 0
         listActionTokens = list( key )
         for actionToken in listActionTokens:
            if actionToken in reqActionTokens:
               tempMatch = tempMatch + 1
         if( tempMatch > maxMatch ):
            action = actionMap[ key ]
            maxMatch = tempMatch
            actionKey = key

      i = 0
      for word in reqActionTokens:
         if word == "for" or word == "of":
            i = i + 1
            break
         i = i + 1

      entityID = ""
      if i < len( reqActionTokens ):
         entityID = reqActionTokens[ i ]

      print "Action is: ", action, " Action tokens are: ", actionKey, " Entity ID is:", entityID

      print "Request command: ", request.json
      # call backend for the response
      output = ""
      if entityID:
         output = backend.runUserCmd( action, entityID )
      else:
         output = backend.runUserCmd( action )
      data = { 'response'  : output, }
      js = json.dumps( data )
      resp = Response( js, status=200, mimetype='application/json' )
#      resp.headers['Access-Control-Allow-Origin'] = '*'
#      resp.header[ 'Access-Control-Allow-Methods'] = '*'
#      resp.header[ 'Access-Control-Allow-Headers' ] = '*'
      return resp
   else:
      message = {
         'status': 500,
         'message': 'Invalid request' + str( request ),
      }
      resp = jsonify( message )
      resp.status_code = 500
#      resp.headers['Access-Control-Allow-Origin'] = '*'
      return resp

#@app.route( '/api/bot/runCmd', methods=[ 'HEAD' ] )
#def allowHead():
#   print "Received header request"
#   resp = Response( "", status=200, mimetype='application/json' )
#   resp.headers['Access-Control-Allow-Origin'] = '*'
#   return resp

app.run( host='0.0.0.0' )
