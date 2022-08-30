# Fuckdaily-for-jit
金陵科技学院每日打卡脚本

#### 使用GITHUB ACTIONS自动签到（因为外网ip原因，容易翻车）
在本项目页面点击右上角fork，将github项目上传至你自己的仓库，Fork后在自己的仓库页面进入Action允许使用我配置好的工作环境，点击Settings，在secrets-Action里点击New repositories secrets增加`ACCOUNT`、`PASSWORD`、`SEVERKEY` 3个Secrets，分别对应你的账号、密码、方糖推送号（不需要推送可填无，需要密钥自行去获取：https://sct.ftqq.com/）


#### 部署服务器自动签到（推荐）
服务器上需要安装python环境和requests库

`pip3 install requests`

`0 1 * * * python FuckDaily.py 账号 密码 sever酱密钥`

#### 关于表单内容更新
每日打卡表单的数据会自动获取前一天（上一次填写的表单）填写的数据填写，当需要更新表单时，自行去打卡界面重新填写并保存，脚本无需做任何更改。需要更新secrets数据时在原先设置secrets的地方点选对应密钥的update。如果想停止运行脚本，可以在Action中的AutoDaily里右上角三个点选项中点击Disable Workflow关闭

#### action部署图文教程
![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/01.png)
Fork本项目
![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/02.png)
创建仓库
![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/03.png)
配置工作环境
![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/04.png)
进入设置
![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/05.png)
设置账号密码
![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/06.png)

![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/08.png)
填写密钥`ACCOUNT`、`PASSWORD`、`SEVERKEY`
![image](https://github.com/Reclizer/Fuckdaily-for-jit/blob/main/image/10.png)
运行
