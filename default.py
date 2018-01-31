#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2017 TDOe
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#    This script is based on script.randomitems & script.wacthlist
#    Thanks to their original authors

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import subprocess
import json

__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__path__ = __addon__.getAddonInfo('path')
__LS__ = __addon__.getLocalizedString
__icon__ = xbmc.translatePath(os.path.join(__path__, 'icon.png'))

WINDOW = xbmcgui.Window(10000)

#def log(txt):
#    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
#    xbmc.log(msg=message, level=xbmc.LOGDEBUG)



def writeLog(message, level=xbmc.LOGNOTICE):
        try:
            xbmc.log('[%s %s]: %s' % (__addonID__, __version__,  message.encode('utf-8')), level)
        except Exception:
            xbmc.log('[%s %s]: %s' % (__addonID__, __version__,  'Fatal: Message could not displayed'), xbmc.LOGERROR)




################################################
# Gather current player ID
################################################
def currentplayer():
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetActivePlayers",
            "id": 1
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    playerid = res['result'][0]['playerid']
    return playerid


################################################
# Gather current player Type (1->Video,2->Audio)
################################################
def get_player_type(playerid):
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetItem",
            "id": 1,
            "params": { "playerid" : playerid, "properties":["title", "album", "artist", "season", "episode", "showtitle", "tvshowid", "description"]}
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    result = res['result']['item']['type']
    return result

################################################
# Gather what plays at the moment
################################################
def get_player_channel_id(playerid):
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetItem",
            "id": 1,
            "params": { "playerid" : playerid, "properties":["title", "album", "artist", "season", "episode", "showtitle", "tvshowid", "description"]}
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    return res['result']['item']


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





class Main:
  def __init__(self):
    self._init_vars()
    self._init_property()
    self._daemon()

  def _init_vars(self):
    self.Player = MyPlayer()
    self.Monitor = MyMonitor(update_settings = self._init_property, player_status = self._player_status)

  def _init_property(self):
    writeLog('Reading properties',level=xbmc.LOGDEBUG)

  def _player_status(self):
    return self.Player.playing_status()

  def _daemon(self):
    while (not xbmc.abortRequested):
      # Do nothing
#      global script_idle
#      if script_idle:
#        if xbmc.getGlobalIdleTime() > 60 * __addon__.getSetting("idle_time"):
#          log('XBMC is idle')
#          log('Going to execute script = "' + script_idle + '"')
#          try:
#              subprocess.call(script_idle)
#          except:
#              log('ERROR executing script when xbmc goes idle')
      xbmc.sleep(10000)
    writeLog('abort requested',level=xbmc.LOGDEBUG)


class MyMonitor(xbmc.Monitor):
  def __init__(self, *args, **kwargs):
    xbmc.Monitor.__init__(self)
    self.get_player_status = kwargs['player_status']
    self.update_settings = kwargs['update_settings']

class MyPlayer(xbmc.Player):
  def __init__(self):
    xbmc.Player.__init__(self)
#    self.substrings = [ '-trailer', 'http://' ]

  def playing_status(self):
    if self.isPlaying():
      return 'status=playing' + ';' + self.playing_type()
    else:
      return 'status=stopped'

  def onPlayBackStarted(self):
    CurrentPlayer=currentplayer()
    PlayerType=get_player_type(CurrentPlayer)
    if PlayerType == "channel":
      ChannelID=get_player_channel_id(CurrentPlayer)
      message="Rezapping in Progress Player: %s Type: %s ChannelID: %s" % (CurrentPlayer,PlayerType,ChannelID['id'])
      RezapCurrent=WINDOW.getProperty('ReZap.Current')
      RezapLast=WINDOW.getProperty('ReZap.Last.1')
      RezapLast2=WINDOW.getProperty('ReZap.Last.2')
      RezapLast3=WINDOW.getProperty('ReZap.Last.3')
      RezapLast4=WINDOW.getProperty('ReZap.Last.4')
      RezapLast5=WINDOW.getProperty('ReZap.Last.5')
      WINDOW.setProperty('ReZap.Last.1', str(RezapCurrent))
      WINDOW.setProperty('ReZap.Current',str(ChannelID['id']))
      WINDOW.setProperty('ReZap.Last.2', str(RezapLast))
      WINDOW.setProperty('ReZap.Last.3', str(RezapLast2))
      WINDOW.setProperty('ReZap.Last.4', str(RezapLast3))
      WINDOW.setProperty('ReZap.Last.5', str(RezapLast4))
      writeLog(message, level=xbmc.LOGNOTICE)

if (__name__ == "__main__"):
    writeLog("Startet in background",level=xbmc.LOGNOTICE)
    Main()
    del MyPlayer
    del MyMonitor
    del Main
    writeLog("Service shutdown",level=xbmc.LOGNOTICE)
