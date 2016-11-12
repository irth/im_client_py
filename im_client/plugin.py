class Plugin:
    def __init__(self, rpc):
        self.rpc = rpc
        self.name = None
        self.deffered_tasks = []

    def defer(self, task):
        self.deffered_tasks.append(task)