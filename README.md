# remote_control
基于[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot )的bot私聊消息/好友申请等信息定向转发

## 当前功能
* 审批入群邀请 
  * 分全部拒绝、全部同意、由bot管理员审批、仅同意特定QQ号邀请四个模式
  * 需要先将bot的QQ设置为审批入群
  * 现在被邀请进50人以下的群默认是不需要同意的，这部分的处理方法之后再补
* 审批好友申请
  * 分全部拒绝、全部同意、由bot管理员审批、仅同意以特定理由发起的申请四个模式
  * 需要先将bot的QQ设置为需要验证信息加好友
  * 同上，需要先将bot的QQ设置为审批加好友
* 私聊消息中继
  * 将bot收到的所有私聊消息转发给指定QQ号
  * 转发对象需与bot的QQ互为好友
* 黑名单
  * bot将不会加入列入黑名单中的群，不会同意来自列入黑名单中的QQ的入群邀请/好友申请，不会转发来自列入黑名单中的QQ的私聊消息
  * 黑名单的优先级高于以上功能的模式

## 使用方法
* 在hoshinobot的`modules`文件夹内：
  > git clone https://github.com/Shiina-Yukari/remote_control.git

* 按说明修改`modules/remote_control/config.json`配置文件内容。
  > group_invite（入群邀请相关）
  >> mode：入群审批模式
  >> + 0：全部拒绝
  >> + 1：全部同意
  >> + 2：管理员审批
  >> + 3：仅同意来自特定QQ号的邀请
  > 
  >> monitor：模式2所需的管理员QQ，需要和bot的QQ互为好友
  > 
  >> admin：模式3所需的特定QQ号列表

  > friend_invite（好友申请相关）
  >> mode：入群审批模式
  >> + 0：全部拒绝
  >> + 1：全部同意
  >> + 2：管理员审批
  >> + 3：仅同意以特定理由发起的申请
  >
  >> monitor：模式2所需的管理员QQ，需要和bot的QQ互为好友
  >
  >> keyword：模式3所需的特定理由内容

  > relay（私聊消息转发相关）
  >> mode：功能开关，0为关闭，1为打开
  >
  >> monitor：消息转发目标QQ，需要和bot的QQ互为好友

  > blacklist（黑名单）
  >> group：群组黑名单
  >
  >> friend：用户黑名单

  > reason（拒绝申请时使用的理由文本模板）
  >> reject：审批被拒绝（或超时）时的理由文本
  >
  >> blacklist：拒绝黑名单申请时的理由文本

* 在`config`文件夹的`__bot__.py`内加入`remote_control`模组：
  > MODULES_ON = {
  > 
  > ...
  > 
  >   'remote_control',
  > 
  > ...
  > 
  > }

* 重启HoshinoBot，之后可以按说明修改`modules/remote_control/config.json`配置文件内容。
