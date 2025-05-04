# -*- coding: utf-8 -*-

import collections
import sys
import signal
import os
import logging
import json
import time
import ssl
import sys
import slixmpp
from datetime import datetime, timezone
from xml.dom import minidom

def sigint_handler(signal, frame):
    print('Caught Ctrl+C. Exiting.')
    sys.exit(0)

def sigpipe_handler(signal, frame):
    print('Caught PIPE signal, exiting.', file=sys.stderr)
    logging.info('Caught PIPE signal, exiting.')
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGPIPE, sigpipe_handler)

class MUCBot(slixmpp.ClientXMPP):

    """
    A simple Slixmpp bot.
    """

    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("groupchat_message", self.muc_message)

    async def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        await self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
        )

    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        try:
            print('INFO\t message stanza rcvd from nwws-oi saying... ' + msg['body'])
            xmldoc = minidom.parseString(str(msg))
            itemlist = xmldoc.getElementsByTagName('x')
            ttaaii = itemlist[0].attributes['ttaaii'].value.lower()
            cccc = itemlist[0].attributes['cccc'].value.lower()
            awipsid = itemlist[0].attributes['awipsid'].value.lower()
            id = itemlist[0].attributes['id'].value
            content = itemlist[0].firstChild.nodeValue
            if awipsid:
                dayhourmin = datetime.now(timezone.utc).strftime("%d%H%M")
                filename = cccc + '_' + ttaaii + '-' + awipsid + '.' + dayhourmin + '_' + id + '.txt'
                print("DEBUG\t Writing " + filename, file=sys.stderr)
                if not os.path.exists(config['archivedir'] + '/' + cccc):
                    os.makedirs(config['archivedir'] + '/' + cccc)
                # Remove every other line
                lines = content.splitlines()
                pathtofile = config['archivedir'] + '/' + cccc + '/' + filename
                f = open(pathtofile, 'w')
                count = 0
                for line in lines:
                    if count == 0 and line == '':
                        continue
                    if count % 2 == 0:
                        f.write(line + "\n")
                    count += 1
                f.close()
                # Run a command using the file as the parameter (if pan_run is defined in the config file)
                if 'pan_run' in config:
                    try:
                        os.system(config['pan_run']+' '+pathtofile+' >/dev/null')
                    except OSError as e:
                        print("ERROR\t Execution failed: " + e, file=sys.stderr)
        except Exception as e:
            print("ERROR\t Caught " + str(type(e)) + " exception:")
            print(e)

if __name__ == '__main__':
    # Check for command line arguments
    if len(sys.argv) == 1:
        print('Usage: '+sys.argv[0]+' /path/to/config')
        sys.exit(1)

    if sys.version_info.major == 3 and sys.version_info.minor >= 10:
        from collections.abc import MutableSet
        collections.MutableSet = collections.abc.MutableSet
    else:
        from collections import MutableSet

    # Parse JSON config
    config = json.load(open('config.json'))

    # Create archive directory if it does not exist
    if not os.path.exists(config['archivedir']):
        os.makedirs(config['archivedir'])

    # Start endless loop
    while True:
        # Setup the MUCBot and register plugins. Note that while plugins may
        # have interdependencies, the order in which you register them does
        # not matter.
        xmpp = MUCBot(
            config['username'] + '@' + config['server'],                # JID
            config['password'],                                         # Password
            'nwws@conference.' + config['server'],                      # Chat Room
            config['resource']                                          # Resource/Nickname
        )
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0045') # Multi-User Chat
        xmpp.register_plugin('xep_0199') # XMPP Ping

        # Connect to the XMPP server and start processing XMPP stanzas. If ConnectionResetError is encountered,
        # catch the exception and reconnect to server
        try:
            print("INFO\t Connecting to XMPP server..")
            xmpp.connect()

            print("INFO\t Connected to XMPP server, starting to process incoming products.")
            xmpp.process()

        except ConnectionResetError:
            print("ERROR\t Caught ConnectionResetError exception, restarting..")
        except Exception as e:
            print("ERROR\t Caught " + str(type(e)) + ' exception:')
            print(e)
            print("ERROR\t Restarting..")

        print("INFO\t Sleeping for 5 seconds...")
        time.sleep(5)
