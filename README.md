# This test bot for VK was made by using vkbottle API.

This project requires installing dependencies with a [`requirements.txt`](requirements.txt) file.

```
pip install -r requirements.txt
```

Also there's a TOKEN which is hidden in .secret file, to use this app, please, generate your own token

```
TOKEN="token"
```

To run application please use the code below in your terminal:

```
python3 main.py
```
# Docker build
```
docker build -t vk-bot .
```

# Docker run
```
docker run -it --rm vk-bot
```