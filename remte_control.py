import json
import os
import time

from aiocqhttp.default import on_message
from nonebot import RequestSession, on_request, on_command, CommandSession

from hoshino import Service, logger

from uuid import uuid4

sv = Service('remote_control', visible=True, enable_on_default=True, bundle='remote_control', help_='''
控制你的bot
'''.strip())
config_default = {
    "group_invite": {
        "mode": 0,  # 0：全部拒绝；1：全部同意；2：管理员审批；3：仅同意来自特定QQ号的邀请
        "monitor": "123",  # 模式2里的管理员QQ
        "admin": ["123", "234", "345"]  # 模式3里的特定QQ号列表
    },
    "friend_invite": {
        "mode": 0,  # 0：全部拒绝；1：全部同意；2：管理员审批；3：仅同意以特定理由发起的申请
        "monitor": "123",  # 模式2里的管理员QQ
        "keyword": "miracle_word"  # 模式3里的特定理由内容
    },
    "relay": {
        "mode": 0,  # 0：关闭；1：打开
        "monitor": "123123123"  # 消息转发目标QQ
    },
    "blacklist": {
        "group": ["123", "234", "345"],  # 群组黑名单
        "friend": ["123", "234", "345"]  # 用户黑名单
    },
    "reason": {
        "reject": "请联系bot管理组成员审批。",  # 审批被拒绝（或超时）时的理由文本
        "blacklist": "DO NOT DISTURB."  # 拒绝黑名单申请时的理由文本
    }
}
pathcfg = os.path.join(os.path.dirname(__file__), 'config.json')
if not os.path.exists(pathcfg):
    try:
        with open(pathcfg, 'w') as cfgf:
            json.dump(config_default, cfgf, ensure_ascii=False, indent=2)
            logger.error('[WARNING]未找到配置文件，已根据默认配置模板创建，请打开插件目录内config.json查看和修改。')
    except Exception:
        logger.error('[ERROR]创建配置文件失败，请检查插件目录的读写权限及是否存在config.json。')
config = json.load(open(pathcfg, 'r', encoding='utf8'))
approve_dict = dict()


uuidChars = ("a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
             "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
             "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z")


def short_uuid():
    uuid = str(uuid4()).replace('-', '')
    result = ''
    for i in range(0,8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub,16)
        result += uuidChars[x % 0x3E]
    return result


def get_config(key, sub_key):
    if key in config and sub_key in config[key]:
        return config[key][sub_key]
    return None


@on_request('group.invite')
async def handle_group_invite(session: RequestSession):
    mode = get_config("group_invite", "mode")
    uid = str(session.ctx['user_id'])
    gid = str(session.ctx['group_id'])
    if gid not in get_config("blacklist", "group") and uid not in get_config("blacklist", "friend"):
        if mode == 1:
            await session.approve()
        elif mode == 2:
            uuid = short_uuid()
            approve_dict[uuid] = False
            monitor_message = f"收到来自QQ：{uid} 的邀请入群通知，群号：{gid}\n若同意，请回复 botctrl {uuid}\n此消息发送时间为{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}，有效时长30分钟。"
            await session.bot.send_private_msg(user_id=int(get_config("group_invite", "monitor")),
                                               message=monitor_message)
            for i in range(0, 6):
                time.sleep(300)
                if approve_dict[uuid]:
                    await session.approve()
                    break
            if not approve_dict[uuid]:
                await session.reject(reason=get_config("reason", "reject"))
            approve_dict.pop(uuid, "nokey")
        elif mode == 3:
            if uid in get_config("group_invite", "admin"):
                await session.approve()
            else:
                await session.reject(reason=get_config("reason", "reject"))
    else:
        await session.reject(reason=get_config("reason", "blacklist"))


@on_request('friend')
async def handle_friend_invite(session: RequestSession):
    mode = get_config("friend_invite", "mode")
    uid = str(session.ctx['user_id'])
    if uid not in get_config("blacklist", "friend"):
        if mode == 1:
            await session.approve()
        elif mode == 2:
            uuid = short_uuid()
            approve_dict[uuid] = False
            monitor_message = f"收到来自QQ：{uid} 的好友申请。\n若同意，请回复 botctrl {uuid}\n此消息发送时间为{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}，有效时长30分钟。"
            await session.bot.send_private_msg(user_id=int(get_config("group_invite", "monitor")),
                                               message=monitor_message)
            for i in range(0, 6):
                time.sleep(300)
                if approve_dict[uuid]:
                    await session.approve()
                    break
            if not approve_dict[uuid]:
                await session.reject(reason=get_config("reason", "reject"))
            approve_dict.pop(uuid, "nokey")
        elif mode == 3:
            comm = session.ctx['comment']
            if comm == get_config("friend_invite", "keyword"):
                await session.approve()
            else:
                await session.reject(reason=get_config("reason", "reject"))
    else:
        await session.reject(reason=get_config("reason", "blacklist"))


@on_command('botctrl')
async def bot_control(session: CommandSession):
    uuid = session.current_arg_text.strip()
    if not uuid:
        uuid = (await session.aget(prompt='请发送审批UID。')).strip()
    if uuid in approve_dict:
        approve_dict[uuid] = True
        await session.send("已完成审批。")
    else:
        await session.send("无该审批UID。")


@on_message('private')
async def msg_relay(session: CommandSession):
    mode = get_config("relay", "mode")
    if mode == 1:
        uid = str(session.ctx['user_id'])
        if uid not in get_config("blacklist", "friend"):
            monitor = int(get_config("group_invite", "monitor"))
            sub_type = session.ctx['sub_type']
            msg = session.ctx['message']
            relay_header = f"收到来自QQ：{uid} 的私聊消息，消息类型：{sub_type}。\n以下为消息内容："
            await session.bot.send_private_msg(user_id=monitor, message=relay_header)
            await session.bot.send_private_msg(user_id=monitor, message=msg)
