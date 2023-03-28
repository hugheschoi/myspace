// 1. 两数之和  hash
// 3. 无重复字符的最长子串  双指针i为开始的下标，j为当前遍历的下标 最大值就是 j - i + 1，滑动窗口（map存 当前值:下标）
var lengthOfLongestSubstring = function(s) {
  let max = 0, i = 0;
  const map = new Map();
  for (let j = 0; j < s.length;j++) {
      if (map.has(s[j])) {
          i = Math.max(i, map.get(s[j]) + 1)
      }
      max = Math.max(max, j - i + 1)
      map.set(s[j], j)
  }
  return max
};
// 5. 最长回文子串, 动态规划，dp[i][j] = dp[i+1][j-1] && s[i] === s[j], j - i < 2：意即子串是一个长度为0或1的回文串只要判断s[i] === s[j即可
// dp[i][j] = (j - i < 2 || dp[i+1][j-1]) && s[i] === s[j]
// let dp = Array.from(new Array(n),() => new Array(n).fill(0));
var longestPalindrome = function(s) {
  let n = s.length;
  let res = '';
  let dp = Array.from(new Array(n), () => new Array(n).fill(0))
  for (let i = n - 1; i >= 0; i--) {
    for (let j = i; j < n; j++) {
      dp[i][j] = s[i] == s[j] && (j - i < 2 || dp[i+1][j-1]);
      if (dp[i][j] && (j - i + 1 > res.length)) {
        res = s.slice(i, j + 1)
      }
    }
  }
  return res
}
// 7, 整数反转
var reverse = function(x) {
  let now = Math.abs(x).toString().split("").reverse().join("");
  if(x < 0){
      return now <= Math.pow(2,31) ? -now : 0;
  }else{
      return now < Math.pow(2,31) ? now : 0;
  }
};

// 20 有效括号， 栈， 映射关系，等于左边的就存，是右边的就看看弹出的是不是对应上
var isValid = function(s) {
  let stack = []
  const map = {
    '(': ')',
    '{': '}',
    '[': ']'
  }
  for (var i = 0; i < s.length; i++) {
    if (map[s[i]]) {
      stack.push(s[i])
    } else if (s[i] !== map[stack.pop()]) {
      return false
    }
  }
  return true
}
// 2 两数相加
var addTwoNumbers = function(l1, l2) {
  let head = null, tail =null
  let carray = 0
  while(l1 || l2) {
    const n1 = l1 ? l1.val : 0;
    const n2 = l2 ? l2.val : 0;
    const sum = n1 + n2 + carry;
    if (!head) {
      head = tail = new ListNode(sum % 10)
    } else {
      tail.next = new ListNode(sum % 10);
      tail = tail.next
    }
    carry = Math.floor(sum / 10);
    if (l1) {
      l1 = l1.next;
    }
    if (l2) {
        l2 = l2.next;
    }
    if (carry > 0) {
      tail.next = new ListNode(carry);
    }
    return head;
  }
};
// 43 字符串相乘
// 53 最大子序和 dp  dp[i] = Math.max(0, dp[i-1]) + nums[i]
// 给定一个整数数组 nums ，找到一个具有最大和的连续子数组
var maxSubArray = function(nums) {
  /**
   * DP: 
   * 分治 problem(i) = Max(problem(i-1)) + a[i]
   * 状态数组定义 dp[i]
   * dp方程 dp[i] = Math.max(dp[i-1] + nums[i], nums[i])
   */
  let dp = nums
  for (let i = 1; i < nums.length; i++) {
      dp[i] = Math.max(dp[i-1], 0) + nums[i]
  }
  return Math.max.apply(null, dp)
};

// 221

// 322 零钱兑换 dp[i] = Math.min(dp[i], dp[i - coin[j] + 1])
// 55. 跳跃游戏 从后往前贪心, end为最后能够跳到的位置，nums[i] + i >= end 就说明能抬到最后
var canJump = function (nums) {
  if (nums === null) return false
  let end = nums.length - 1
  for (let i = nums.length - 1; i >= 0; i--) {
    if (nums[i] + i >= end) {
      end = i
    }
  }
  return end === 0
};
// 45. 跳跃游戏 II 找到最少次数 从左到右找，找到第一个满足的跳跃的
var jump = function(nums) {
  let end = nums.length - 1
  let count = 0
  while (end > 0) {
      for (let i = 0; i < end; i++) {
          if (nums[i] + i >= end) {
              end = i
              count++
              break
          }
      }
  }
  return count
};
// 9 回文数
// 206. 反转链表
var reverseList = function(head) {
  let prev = null
  while(head) {
      let temp = head.next
      head.next = prev
      prev = head
      head = temp
  }
  return prev
};
// 32. 最长有效括号 栈，放一个-1先，如果是'(' 就是push 下标，如果是')' 如果栈为空 就push ')'，如果不为空。长度为当前下标减栈顶元素
var longestValidParentheses = function(s) {
  let maxans = 0
  let stack = [-1]
  for (let i = 0; i < s.length; i++) {
      if (s[i] === '(') {
          stack.push(i)
      } else {
          stack.pop()
          if (stack.length === 0) {
              stack.push(i)
          } else {
              maxans = Math.max(maxans, i - stack[stack.length - 1])
          }
      }
  }
  return maxans
};
// 344 双指针 或者反转
// 200. 岛屿数量  
var numIslands = function(grid) {
  let sum = 0
  if (grid.length === 0) return sum
  function dfs(i, j, m, n) {
  	if (i < 0 || j < 0 || i > m - 1 || j > n - 1 || grid[i][j] === '0') {
  		return
  	}
  	grid[i][j] = '0'
    dfs(i-1, j, m, n)
    dfs(i, j-1, m, n)
    dfs(i+1, j, m, n)
    dfs(i, j+1, m, n)
  }
  const [m, n] = [grid.length, grid[0].length]
  for (let i = 0; i < m; i++) {
  	for (let j = 0; j < n; j++) {
  		if (grid[i][j] === '1') {
        sum++
  			dfs(i, j, m, n)
  		}
  	}
  }
  return sum
};
// 85. 最大矩形
// 221. 最大正方形 dp(i,j)=min(dp(i−1,j),dp(i−1,j−1),dp(i,j−1))+1
// 70. 爬楼梯 迭代替换、dp
var climbStairs2 = function (n) {
  let res1 = 1
  let res2 = 1
  let sum = res2
  for (let i = 2; i <= n; i++) {
    sum = res1 + res2
    res1 = res2ß
    res2 = sum
  }
  return sum
}
var climbStairs = function(n) {
  let dp = []
  dp[0] = 1
  dp[1] = 1
  for (let i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2]
  }
  return dp[n]
};

// 72. 编辑距离 dp
for(var i = 1;i <= n;++i){
  dp[i][0] = dp[i-1][0] + 1;
}
for(var j = 1;j <= m;++j){
  dp[0][j] = dp[0][j-1] + 1;
}
for(var i = 1;i <= n;++i){
  for(var j = 1;j <= m;++j){
      if(word1[i-1] == word2[j-1]){
          dp[i][j] = dp[i-1][j-1];
      }else{
          dp[i][j] = Math.min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])+1;
      }
  }
}
// 21  合并两个有序链表  递归 l1.next = mergeTwoLists(l1.next, l2);   l2.next = mergeTwoLists(l1, l2.next);
if (l1 == null) {
  return l2;
} else if (l2 == null) {
  return l1;
} else if (l1.val < l2.val) {
  l1.next = mergeTwoLists(l1.next, l2);
  return l1;
} else {
  l2.next = mergeTwoLists(l1, l2.next);
  return l2;
}
// 93. 复原IP地址 递归
// 11. 盛最多水的容器 双指针
// 42. 接雨水 单调栈 单调递减，知道遇到比栈顶大的（此时必有积水），就要出栈加上（补平凹点）
// 739.  每日温度 单调栈 从栈底到栈顶的下标对应的温度列表中的温度依次递减
// 820 字典树，不看
//  37 解数独 递归回溯
// 101. 对称二叉树
function isMirror(t1, t2) {
  if (t1 == null && t2 == null) return true;
          if (t1 == null || t2 == null) return false;
          return (t1.val == t2.val)
              && isMirror(t1.right, t2.left)
              && isMirror(t1.left, t2.right);
}
// 46 全排列 递归
// if (!subres.includes(nums[i])) {
//   subres.push(nums[i])
//   helper(subres.slice(0))
//   subres.pop()
// }
// 14. 最长公共前缀 暴力法或二分查找
let left = 0, right = len(array) - 1
while (left <= right) {
  let mid = (left + right) >> 1
  if (array[mid] === target) { /*find the target*/; return }
  else if (array[mid] < target) left = mid + 1
  else right = mid - 1
}
// 最长上升字序 动态规划 dp[i] = Math.max(dp[i], dp[j] + 1);
// dp[i] = 1;
// for (int j = 0; j < i; j++) {
//     if (nums[i] > nums[j]) {
//         dp[i] = Math.max(dp[i], dp[j] + 1);
//     }
// }
//  x平方根 二分法

if (x === 0 || x === 1) return x
let left = 1, right = x;
while (left <= right) {
  const mid = left + ((right - left) >> 1)
  if (mid * mid === x) {
    return mid
  } else if (mid * mid < x) {
    left = mid + 1
  } else {
    right = mid - 1
  }
}
