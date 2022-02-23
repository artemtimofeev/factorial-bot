import threading
from datetime import datetime
from heapq import heappush as insert, heappop as extract_maximum


class MessageQueue:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def push(self, message):
        self.lock.acquire()
        insert(self.queue, message)
        self.lock.release()

    def pop(self):
        self.lock.acquire()
        messages_to_send = []
        current_time = datetime.timestamp(datetime.now())

        while (len(self.queue) > 0
               and self.queue[0].send_time < current_time):
            messages_to_send.append(extract_maximum(self.queue))

        self.lock.release()

        return messages_to_send
