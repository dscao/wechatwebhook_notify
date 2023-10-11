# wechatwebhook_notify
wechatwebhook notify for homeassistant custom component


Thanks to: https://github.com/danni-cool/docker-wechatbot-webhook


配置：
```notify:
  - platform: wechatwebhook_notify
    name: wechatwebhook #自定义推送服务名称，比如这里出来就是 notify.wechatwebhook
    touser: '大胜' #默认发送对象昵称 
    isRoom: false  #默认发送对象是否是群 
    resource: 'http://192.168.8.2:3001'   #wechatbot-webhook服务器url
```

调用：
```
service: notify.wechatwebhook
data:
  message: 消息内容
  target:
    - 昵称1
    - 昵称2
    - 昵称3
    
service: notify.wechatwebhook
data:
  message: 发送纯文本消息，当前时间：{{now().strftime('%Y-%m-%d %H:%M:%S')}}


service: notify.wechatwebhook
data:
  message: 发送带标题和分隔线的纯文本消息,我就是我, 是不一样的烟火
  title: 这是标题

service: notify.wechatwebhook
data:
  message: 'https://samplelib.com/lib/preview/mp3/sample-3s.mp3'
  data:
    type: fileUrl
```

