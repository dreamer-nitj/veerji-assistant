#!/usr/bin/env python

import Tac
import shlex

defaultUser = 'sonu'
actionToCmdMap = { 'mut' : 'a4 mut status -u %s -c 2 -a',
                 'dir' : 'a dir %s' }

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
   out[ 'speech' ] = speech

   print out
   return out
