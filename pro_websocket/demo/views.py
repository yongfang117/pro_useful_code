from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from dwebsocket.decorators import require_websocket,accept_websocket
from django.http import HttpResponse
clients = []


def index(request):
    return render(request, 'index.html')


def index2(request):
    return render(request, 'index2.html')


def modify_message(message):
    return message.lower()


@accept_websocket
def echo(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            request.websocket.send(message)  # 发送消息到客户端


@require_websocket
def echo_once(request):
    message = request.websocket.wait()
    request.websocket.send(message)
