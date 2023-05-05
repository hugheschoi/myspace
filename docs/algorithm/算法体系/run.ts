
function postorderTraversal(root: TreeNode | null): number[] {
    let res:number[] = []
    function traversal (root: TreeNode | null) {
        if (!root) return
        if (root.left) {
            traversal(root.left)
        }
        if (root.right) {
            traversal(root.right)
        }
        res.push(root.val)
    }
    traversal(root)
    return res
};

function postorderTraversal(root: TreeNode | null): number[] {
    let res:number[] = []
    let stack: TreeNode [] = []
    let curr = root
    while (stack.length || curr) {
        if (curr) {
            res.unshift(curr.val)
            stack.push(curr)
            curr = curr.right
        } else {
            let node = stack.pop()
            curr = node.left
        }
    }
    return res
};