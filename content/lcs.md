title: 最长共同子序列 (Longest Common SubsequenceLCS)
date: 2020-06-29
author: charles
Tags: python
Slug: lcs
Category: python


### 1. 最长共同子序列 (Longest Common Subsequence; LCS) 
- 给定两个序列，找出两个序列中存在的最长子序列的长度。子序列是指以相同的相对顺序出现，但不一定是连续的序列 称为「**最长共同子序列**」(*Longest Common Subsequence*; LCS)」

- 示例：
序列“ ABCDGH”和“ AEDFHR”的LCS为长度3的“ ADH”。
序列“ AGGTAB”和“ GXTXAYB”的LCS为长度4的“ GTAB”。
#### 解题思路
首先看一个2个字符串abcdefg和cef 要想求2个字符串最后一个位置的LCS，我们需要在下面3中情况中取最大值 如果最后一个字符不相等，则我们在下面两种情况中取一个最大值

第一个字符串取最后一个位置和第二个字符串不取最后一个位置，即abcdefg和ce
第一个字符串不取最后一个位置和第二个字符串取最后一个位置，即abcdef和cef
如果最后一个字符相等，我们只需要把前面的子串的LCS长度（即abcdef和ce）加上最后一个最后一个字符是否相等，相等为1，不等为0。
这里有一个问题就是，为什么当两个字符串最后一个字符相等的时候，我们取了最终就一定可以得到LCS了？ 比如abcd和bdd，
如果我们两个字符串都不取最后一个d，则剩下的串为abc和bd，前面构成的LCS一定比取最后一个少1。
如果我们只取其中一个，则剩下的串有可能为abcd和bd和abc和bdd，这2种情况的LCS最好也是和我们之前结果一样。
<hr>

下面用简单的递归来实现
```
def lcs(X, Y, m, n):
    if m == 0 or n == 0:
        return 0
    elif X[m - 1] == Y[n - 1]:
        return 1 + lcs(X, Y, m - 1, n - 1)
    else:
        return max(lcs(X, Y, m, n - 1), lcs(X, Y, m - 1, n))


X = "AGGTAB"
Y = "GXTXAYB"
print("Length of LCS is ", lcs(X, Y, len(X), len(Y)))
```
考虑到上述实现，以下是针对输入字符串“ AXYT”和“ AYZX”
```
                         lcs（“ AXYT”，“ AYZX”）
                       /              \
         lcs（“ AXY”，“ AYZX”）lcs（“ AXYT”，“ AYZ”）
         /             \           /       \
lcs（“ AX”，“ AYZX”）lcs（“ AXY”，“ AYZ”）lcs（“ AXY”，“ AYZ”）lcs（“ AXYT”，“ AY”）
```

在上面的部分递归树中，lcs（“ AXY”，“ AYZ”）被求解两次。如果我们绘制完整的递归树，则可以看到有很多子问题可以一次又一次地解决。因此，此问题具有“*重叠子结构*”属性，并且可以通过使用“记忆化”或“制表”来避免重新计算相同子问题。以下是LCS问题的列表实现。
<hr>
上述天真的递归方法的时间复杂度在最坏的情况下为O（2 ^ n），最坏的情况发生在X和Y的所有字符不匹配（即LCS的长度为0）时。

```
def lcs(X, Y):
    m = len(X)
    n = len(Y)
    # m,n都加1 确保m/n为空的case
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    print(dp)
    return dp[m][n]

X = "AGGTAB"
Y = "GXTXAYB"
print("Length of LCS is ", lcs(X, Y))
```
上述实现的时间复杂度为O（mn），比递归实现的最坏情况下的时间复杂度好得多。

