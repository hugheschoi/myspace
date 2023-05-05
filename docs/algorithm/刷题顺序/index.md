# 刷题线路
## 基础
两数之和（简单）
有效的括号（简单）
字符串解码（中等）
LRU 缓存机制（困难）
实现 Trie（前缀树）（中等）
添加与搜索单词 - 数据结构设计（中等）
单词搜索 II （困难）
找不同（简单）
单词规律（简单）
字符串中的第一个唯一字符（简单）
无重复字符的最长子串（中等）
最小覆盖子串（困难）
合并两个有序链表（简单）

```js
var mergeTwoLists = function(l1, l2) {
    if (l1 === null) {
        return l2;
    } else if (l2 === null) {
        return l1;
    } else if (l1.val < l2.val) {
        l1.next = mergeTwoLists(l1.next, l2);
        return l1;
    } else {
        l2.next = mergeTwoLists(l1, l2.next);
        return l2;
    }
};
var mergeTwoLists = function(l1, l2) {
    const prehead = new ListNode(-1);
    let prev = prehead;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) {
            prev.next = l1;
            l1 = l1.next;
        } else {
            prev.next = l2;
            l2 = l2.next;
        }
        prev = prev.next;
    }

    // 合并后 l1 和 l2 最多只有一个还未被合并完，我们直接将链表末尾指向未合并完的链表即可
    prev.next = l1 === null ? l2 : l1;

    return prehead.next;
};
```

```typescript
function mergeTwoLists(l1: ListNode | null, l2: ListNode | null): ListNode | null {
  console.log(l1, l2)
  const prehead = new ListNode(-1)
  let prev = prehead
  console.log(prehead)
  console.log(prev)
  while (l1 !== null && l2 !== null) {
    if (l1.val <= l2.val) {
      prev.next = l1
      l1 = l1.next
    } else {
      prev.next = l2
      l2 = l2.next
    }
    console.log('prev', prev)
    console.log('prehead', prehead)
    prev = prev.next
    console.log('prev', prev)
    console.log('prehead', prehead)
  }
  prev.next = l1 === null ? l2 : l1;
  return prehead.next
};
/*
	[1,2,4] [1,3,4]
  ListNode { val: -1, next: null }
  ListNode { val: -1, next: null }
  prev ListNode { val: -1, next: [1,2,4] }
  prehead ListNode { val: -1, next: [1,2,4] }
  prev [1,2,4]
  prehead ListNode { val: -1, next: [1,2,4] }
  prev [1,1,3,4]
  prehead ListNode { val: -1, next: [1,1,3,4] }
  prev [1,3,4]
  prehead ListNode { val: -1, next: [1,1,3,4] }
  prev [1,2,4]
  prehead ListNode { val: -1, next: [1,1,2,4] }
  prev [2,4]
  prehead ListNode { val: -1, next: [1,1,2,4] }
  prev [2,3,4]
  prehead ListNode { val: -1, next: [1,1,2,3,4] }
  prev [3,4]
  prehead ListNode { val: -1, next: [1,1,2,3,4] }
  prev [3,4]
  prehead ListNode { val: -1, next: [1,1,2,3,4] }
  prev [4]
  prehead ListNode { val: -1, next: [1,1,2,3,4] }
*/
我们可以用迭代的方法来实现上述算法。当 l1 和 l2 都不是空链表时，判断 l1 和 l2 哪一个链表的头节点的值更小，将较小值的节点添加到结果里，当一个节点被添加到结果里之后，将对应链表中的节点向后移一位。

算法

首先，我们设定一个哨兵节点 prehead ，这可以在最后让我们比较容易地返回合并后的链表。我们维护一个 prev 指针，我们需要做的是调整它的 next 指针。然后，我们重复以下过程，直到 l1 或者 l2 指向了 null ：如果 l1 当前节点的值小于等于 l2 ，我们就把 l1 当前的节点接在 prev 节点的后面同时将 l1 指针往后移一位。否则，我们对 l2 做同样的操作。不管我们将哪一个元素接在了后面，我们都需要把 prev 向后移一位。

在循环终止的时候， l1 和 l2 至多有一个是非空的。由于输入的两个链表都是有序的，所以不管哪个链表是非空的，它包含的所有元素都比前面已经合并链表中的所有元素都要大。这意味着我们只需要简单地将非空链表接在合并链表的后面，并返回合并链表即可。
```



环形链表（简单）
环形链表 II （中等）
反转链表（简单）
反转链表 II （中等）
旋转链表（中等）
排序链表
链表中倒数第 k 个节点
两两交换链表中的节点（中等）
按奇偶排序数组（简单）
按奇偶排序数组 II （简单）
有序数组的平方（简单）
山脉数组的峰顶索引（简单）
搜索旋转排序数组（困难）
搜索旋转排序数组 II （中等）
寻找旋转排序数组中的最小值（中等）
寻找旋转排序数组中的最小值 II （困难）
搜索二维矩阵（中等）
等式方程的可满足性（中等）
朋友圈（中等）
账户合并（中等）

## 深度优先搜索
二叉树的最大深度（简单）
路径总和（简单）
路径总和 II （中等）
被围绕的区域（中等）
岛屿数量（中等）
岛屿的最大面积（中等）
在二叉树中分配硬币（中等）
## 回溯
括号生成（中等）
N 皇后（困难）
N 皇后 II （困难）
解数独 （中等）
不同路径 III （困难）
单词搜索（中等）
## 分治
搜索二维矩阵 II （中等）
合并 K 个排序链表（中等）
为运算表达式设计优先级（中等）
给表达式添加运算符（困难）
数组中的第 K 个最大元素（中等）
最接近原点的 K 个点（中等）
鸡蛋掉落（困难）
## 动态规划
使用最小花费爬楼梯（简单）
爬楼梯（简单）
不同路径（简单）
最小路径和 （中等）
最大子序和 （简单）
乘积最大子数组（中等）
买卖股票的最佳时机（简单）
买卖股票的最佳时机 II （简单）
买卖股票的最佳时机 III （困难）
买卖股票的最佳时机 IV （困难）
最佳买卖股票时机含冷冻期（中等）
买卖股票的最佳时机含手续费（中等）
零钱兑换 （中等）
零钱兑换 II （中等）
编辑距离（困难）
不同的子序列（困难）
柱状图中最大的矩形（困难）
最大矩形（困难）
最大正方形（中等）
最低票价（中等）
区域和检索 - 数组不可变（简单）
二维区域和检索 - 矩阵不可变（中等）
最长上升子序列 （中等）
鸡蛋掉落（困难）
