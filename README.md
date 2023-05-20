<!--
 * @Description: 
 * @Author: colin gao
 * @Date: 2023-05-07 06:46:52
 * @LastEditTime: 2023-05-10 18:05:57
-->

# langchain-chatbot

Based on the Langchain framework, a retrieval and generative chatbot.

## usage

```
pip install -r requirements.txt
```

## copy env

```bash
cp .template.env .env
```

## edit env

edit your env config

## run chatbot

```
python chatbot.py
```

## run streamlit

```
streamlit run streamlit.py
```

## 进程管理工具 supervisor

- 查看进程 `supervisorctl status`
- 查看进程日志 `supervisorctl tail -f clash`
- 查看进程日志文件 `/var/log/clash.log`

## TODO

[TODO](./TODO.md)
