import subprocess
from datetime import timedelta
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

users = {}


def get_tt_video_id(url: str) -> str:
    a = re.findall(r'((@.*\/.*\/)|(\/v\/))([\d]*)', url)
    return a[-1][-1]


def download_tt(tt_link) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    
    response = requests.get(tt_link, headers=headers)
    
    api = TikTokAPI(cookie=response.cookies)
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
    if dur / 4 > part_len:
        return []
    
    for i in range(int(dur + part_len / 2) // part_len):
        fname = video_path + f"_{i}_out.mp4"
        command = f"./ffmpeg.exe -i {video_path} " \
                  f" -ss 00:00:{str(part_len * i).zfill(2)} -t 00:00:{str(part_len).zfill(2)} " \
                  f" -c:v libx264 {fname} -y"
        print(command)
        subprocess.run(command)
        ret.append(fname)
    os.remove(video_path)
    return ret


def process_tt_msg(event: VkBotMessageEvent):
    peer_id = event.obj.get('peer_id')
    from_id = event.obj.get('from_id')
    tt_file = download_tt(text)
    vids = split_video(tt_file)
    
    # tt_video = uploader.story(vids[0], 'video', user_ids=[from_id])
    tt_video = uploader.story(vids[0], 'video', group_id=GROUP_ID, link_text="more",
                              link_url=r"https://vk.com/donut/public206314659")
    data = tt_video.json()
    attstr = f"story{data['response']['story']['owner_id']}_{data['response']['story']['id']}"
    
    vk.messages.send(peer_id=peer_id,
                     attachment=attstr,
                     random_id=get_random_id())
    
    for vid in vids[1:]:
        uploader.story(vid, 'video', group_id=GROUP_ID)
    
    for v in vids:
        os.remove(v)


if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=os.getenv("BOT_TOKEN"))
    GROUP_ID = int(os.getenv("GROUP_ID"))
    longpoll = VkBotLongPoll(vk_session, GROUP_ID, wait=-9)
    vk = vk_session.get_api()
    uploader = VkUpload(vk)
    
    TIKTOK_SUBSTRING = 'https://vm.tiktok.com'
    
    print("start")
    
    while True:
        try:
            print('listen')
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    text: str = event.obj.get('text')
                    sender = event.obj.get('from_id')
                    print(event)
                    if text.find(TIKTOK_SUBSTRING) != -1:
                        if sender in users:
                            if (datetime.now() - users[sender]).seconds < 20:
                                continue
                        users[sender] = datetime.now()
                        process_tt_msg(event)
        except Exception as e:
            print(e)
