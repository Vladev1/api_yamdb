# 69441654
class Dek:
    def __init__(self, max_size):
        self._data = [None] * max_size
        self._front = max_size - 1
        self._back = 0
        self._size = 0
    @property
    def is_full(self):
        return self._size == self._max_size

    @property
    def is_empty(self):
        return self._size == 0

    def push_back(self, value):
        self._back = self._push(self._back, 1, value)

    def pop_back(self):
        self._back, value = self._pop(self._back, 1)
        return value

    def push_front(self, value):
        self._front = self._push(self._front, -1, value)

    def pop_front(self):
        self._front, value = self._pop(self._front, -1)
        return value

    def _push(self, i, di, value):
        if self._size >= len(self._data):
            raise OverflowError
        self._data[i] = value
        self._size += 1
        return (i + di) % len(self._data)

    def _pop(self, i, di):
        if self._size <= 0:
            raise IndexError
        j = (i - di) % len(self._data)
        x = self._data[j]
        self._data[j] = None
        self._size -= 1
        return j, x


def main():
    count_command = int(input())
    queue_size = int(input())

    queue = Dek(queue_size)
    commands = {
        'push_front': queue.push_front,
        'push_back': queue.push_back,
        'pop_front': queue.pop_front,
        'pop_back': queue.pop_back,
    }
    for _ in range(count_command):
        command = input()
        operation, *value = command.split()
        if value:
            try:
                result = commands[operation](int(*value))
                if result is not None:
                    print(result)
            except OverflowError:
                print('error')
        else:
            try:
                result = commands[operation]()
                print(result)
            except IndexError:
                print('error')


if __name__ == '__main__':
    main()  