import subprocess
import traceback
from datetime import timedelta
from time import sleep
from typing import List

from datetime import datetime
import ffmpeg
from TikTokAPI import TikTokAPI
from ffprobe import FFProbe

import re
import os
import requests

import vk_api
from vk_api.utils import get_random_id
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent

import logging as log

users = {}


def get_tt_video_id(url: str) -> str:
    a = re.findall(r'((@.*\/.*\/)|(\/v\/))([\d]*)', url)
    return a[-1][-1]


tt_session = requests.sessions.Session()


def renew_session():
    tt_session.close()


def download_tt(tt_link) -> str:
    l = log.getLogger("download_tt")
    
    try:
        response = tt_session.get(tt_link)
    except:
        renew_session()
        response = tt_session.get(tt_link)
        
    api = TikTokAPI(cookie=tt_session.cookies)
    cwd = os.getcwd()
    vid = get_tt_video_id(response.url)
    file_path = cwd + '\\' + vid + '.mp4'
    api.downloadVideoById(vid, file_path)
    response.close()
    
    return file_path


def split_video(video_path: str, part_len=14) -> List[str]:
    ret = []
    metadata = FFProbe(video_path)
    dur = metadata.video[0].duration_seconds()
    if dur <= part_len:
        return [video_path]
    if dur / 8 > part_len:
        return []
    
    for i in range(int(dur + part_len / 2) // part_len):
        fname = video_path + f"_{i}_out.mp4"
        command = f"./ffmpeg.exe -i {video_path} " \
                  f" -ss 00:00:{str(part_len * i).zfill(2)} -t 00:00:{str(part_len).zfill(2)} " \
                  f" -c:v libx264 {fname} -y"
        print(command)
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ret.append(fname)
    os.remove(video_path)
    return ret


def process_tt_msg(event: VkBotMessageEvent):
    l = log.getLogger("process_tt_msg")
    peer_id = event.obj.get('peer_id')
    from_id = event.obj.get('from_id')
    tt_file = download_tt(text)
    vids = split_video(tt_file)
    vk.messages.setActivity(peer_id=peer_id, type="typing")
    # tt_video = uploader.story(vids[0], 'video', user_ids=[from_id])
    try:
        tt_video = uploader.story(vids[0], 'video', group_id=GROUP_ID, link_text="more",
                                  link_url=r"https://vk.com/donut/public206314659")
    except Exception as e:
        l.getChild("can't upload story").error(e)
        return
    
    data = tt_video.json()
    attstr = f"story{data['response']['story']['owner_id']}_{data['response']['story']['id']}"
    
    try:
        vk.messages.send(peer_id=peer_id,
                         attachment=attstr,
                         random_id=get_random_id())
    except Exception as e:
        l.getChild("can't send vk message").error(e)
    
    for vid in vids[1:]:
        sleep(0.5)
        try:
            uploader.story(vid, 'video', group_id=GROUP_ID)
        except Exception as e:
            l.getChild("can't upload story").error(e)
    
    for v in vids:
        try:
            os.remove(v)
        except Exception as e:
            l.getChild("can't remove file").error(e)


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    l = log.getLogger("main")
    vk_session = vk_api.VkApi(token=os.getenv("BOT_TOKEN"))
    GROUP_ID = int(os.getenv("GROUP_ID"))
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    vk = vk_session.get_api()
    uploader = VkUpload(vk)
    
    TIKTOK_SUBSTRING = 'https://vm.tiktok.com'
    
    l.info("start")
    
    while True:
        try:
            l.info('listen')
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    text: str = event.obj.get('text')
                    sender = event.obj.get('from_id')
                    if text.find(TIKTOK_SUBSTRING) != -1:
                        if sender in users:
                            if (datetime.now() - users[sender]).seconds < 20:
                                continue
                        users[sender] = datetime.now()
                        process_tt_msg(event)
        except Exception as e:
            l.exception(e)
            renew_session()
