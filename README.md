<!--
 * @Description: 
 * @Author: colin gao
 * @Date: 2023-05-07 06:46:52
 * @LastEditTime: 2023-05-23 17:02:36
-->

# langchain-chatbot
Langchain-Chatbot 是基于 Langchain 框架的检索式和生成式聊天机器人。该机器人能够以对话的方式理解并回应用户的输入​1​。

## Running by command
```
pip install -r requirements.txt
```

## copy env
```bash
cp .template.env .env
```

## edit env
配置你自己的environment，包括openai-key和科学上网代理

## 构建知识库
运行以下命令构建知识库
```
python ingest.py
```

## run chatbot
运行以下命令启动聊天机器人
```
python chatbot.py
```

## 运行应用
运行以下命令启动应用
```
python app.py
```

## 通过HTTP服务器测试
您可以通过向 'http://127.0.0.1:9000/chat' 发送 POST 请求，其 JSON 主体包含聊天机器人要响应的文本，来测试聊天机器人。例如：
```curl
curl --location --request POST 'http://127.0.0.1:9000/chat' \
--header 'Content-Type: application/json' \
--data-raw '{
	"text": "你好"
}'
```

## docker构建
运行以下命令构建Docker镜像并启动Docker容器
```
docker-compose up -d
```

## 进程管理工具 supervisor
您可以使用 Supervisor 来管理进程。这里是一些有用的命令：
- 查看进程 `supervisorctl status`
- 查看进程日志 `supervisorctl tail -f clash`
- 查看进程日志文件 `/var/log/clash.log`

## langchain过河记系列文章
- [langchain过河记（一）](https://zhuanlan.zhihu.com/p/630925973)
- [langchain过河记（二）](https://zhuanlan.zhihu.com/p/630930843)
- [langchain过河记（三）](https://zhuanlan.zhihu.com/p/630971903)
- [langchain过河记（四）](https://zhuanlan.zhihu.com/p/631600368)

## external link
[liveportraitweb](https://www.liveportraitweb.com/)
[novelling](https://www.novelling.com/)
[Rewritifyai](https://www.rewritifyai.com/)
[MMAudio](https://www.mmaudio.pro/)
