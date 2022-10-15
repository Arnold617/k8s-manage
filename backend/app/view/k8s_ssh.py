# @Time    : 2022/10/14 10:19
# @Author  : John
# @FileName: k8s_ssh.py

from channels.generic.websocket import WebsocketConsumer
from app.view.api import KubernetesTools
from threading import Thread


class K8SStreamThread(Thread):
    def __init__(self, websocket, container_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = container_stream

    def run(self):
        while self.stream.is_open():
            if self.stream.peek_stdout():
                stdout = self.stream.read_stdout()
                self.websocket.send(stdout)

            if self.stream.peek_stderr():
                stderr = self.stream.read_stderr()
                self.websocket.send(stderr)
        else:
            self.websocket.close()


class SSHConsumer(WebsocketConsumer):

    def connect(self):
        # self.name = self.scope["url_route"]["kwargs"]["name"]
        data = str(self.scope["query_string"], 'utf-8')
        data_tmp = data.split('&')
        namespace = data_tmp[0].split('=')[1]
        podName = data_tmp[1].split('=')[1]
        if namespace and podName:
            self.stream = KubernetesTools().pod_exec(podName, namespace)
            kub_stream = K8SStreamThread(self, self.stream)
            kub_stream.start()

        self.accept()

    def disconnect(self, close_code):
        # self.stream.write_stdin('exit\r')
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        self.stream.write_stdin(text_data)
