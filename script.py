#!/usr/bin/python

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import json


__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__path__ = __addon__.getAddonInfo('path')
__LS__ = __addon__.getLocalizedString
__icon__ = xbmc.translatePath(os.path.join(__path__, 'icon.png'))

WINDOW                  = xbmcgui.Window( 10000 )



################################################
# Switch to channel
################################################
def writeLog(message, level=xbmc.LOGNOTICE):
        try:
            xbmc.log('[%s %s]: %s' % ( __addonID__,__version__,message.encode('utf-8')), level)
        except Exception:
            xbmc.log('[%s %s]: Fatal: Message could not displayed' % (__addonID__,__version__), xbmc.LOGERROR)


################################################
# Switch to channel
################################################
def switchToChannel(pvrid):
    writeLog('Switch to channel id %s' % (pvrid), level=xbmc.LOGDEBUG)
    query = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Player.Open",
        "params": {"item": {"channelid": int(pvrid)}}
        }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    if 'result' in res and res['result'] == 'OK':
        return True
    else:
        writeLog('Couldn\'t switch to channel id %s' % (pvrid), level=xbmc.LOGDEBUG)
    return False



################################################
#                   M A I N
################################################
RezapLast=WINDOW.getProperty('ReZap.Last')
if RezapLast == '':
  writeLog('Not possible to rezap, no data available', level=xbmc.LOGNOTICE)
else:
  writeLog('Switch to channel id %s' % (str(RezapLast)), level=xbmc.LOGNOTICE)
  switchToChannel(RezapLast)


