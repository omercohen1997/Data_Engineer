from dataclasses import dataclass

@dataclass
class Node:
    value: int
    left: 'Node' = None
    right: 'Node' = None    


class BST:
   
    def __init__(self):
        self.root = None
        self.size = 0
    
    
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            self.size += 1
        else:
            self.helper_insert(self.root, value)
            
    
    def helper_insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
                self.size += 1
            else:
                self.helper_insert(node.left, value)
                
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
                self.size += 1
            else:
                self.helper_insert(node.right, value)
        
        return node
        
    def __len__(self):
        return self.size
    
    def is_empty(self):
        return self.size == 0
    
    
    def remove(self, value):
        def _remove(node , value):
            #case 1: node not exsit.
            if node is None:
                return None
            if value < node.value:
                node.left = _remove(node.left, value)
            elif value > node.value:
                node.right = _remove(node.right, value)
            else:
                # case 2: node found and no left child (can be ca leaf or have a right child)
                self.size -= 1
                if node.left is None:
                    return node.right
                # case 2: node found and no right child (can be ca leaf or have a left child)
                if node.right is None:
                    return node.left
                
                #case 3: node found and has 2 children.
                min_larger_node = self._find_min(node.right)
                node.value = min_larger_node.value
                node.right = _remove(node.right, min_larger_node.value)
            return node

        self.root = _remove(self.root, value)
                
        
    def _find_min(self, node): 
        while node.left is not None:
            node = node.left
        return node           
            


    def find(self, value):
        def _find(node, value):
            if node is None:
                return False
            
            if value < node.value:
                return _find(node.left, value)
            elif value > node.value:
                return _find(node.right, value)
            else:
                return True
        
        return _find(self.root, value)
    
    
    def inorder(self):
        def _inorder(node):
            if node is not None:
                yield from _inorder(node.left)
                yield node.value
                yield from _inorder(node.right)
            
            
        yield from _inorder(self.root)
            
            
    def preorder(self):
        def _preorder(node):
            if node is not None:
                yield node.value
                yield from _preorder(node.left)
                yield from _preorder(node.right)
            
            
        yield from _preorder(self.root)
        
        
        
    def postorder(self):
        def _postorder(node):
            if node is not None:
                yield from _postorder(node.left)
                yield from _postorder(node.right)
                yield node.value
            
            
        yield from _postorder(self.root)




    def __iter__(self):
        yield from self.inorder()

    
bst = BST()
bst.insert(10)
bst.insert(5)
bst.insert(15)
bst.insert(3)

print("Tree size:", len(bst))
print("In-order traversal:", list(bst.inorder()))
print("Pre-order traversal:", list(bst.preorder()))
print("Post-order traversal:", list(bst.postorder()))
print("Find 5:", bst.find(5))
print("Find 20:", bst.find(20))

bst.remove(5)
print("Tree size after removing 5:", len(bst))
print("In-order traversal after removing 5:", list(bst.inorder()))