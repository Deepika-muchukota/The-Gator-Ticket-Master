class Node:
    def __init__(self, user_id, seat_id):
        # Initialize node with user_id as key and seat_id as value
        self.user_id = user_id   # Key for searching
        self.seat_id = seat_id   # Value stored
        self.parent = None       # Parent node reference
        self.left = None         # Left child reference
        self.right = None        # Right child reference
        self.color = 'RED'       # New nodes are always red

class RedBlackTree:
    def __init__(self):
        # Initialize empty red-black tree with NIL sentinel node
        self.NIL = Node(None, None)   # NIL nodes are always black
        self.NIL.color = 'BLACK'      # Empty tree points to NIL
        self.root = self.NIL

    def left_rotate(self, x):
        # Perform left rotation to maintain red-black tree properties
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        # Perform right rotation to maintain red-black tree properties
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, user_id, seat_id):
        # Insert new node and maintain red-black properties
        node = Node(user_id, seat_id)
        node.left = self.NIL
        node.right = self.NIL
        
        # Find insertion position
        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.user_id < x.user_id:
                x = x.left
            else:
                x = x.right

        # Set parent and insert node
        node.parent = y
        if y == None:
            self.root = node
        elif node.user_id < y.user_id:
            y.left = node
        else:
            y.right = node

        self.insert_fixup(node)   

    def insert_fixup(self, k):
        while k.parent and k.parent.color == 'RED':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'BLACK'

    def find(self, user_id):
        # Find node with given user_id
        node = self.root
        while node != self.NIL:
            if user_id == node.user_id:
                return node
            elif user_id < node.user_id:
                node = node.left
            else:
                node = node.right
        return None

    def delete(self, user_id):
        # Delete node with given user_id
        z = self.find(user_id)
        if not z:
            return False

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'BLACK':
            self.delete_fixup(x)
        return True

    def delete_fixup(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 'BLACK' and w.right.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                else:
                    if w.right.color == 'BLACK':
                        w.left.color = 'BLACK'
                        w.color = 'RED'
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.right.color = 'BLACK'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 'BLACK' and w.left.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                else:
                    if w.left.color == 'BLACK':
                        w.right.color = 'BLACK'
                        w.color = 'RED'
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.left.color = 'BLACK'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'BLACK'

    def transplant(self, u, v):
        # Helper method for delete operation
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        # Find minimum value in subtree rooted at node
        while node.left != self.NIL:
            node = node.left
        return node

    def in_order_traversal(self):
        # Get sorted list of (seat_id, user_id) pairs
        result = []
        def _in_order(node):
            if node != self.NIL:
                _in_order(node.left)
                result.append((node.seat_id, node.user_id))
                _in_order(node.right)
        _in_order(self.root)
        return result