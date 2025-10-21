> 🚀 从登录到在 GPU 节点上运行 GROMACS 分子动力学模拟的完整流程。

------

## 🧭 一、总体思路

在多瑙超算（LSF 系统）上跑任务的流程是：

> 登录节点写脚本 → 提交脚本到调度系统 → 系统分配 GPU 节点 → 自动运行任务 → 输出结果文件

**不能直接在命令行运行 GROMACS**，因为登录节点只用于准备和提交。

------

## 🧱 二、运行流程总览（6步）

| 步骤 | 操作内容                     | 说明                      |
| ---- | ---------------------------- | ------------------------- |
| ①    | 登录登录节点                 | 在 `[hxsun25@login03 ~]$` |
| ②    | 编写作业脚本 `.sh`           | 定义资源、队列、命令等    |
| ③    | 提交任务                     | `bsub < run_md.sh`        |
| ④    | 查看任务状态                 | `bjobs`                   |
| ⑤    | 查看输出日志                 | `cat run_md.sh.o*`        |
| ⑥    | 任务结束后下载或继续分析结果 |                           |

------

## 🧩 三、GROMACS GPU 任务脚本模板

请新建脚本：

```bash
vim run_md.sh
```

然后复制下面的完整内容进去：

```bash
#!/bin/bash
#BSUB -J md_run                  # 作业名称
#BSUB -q gpu                     # 提交到 gpu 队列
#BSUB -n 8                       # 请求 8 个CPU线程
#BSUB -gpu "num=1:mode=exclusive_process"  # 申请 1 个GPU
#BSUB -o md_run.o                # 标准输出文件
#BSUB -e md_run.e                # 错误输出文件
#BSUB -W 48:00                   # 预计最大运行时间 48小时
#BSUB -R "rusage[mem=16G]"       # 每个节点使用16G内存

# 进入任务工作目录（自动识别提交时的目录）
cd $LS_SUBCWD

# 加载环境模块（根据系统实际环境修改）
module load gromacs/2022.3

# 输出环境信息
echo "Running on host: $(hostname)"
echo "Start time: $(date)"
echo "Using GPU for GROMACS simulation"

# 执行 GROMACS 模拟命令（根据文件修改）
gmx mdrun -s md.tpr -deffnm md_run -ntmpi 1 -ntomp 8 -gpu_id 0

# 结束
echo "End time: $(date)"
```

保存退出（`Esc` → `:wq` → 回车）。

------

## ⚙️ 四、提交任务

```bash
bsub < run_md.sh
```

会看到类似：

```
Job <64001234> is submitted to queue <gpu>.
```

------

## 🔍 五、查看任务状态

```bash
bjobs
```

常见状态：

| 状态   | 含义               |
| ------ | ------------------ |
| `PEND` | 排队中（等待资源） |
| `RUN`  | 正在运行           |
| `DONE` | 已完成             |
| `EXIT` | 出错退出           |

------

## 📄 六、查看日志结果

```bash
cat md_run.o
cat md_run.e
```

正常运行时，会看到类似：

```
Running on host: gpu01
Start time: Wed Oct 15 15:40:00 CST 2025
Using GPU for GROMACS simulation
...
End time: Wed Oct 15 18:20:00 CST 2025
```

出错时（比如路径或模块问题）会在 `.e` 文件中记录。

------

## 🧠 七、需要准备的输入文件

GROMACS 模拟需要你在当前目录下准备：

| 文件        | 说明                           |
| ----------- | ------------------------------ |
| `md.tpr`    | 由 `gmx grompp` 生成的输入文件 |
| `topol.top` | 拓扑文件                       |
| `md.mdp`    | 模拟参数文件                   |
| `conf.gro`  | 初始结构文件                   |

------

## 📘 八、任务结束后（结果分析）

任务完成后会生成：

```
md_run.trr     # 轨迹文件
md_run.edr     # 能量文件
md_run.log     # 日志
md_run.gro     # 最终结构
```

然后你可以：

- 用 `gmx rms`, `gmx rmsf`, `gmx gyrate` 等命令做分析；
- 或生成轨迹文件`用轨迹生成脚本`到本地用pymol 可视化。

