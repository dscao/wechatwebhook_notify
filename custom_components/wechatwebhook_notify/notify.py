import logging
import time
import requests
import json
import os
import base64
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_MESSAGE,
    ATTR_TITLE,
    ATTR_DATA,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCE, CONF_TOKEN

_LOGGER = logging.getLogger(__name__)
DIVIDER = "———————————"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required("touser"): cv.string,
    vol.Required(CONF_RESOURCE): cv.url,
    vol.Required(CONF_TOKEN): cv.string,
    vol.Optional("isRoom", default = 'false'): cv.boolean,    
    vol.Optional("resource_username", default = ""): cv.string,
    vol.Optional("resource_password", default = ""): cv.string,
})


def get_service(hass, config, discovery_info=None):
    return WeChatNotificationService(
        hass,
        config.get("touser"),
        config.get("isRoom"),
        config.get(CONF_RESOURCE),
        config.get(CONF_TOKEN),
        config.get("resource_username"),
        config.get("resource_password"),
    )


class WeChatNotificationService(BaseNotificationService):
    def __init__(self, hass, touser, isRoom, wechatbaseurl, token, resource_username, resource_password):
        self._touser = touser
        self._isroom = isRoom
        self._wechatbaseurl = wechatbaseurl
        self._token = token

        if resource_username and resource_password:
            self._header = {"Authorization": "Basic {}".format(self.getAuth(resource_username,resource_password)), "Content-Type": "application/json"} 
        else:
            self._header = {"Content-Type": "application/json"}
        
        
    def getAuth(self,uername,password):
        serect = uername + ":"+password
        bs = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
        return bs

    def send_message(self, message="", **kwargs):
        send_url = (
            self._wechatbaseurl + "/webhook/msg?token=" + self._token
        )
        title = kwargs.get(ATTR_TITLE)

        data = kwargs.get(ATTR_DATA) or {}
        msgtype = data.get("type", "text")
        url = data.get("url")

        touser = kwargs.get(ATTR_TARGET) or [self._touser]
        
        isroom = data.get("isroom", self._isroom)

        if msgtype == "text":
            content = ""
            if title is not None:
                content += title+"\r\n"
            content += message
            msg = content
        elif msgtype == "fileUrl":
            msg = message

        else:
            raise TypeError("消息类型type输入错误，请输入：text/fileUrl")
        
        for user in touser:        
            send_values = {
                "to": user,
                "type": msgtype,
                "content": msg,
                "isRoom": isroom
            }
            send_msges = bytes(json.dumps(send_values), "utf-8")
            
            _LOGGER.debug(send_values)
            _LOGGER.debug(send_url)
            _LOGGER.debug(send_msges)
            _LOGGER.debug(self._header)
            
            response = requests.post(send_url, send_msges, headers=self._header).json()        
            
            if response["success"] != True:
                _LOGGER.error(response)
            else:
                _LOGGER.debug(response)
