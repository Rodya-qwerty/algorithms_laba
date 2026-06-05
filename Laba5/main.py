class TreeNode:
    def __init__(self, value):
        self.value = value      # хранимые данные
        self.left = None        # левый потомок
        self.right = None       # правый потомок

def insert(root, value):
    """Добавить значение в бинарное дерево поиска."""
    if root is None:
        return TreeNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

def search(root, target):
    """Найти значение в дереве поиска."""
    if root is None or root.value == target:
        return root  # None, если не найдено
    if target < root.value:
        return search(root.left, target)
    else:
        return search(root.right, target)
        
def inorder(root, result=None):
    if result is None:
        result = []
    if root:
        inorder(root.left, result)          # 1. левое поддерево
        result.append(root.value)           # 2. узел
        inorder(root.right, result)         # 3. правое поддерево
    return result


if __name__ == "__main__":
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    print(
        inorder(root)
    )
