import nonebot
import asyncio
import random
import os

from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment,MessageEvent,Bot, PrivateMessageEvent
from nonebot.plugin import PluginMetadata
from .generator import gen
from .config import Config, ConfigError


plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())
if not plugin_config.bing_cookies:
    raise ConfigError("请设置BingImageCreator的cookies!")
if plugin_config.bing_proxy:
    os.environ["http_proxy"] = plugin_config.bing_proxy
    os.environ["https_proxy"] = plugin_config.bing_proxy

paint = on_command("画图", block=False, priority=1)

__plugin_meta__ = PluginMetadata(
    name="DALL-E 3绘图",
    description="调用NewBing的DALL-E 3进行绘图",
    usage=
    '''
    直接发送: 画图 XXXXXX
    ''',
    config= Config,
    extra={},
    type="application",
    homepage="https://github.com/Alpaca4610/nonebot_plugin_BingImageCreator.git",
    supported_adapters={"~onebot.v11"}
)


@paint.handle()
async def _(bot: Bot,event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    random_cookies = random.choice(plugin_config.bing_cookies)
    await paint.send(str("DALL·E 3正在画图中....."))
    try:
        res = await gen(random_cookies,content)
    except Exception as e:
        await paint.finish(MessageSegment.text("画图错误 "+ str(e)),at_sender = True)


    if isinstance(event, PrivateMessageEvent):
        for pic in res:
            await paint.send(MessageSegment.image(pic))
    else:
        msgs = [
                        {
                            "type": "node",
                            "data": {
                                "name": "DALLE 3",
                                "uin": bot.self_id,
                                "content": MessageSegment.image(pic),
                            },
                        }
                        for pic in res               
                    ]
        
        await bot.call_api("send_group_forward_msg",group_id=event.group_id,messages=msgs)
