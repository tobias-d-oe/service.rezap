#!/usr/bin/python

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import json
import urllib

__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonDir__            = __addon__.getAddonInfo("path")

__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__path__ = __addon__.getAddonInfo('path')
__LS__ = __addon__.getLocalizedString
__icon__ = xbmc.translatePath(os.path.join(__path__, 'icon.png'))

WINDOW                  = xbmcgui.Window( 10000 )




def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict



def pvrchannelid2channelname(channelid):
    query = {
            "jsonrpc": "2.0",
            "method": "PVR.GetChannels",
            "params": {"channelgroupid": "alltv"},
            "id": 1
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    if 'result' in res and 'channels' in res['result']:
        res = res['result'].get('channels')
        for channels in res:
            if channels['channelid'] == channelid:
                return channels['label']
    return False

# get pvr channel logo url

def pvrchannelid2logo(channelid):
    query = {
            "jsonrpc": "2.0",
            "method": "PVR.GetChannelDetails",
            "params": {"channelid": channelid, "properties": ["thumbnail"]},
            "id": 1
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    if 'result' in res and 'channeldetails' in res['result'] and 'thumbnail' in res['result']['channeldetails']:
        return res['result']['channeldetails']['thumbnail']
    else:
        return False


################################################
# Logging Function
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

def item_create(num):
  channelNum = WINDOW.getProperty('ReZap.Last.%s' % (str(num)))
  url = 'XBMC.RunAddon(service.rezap,"?switch=%s" % (str(num)))'
  li = xbmcgui.ListItem(str(num))
  Label2=str(pvrchannelid2channelname(int(channelNum)))
  Icon=str(pvrchannelid2logo(int(channelNum)))
  writeLog('DEBUG in Item: %s %s' % (Label2,Icon), level=xbmc.LOGNOTICE)
  li.setLabel2(Label2)
  li.setIconImage(Icon)
  li.setProperty("PVRID",str(channelNum))
  return li


################################################
#                   M A I N
################################################



if len(sys.argv)>=3:
    addon_handle = int(sys.argv[1])
    params = parameters_string_to_dict(sys.argv[2])
    methode = urllib.unquote_plus(params.get('methode', ''))
    num = urllib.unquote_plus(params.get('num', ''))
elif len(sys.argv)>1:
    params = parameters_string_to_dict(sys.argv[1])
    methode = urllib.unquote_plus(params.get('methode', ''))
    num = urllib.unquote_plus(params.get('num', ''))
else:
    methode = None




if methode=='zap':
  switchToChannel(num)        
elif methode=='get_container':

  for x in range(1, 6):
    writeLog('DEBUG in for loop %s' % (str(x)), level=xbmc.LOGNOTICE)
    ZapVal=WINDOW.getProperty('ReZap.Last.%s' % (x))
    writeLog('DEBUG ZapVal %s' % (str(ZapVal)), level=xbmc.LOGNOTICE)
    if str(WINDOW.getProperty('ReZap.Last.%s' % (x))) != "":   
      writeLog('DEBUG in if %s' % (str(ZapVal)), level=xbmc.LOGNOTICE)
      li=item_create(x)
      url = 'XBMC.RunAddon(service.rezap,"?switch=%s" % (str(x)))'
      try:
          xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
      except:
          pass    
  xbmcplugin.endOfDirectory(addon_handle)

else:
  RezapLast=WINDOW.getProperty('ReZap.Last.1')
  if RezapLast != '':
    DETAILWIN = xbmcgui.WindowXMLDialog('rezap-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()
  

