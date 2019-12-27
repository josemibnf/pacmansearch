class Node:
    def __init__(self, _state, _parent=None, _action=None, _cost=0, _depth=0):
        self.state = _state
        self.parent = _parent
        self.action = _action
        self.cost = 0
        self.depth = 0
        if self.parent != None:
            self.cost = self.cost + self.parent.cost
        
    def total_path(self):
        path = []
        curr = self
        while curr.parent != None:
            path.append(curr.action)
            curr = curr.parent
        return list(reversed(path))
    
    def get_state(self):
        return self.state

if __name__ == "__main__":
    n1 = Node([1,2,None, 3,4,5,6,7,8], None, None, 0)
    n2 = Node([1,2,5,3,4,5,6,7,8], n1, 'NORTH', 1)
    n3 = Node([1,2,None,3,4,5,6,7,8], n2, 'SOUTH', 1)
    
    print (n3.total_path())