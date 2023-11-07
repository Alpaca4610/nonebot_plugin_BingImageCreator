import nonebot
import asyncio
import random
import os

from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment,MessageEvent,Bot

from BingImageCreator import ImageGen
from .config import Config, ConfigError


plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())
if not plugin_config.bing_cookies:
    raise ConfigError("请设置BingImageCreator的cookies!")
if plugin_config.bing_proxy:
    os.environ["http_proxy"] = plugin_config.bing_proxy
    os.environ["https_proxy"] = plugin_config.bing_proxy

paint = on_command("画图", block=False, priority=1)

@paint.handle()
async def _(bot: Bot,event: MessageEvent, msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    random_cookies = random.choice(plugin_config.bing_cookies)
    image_ = ImageGen(random_cookies,None,None,None)
    await paint.send(str("DALL·E 3正在画图中....."))
    loop =  asyncio.get_event_loop()
    try:
        res = await loop.run_in_executor(None, image_.get_images, content)
    except Exception:
        await paint.finish(MessageSegment.text("画图错误"),at_sender = True)

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
