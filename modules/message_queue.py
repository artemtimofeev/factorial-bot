from datetime import datetime
from heapq import heappush as insert, heappop as extract_maximum


class MessageQueue:
    def __init__(self):
        self.queue = []

    def push(self, message):
        insert(self.queue, message)

    def pop(self):
        messages_to_send = []
        current_time = datetime.timestamp(datetime.now())

        while (len(self.queue) > 0
               and self.queue[0].send_time < current_time):
            messages_to_send.append(extract_maximum(self.queue))

        return messages_to_send
