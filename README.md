# 妹子图

#### 一、介绍
应朋友要求，写了一个宅男福利爬虫，利用`Scrapy`爬取妹子图网站(ituba.cc)，并下载到本地。

(⊙﹏⊙)额，请放心食用，挂代理可使进餐速度加快！

#### 二、软件架构
Python 3.11.3

Scrapy 2.9.0

#### 三、更新记录
##### 2020.05.21
1.修复软件中的bug<br>
2.添加.gitignore文件，删除无用文件

#### 四、使用说明
```
git clone https://github.com/AwsomeCui/Meizitu.git
cd Meizitu
#1.该脚本跑ituba.cc的图片存在本地
python3 itubacc.py
#2.该脚本跑everia.club的图片链接信息存储再mongodb中
python3 everia.py
```
程序会自动在个人主目录创建meizi文件夹，目录格式为 `~/meizi/{sort1}/{sort2}/{title}/{page}.jpg`
![文件保存路径](./screenshot/WX20200521-002301.png)

#### 五、成果图
![成果图](./screenshot/WX20190408-222536.png)

#### 六、特别声明

此爬虫仅供学习使用，不得用于商业用户，侵删！
