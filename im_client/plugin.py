class Plugin:
    def __init__(self, name, reader, writer):
        self.reader = reader
        self.writer = writer
        self.name = name
        self.deffered_tasks = []

    def defer(self, task):
        self.deffered_tasks.append(task)