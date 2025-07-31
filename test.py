class Node:
    def __init__(self, val: int, neighbors: list):
        self.val = val
        self.neighbors = neighbors if neighbors else []


prev_node = [[2, 4], [1, 3], [2, 4], [1, 3]]


def clone_node(node: Node):
    pass


copy_node = clone_node(prev_node)
print(copy_node)
