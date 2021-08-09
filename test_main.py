from unittest import TestCase

from main import split_video
from main import get_tt_video_id


class Test(TestCase):
    def test_split_video(self):
        print(split_video(r'input.mp4'))
    
    def test_get_tt_video_id_1(self):
        assert '6992485399234907398' == get_tt_video_id(
            r'https://m.tiktok.com/v/6992485399234907398.html?_d=secCgYIASAHKAESMgow%2FoLPUSRdVoGg1M8Gh%2FcPUjTRu6D%2FJcyaoq7J6MYOsRcAam5BbOY1mvf66Pfe%2BzSQGgA%3D&checksum=938bd3eb4b37ca3a0a28a21347de504208315da7ad879bb7fa1cc1dd9f7a4235&language=ru&preview_pb=0&sec_user_id=MS4wLjABAAAAEAU1M4bxAoqlZy5JSz3HZGjN54uToEUPQ8E-Cvdp115IZ_UAjf-pAxipcvBPN1OB&share_app_id=1233&share_item_id=6992485399234907398&share_link_id=f367c26c-a0e2-45ca-8fd5-e3075943474f&source=h5_m&timestamp=1628440106&u_code=de91i62309glhi&user_id=6867927059425100805&utm_campaign=client_share&utm_medium=android&utm_source=vk')
    
    def test_get_tt_video_id_2(self):
        assert '6992485399234907398' == get_tt_video_id(
            r'https://www.tiktok.com/@watchhololive/video/6992485399234907398?_d=secCgYIASAHKAESMgow%2FoLPUSRdVoGg1M8Gh%2FcPUjTRu6D%2FJcyaoq7J6MYOsRcAam5BbOY1mvf66Pfe%2BzSQGgA%3D&checksum=938bd3eb4b37ca3a0a28a21347de504208315da7ad879bb7fa1cc1dd9f7a4235&language=ru&preview_pb=0&sec_user_id=MS4wLjABAAAAEAU1M4bxAoqlZy5JSz3HZGjN54uToEUPQ8E-Cvdp115IZ_UAjf-pAxipcvBPN1OB&share_app_id=1233&share_item_id=6992485399234907398&share_link_id=f367c26c-a0e2-45ca-8fd5-e3075943474f&source=h5_m&timestamp=1628440106&u_code=de91i62309glhi&user_id=6867927059425100805&utm_campaign=client_share&utm_medium=android&utm_source=vk&_r=1&is_copy_url=1&is_from_webapp=v1')
