#!/usr/bin/env python

import Tac
import shlex
import os
import random

defaultUser = 'sonu'
actionToCmdMap = { 'mut' : 'a4 mut status -u %s -c 2 -a',
                   'dir' : 'a dir %s' }

intro_speeches = [
    "SatSriAkal! I am Veer Ji also known as Big Brother. And I can help in finding project information",
    "Namaskara! I am Veer Ji also known as Big Brother. Let me know if you need user information",
    "Hola! I am Veer Ji The Big Brother! Ask me no questions, I will tell you no lies"
    ]

def runUserCmd( action, user=None ):
   print "action ", action, " user ", user

   global defaultUser
   if user:
      defaultUser = user

   speech = 'I did not hear it right, can you repeat.'
   out = {}
   if 'mut' in action:
      cmd = shlex.split( actionToCmdMap[ 'mut' ] % defaultUser )
      lines = Tac.run( cmd, stdout=Tac.CAPTURE )

      # convert to json
      lines = lines.split( '\n' )
      for line in lines[ 2 : -1 ]:
         if len( line.split() ) > 4:
            out[ line.split()[ 1 ] ] = ' '.join( line.split()[ 3: ] )

      speech = "%s " % defaultUser
      for proj in out:
         speech += "project %s is %s" % ( proj, out[ proj ] )
      else:
         speech += ' user does not exist. Please try again.'

   elif 'dir' in action:
      cmd = shlex.split( actionToCmdMap[ 'dir' ] % defaultUser )
      lines = Tac.run( cmd, stdout=Tac.CAPTURE )

      if len( lines ) > 100:
         # convert to json format
         out = lines.replace( ":", "':'" ).replace( "\n", "','" ).replace( " ", "" )
         out = eval( "{'" + out[ : -2 ] + "}" )

         # add a readable speech to speak
         speech = '%s is a %s working in %s. You can call %s at %s'
         speech = speech % ( out[ 'displayName' ], out[ 'st' ],
                             out[ 'postalAddress' ], out[ 'displayName' ],
                             out[ 'mobile' ] )
      else:
         speech = "User %s does not exist. Please try again." % defaultUser
   elif 'cv' in action.lower():
      speech = ''
      output = os.popen( "echo -e 'su cvp\n cvpi status all' |a4 ssh root@cvp60" ).read()
      print output
      if 'FAIL' in output:
         speech += "Few services are in failed state."
      if 'NOT RUNNING' in output:
         speech += 'Few services are not running.'
      if speech == '':
         speech += 'All services are healthy and running.'
      else:
         speech += 'Rest of the services are running.'
   elif 'intro' in action:
      low = 0
      high = len( intro_speeches )
      rand_num = random.uniform(low, high)
      speech = intro_speeches[int( rand_num )]
   elif 'capabilities' in action:
      speech = "Here is the list of mundane tasks that I can do. Check user information, Get project information, Check cvp services status and I can learn more."
   out[ 'speech' ] = speech

   print out
   return out
