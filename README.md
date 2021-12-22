# remote_control
基于[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot )的bot私聊消息/好友申请等信息定向转发

## 当前功能
* 审批入群邀请 
    * 分全部拒绝、全部同意、由bot管理员审批、仅同意特定QQ号邀请四个模式
    * 需要先将bot的QQ设置为审批入群
    * 现在被邀请进50人以下的群默认是不需要同意的，这部分的处理方法之后再补
* 审批好友申请
    * 分全部拒绝、全部同意、由bot管理员审批、仅同意以特定理由发起的申请四个模式
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

* 在`config`文件夹的`__bot__.py`内加入`remote_control`模组：
    > MODULES_ON = {
    > 
    > ...
    > 
    >     'remote_control',
    > 
    > ...
    > 
    > }

* 重启HoshinoBot，之后可以按说明修改`modules/remote_control/config.json`配置文件内容。
