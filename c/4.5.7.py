
class BinaryTree:

    def __init__(self, v):
        self.v = v
        self.left_child = None
        self.right_child = None

    def insert_left(self, v):
        self.left_child = BinaryTree(v)
        return self
        
    def insert_right(self, v):
        self.right_child = BinaryTree(v)
        return self

    def __repr__(self):
        return f'{self.v}: {self.left_child.v} - {self.right_child.v}'

    def pre_order(self):
        print(self.v)
        if self.left_child is not None:
            self.left_child.pre_order()
        if self.right_child is not None:
            self.right_child.pre_order()

    def post_order(self):
        if self.left_child is not None:
            self.left_child.post_order()
        if self.right_child is not None:
            self.right_child.post_order()
        print(self.v, end=', ')

# создаём корень и его потомков /7|2|5\
node_root = BinaryTree(2).insert_left(7).insert_right(5)
# левое поддерево корня /2|7|6\
node_7 = node_root.left_child.insert_left(2).insert_right(6)
# правое поддерево предыдущего узла /5|6|11\
node_6 = node_7.right_child.insert_left(5).insert_right(11)
# правое поддерево корня /|5|9\
node_5 = node_root.right_child.insert_right(9)
# левое поддерево предыдущего узла корня /4|9|\
node_9 = node_5.right_child.insert_left(4)

print(node_root)
node_root.post_order()

