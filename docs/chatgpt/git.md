#### git 查看新分支是从哪拉出来的

要查看 Git 中新分支是从哪里拉出来的，可以使用以下命令：

```bash
git merge-base <branch-name> master
```

将 `<branch-name>` 替换为您想要查找其来源的分支的名称。此命令将返回指定分支和 `master` 分支的最近共同祖先的 SHA-1 校验和。如果该值与当前分支的 SHA-1 校验和相同，则该分支是通过 `master` 分支合并而来。

这个命令会返回一个 SHA-1 值。如果有输出，它将是两个分支共同的祖先的SHA-1哈希。如果没有输出，这意味着它们根本没有公共的祖先，因此可以认为此分支是在空仓库中创建的。 

例如，如果我们想知道名为 `feature-branch` 的分支是如何从 `master` 分支拉出的，我们可以运行以下命令：

```bash
git merge-base feature-branch master
```

如果该命令返回一个 SHA-1 校验和，则说明该分支是通过将 `master` 分支合并到 `feature-branch` 分支所创建的。如果该命令未返回任何结果，则该分支可能是在空仓库中创建的或者是由另一分支合并而来。

#### 查看git commit记录

要查看 Git 仓库中的提交历史记录，您可以使用以下命令：

```bash
git log
```

这将显示最近的提交记录列表。默认情况下，它会按时间顺序显示提交，并显示每个提交的作者、日期和消息。

如果您想要查看更详细的信息，可以使用 `--stat` 选项来显示有关每个提交所做更改的概述：

```bash
git log --stat
```

还可以使用 `-p` 选项来显示与每个提交相关联的差异：

```bash
git log -p
```

如果您只想查看特定分支或标签的提交历史记录，则可以在命令中指定分支或标签的名称：

```bash
git log <branch-name>
```

还可以使用一些其他选项来过滤提交历史记录。例如，您可以在特定日期之后或之前查找提交：

```bash
git log --after="2020-01-01"
git log --before="2021-12-31"
```

上面的命令将显示 2020 年 1 月 1 日以后或 2021 年 12 月 31 日之前的所有提交。

还有许多其他选项可用于自定义 Git 日志输出。您可以查看 Git 的文档以获取更多信息。

#### git 查看分支的上游

要查看 Git 分支的上游，可以使用以下命令：

```bash
git rev-parse --abbrev-ref <branch-name>@{upstream}
```

这会显示给定分支的上游分支名称。上游分支是该分支最后一次拉取更改的来源，也就是它所跟踪的远程分支。

如果您想查看分支跟踪的远程存储库的详细信息，可以使用以下命令：

```bash
git remote show <remote-name>
```

这将显示有关远程存储库的信息，包括跟踪哪些分支以及它们的上游分支。