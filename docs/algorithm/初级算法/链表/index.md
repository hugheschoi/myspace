链表的结构，有一个next 的指针指向下一个，还有一个val

```js
 * function ListNode(val) {
 *     this.val = val;
 *     this.next = null;
 * }
```

### 删除

如果要**删除**链表某个节点，可以将这个节点的值变为下一个节点的值，并吧这个节点的next指向 next.next

这样看，值和指针其实都变成了下一个的节点，相当于把这个节点删了

删除链表的节点的本质是：**把这个节点跳过**



### 查找

比如说要查找倒数第 n 个的节点，要怎么做？ - 快慢指针，先走 n 步，然后再一起走，那么快的走到头了，慢的正好在倒数第 n 个。

找第n个。就走 n 步， node = node.next;

链表不像数组，有下标，它只有next指针



### 求链表的长度

递归获取长度，每一层加一，叠加。

```js
//求链表的长度
private int length(ListNode head) {
    if (head == null)
        return 0;
    return length(head.next) + 1;
}
```



### 链表的循环

```js
let curr = head;
while (curr !== null) {
  // 要在循环中做的事情
  curr = curr.next;
}
// 跳出循环了，此时 curr 的 null
```



### 链表的递归

