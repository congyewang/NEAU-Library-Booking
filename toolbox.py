import requests
from PIL import Image
import matplotlib.pyplot as plt


class Toolbox(object):
    """
    预定东北农业大学图书馆存柜及研修间
    """
    def __init__(self, login_url, username, password, check_url, result_url):
        self.login_url = login_url
        self.result_url = result_url
        self.pic_url = "http://yd.lib.neau.edu.cn/public/captcha.html"
        self.check_url = check_url
        self.s = requests.Session()
        self.captcha = ""
        self.data = {
            "username": username,
            "password": password
        }

    def post_data(self, post_key, num=1):
        """
        用于post数据
        :param post_key: 若存柜则为"lc", 研修间则为"fjlx"
        :param num: 存柜输入楼层号, 研修间输入房间类型
        :return: code, msg, data: code为状态码, msg为提示信息, data一般为None
        """
        while True:
            # get pic
            pic = self.s.get(self.pic_url, timeout=200)
            with open("captcha.png", "wb") as file:
                file.write(pic.content)
            try:
                img = Image.open("captcha.png")
                # img.show()
                plt.figure("captcha")
                plt.imshow(img)
                plt.show()
            except IOError:
                print("Fail to load image!")
            captcha = input("Please input the captcha code:")
            self.data["captcha"] = captcha
            # check_code
            check = self.s.post(
                url=self.check_url,
                data=self.data,
                timeout=200)
            code = check.json()['code']
            if code == 200:
                print("Captcha code currect!")
                break
            else:
                print(f"Captcha code error! Error code: {code}")
        # post
        post_data = {post_key: str(num)}
        result = self.s.post(self.result_url, data=post_data, timeout=200)
        if result.status_code == 200:
            try:
                code = result.json()['code']
                msg = result.json()['msg']
                data = result.json()['data']
                print("Posting suceed!")
                return code, msg, data
            except Exception:
                print(f"Post error! Error code:{result.status_code}")

    @classmethod
    def cyd(cls, num=5):
        """
        存柜预定
        :param num: 存柜楼层
        :return: None
        """
        login_url = "http://yd.lib.neau.edu.cn/public/index/index/index.html"
        username = "A05160308"
        password = "303611"
        check_url = "http://yd.lib.neau.edu.cn/public/login.html"
        result_url = "http://yd.lib.neau.edu.cn/public/yd.html"
        i = 1

        while True:
            cyd = cls(login_url, username, password, check_url, result_url)
            code, msg, data = cyd.post_data("lc", num)
            if code == 200:
                print("-" * 50)
                print(f"第{i}次")
                print(f"状态码:{code}\n消息:{msg}\n数据:{data}")
                print("已成功预定!")
                print("-" * 50)
                break
            else:
                print("-" * 50)
                print(f"第{i}次")
                print(f"状态码:{code}\n消息:{msg}\n数据:{data}")
                print("-" * 50)
                i += 1

    @classmethod
    def yyd(cls, num=1):
        """
        预定研修间
        :param num: 预定房间类型
        :return: None
        """
        login_url = 'http://yd.lib.neau.edu.cn/public/index/yxj/main.html'
        username = "A05160308"
        password = "303611"
        check_url = "http://yd.lib.neau.edu.cn/public/ylogin.html"
        result_url = "http://yd.lib.neau.edu.cn/public/yyuding.html"
        i = 1

        while True:
            yyd = cls(login_url, username, password, check_url, result_url)
            code, msg, data = yyd.post_data("fjlx", num)
            if code == 200:
                print("-" * 50)
                print(f"第{i}次")
                print(f"状态码:{code}\n消息:{msg}\n数据:{data}")
                print("已成功预定!")
                print("-" * 50)
                break
            else:
                print("-" * 50)
                print(f"第{i}次")
                print(f"状态码:{code}\n消息:{msg}\n数据:{data}")
                print("-" * 50)
                i += 1


if __name__ == "__main__":
    Toolbox.cyd()
