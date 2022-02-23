from collections import deque


class Queue(object):
    def __init__(self):
        self.deque = deque()

    def append(self, elem):
        self.deque.append(elem)

    def add(self, elements: list):
        for i in elements:
            self.append(i)

    def take_batch(self, batch_size=24):
        batch = []

        for item in self:
            if len(batch) < batch_size:
                batch.append(item)
            else:
                break

        return batch

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.deque.popleft()
        except IndexError:
            raise StopIteration
