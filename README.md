<!--
 * @Description: 
 * @Author: colin gao
 * @Date: 2023-05-07 06:46:52
 * @LastEditTime: 2023-05-20 21:07:48
-->

# langchain-chatbot
基于langchain框架，一个检索式和生成式的chatbot。

## langchain过河记系列文章
- [langchain过河记（一）](https://zhuanlan.zhihu.com/p/630925973)

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
```
python ingest.py
```

## run chatbot
```
python chatbot.py
```

## run app
```
python app.py
```

## test by http server
```curl
curl --location --request POST 'http://127.0.0.1:9000/chat' \
--header 'Content-Type: application/json' \
--data-raw '{
	"text": "你好"
}'
```

## run streamlit
```
streamlit run streamlit.py
```

## docker构建
```
docker-compose up -d
```

## 进程管理工具 supervisor
- 查看进程 `supervisorctl status`
- 查看进程日志 `supervisorctl tail -f clash`
- 查看进程日志文件 `/var/log/clash.log`
