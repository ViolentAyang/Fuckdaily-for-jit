# Fuckdaily-for-jit
金陵科技学院每日打卡脚本

#### 使用GITHUB ACTIONS自动签到
在本项目页面点击右上角fork，将github项目上传至你自己的仓库，Fork后在自己的仓库页面进入Action允许使用我配置好的工作环境，点击Settings，在secrets-Action里点击New repositories secrets增加`ACCOUNT`、`PASSWORD`、`SEVERKEY` 3个Secrets，分别对应你的账号、密码、方糖推送号（不需要推送可填无，需要密钥自行去获取：https://sct.ftqq.com/）

#### 关于表单内容更新
每日打卡表单的数据会自动获取前一天（上一次填写的表单）填写的数据填写，当需要更新表单时，自行去打卡界面重新填写并保存，脚本无需做任何更改。需要更新secrets数据时在原先设置secrets的地方点选对应密钥的update。如果想停止运行脚本，可以在Action中的AutoDaily里右上角三个点选项中点击Disable Workflow关闭

#### 图文教程
![](imagec/01.png)
![](imagec/02.png)
![](imagec/03.png)
![](imagec/04.png)
![](imagec/05.png)
![](imagec/06.png)
![](imagec/07.png)
![](imagec/08.png)
![](imagec/09.png)
![](imagec/10.png)
