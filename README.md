# Django-Mall
Django天天生鲜商城项目根据传智播客教程编写，除了复现代码之外，做了一定的优化（忘记密码根据邮箱重置），旨在熟悉与理解Django框架。

# 在本地运行项目
* 克隆项目到本地
>```Bash
>git clone https://github.com/ennl2py/Django-Mall.git
>```
* 创建虚拟环境
* 安装项目依赖
>```Bash
>pip install -r requirements.txt
>```
* 迁移数据库
>在下一行代码运行前，请根据你的数据库实际情况，修改项目文件夹`ttshengxian`下`settings.py`文件中的`DATABASES`配置（本例采用的是MySQL数据库，并用`PyMysql`进行管理）
>```Bash
>python manage.py migrate
>```
* 创建后台管理员账户
>```Bash
>python manage.py createsuperuser
>```
* 运行开发服务器
>```Bash
>python manage.py runserver
>```
* 添加商品分类及相应分类对应的商品
>在浏览器输入：127.0.0.1:8000/admin，登录到后台，商品分类根据前端设计只需要添加6个，分别为新鲜水果、海鲜水产、猪牛羊肉、禽类蛋品、新鲜蔬菜、速冻食品6个，分类添加完毕后，添加商品即可。
* 项目预览
>在浏览器输入：127.0.0.1:8000，查看效果。
