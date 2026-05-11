## LSF_大规模分子对接——快速投递操作实战

#### 更新时间：2026年5月9日

#### 大规模分子对接任务的 LSF 多队列调度实践记录

**项目**：IRP2–IRE 相关小分子虚拟筛选
**平台**：LSF 调度的公共超算平台
**软件**：AutoDock Vina（Python API）
**环境**：conda `vina23`（自行配置的 conda 虚拟环境）

#### 1. 问题与困境

在本课题中，需要对 **11462 个小分子**进行对接计算。
公共超算平台存在以下**现实限制**：

- 单个作业可申请 CPU 核心数有限（如 ≤36 核）
- 高优先级队列（`high`）存在 **host slot / job slot 上限**
- 常规队列（`normal`）排队极长
- 无法一次性申请数百核心完成全部计算

👉 **核心问题**：
如何在不违反平台规则的前提下，**尽可能快地完成大规模分子对接任务**？

#### 2.总体解决思路

> **不要申请一个“大作业”，而是把任务拆成多个“小作业”，
> 并向多个队列并行投递，抢占零散可用资源，通过不断抢占，实现总计算资源的占有*

1. **任务分块（chunking）**
   - 将 11462 个 ligand 拆分为 58 个 chunk
   - 每个 chunk 约 200 个分子
   - 每个 chunk 作为一个独立 LSF 作业
2. **单作业小资源**
   - 每个作业仅申请 **4 CPU 核心**
   - 作业内并行运行 4 个 vina 进程
3. **多队列并行投递**
   - 不依赖单一队列
   - 同一程序、同一参数，投递到不同队列
   - 哪个队列能 RUN 就先跑
4. **结果完全隔离**
   - 每个 chunk 输出到独立目录
   - 可随时重跑单个 chunk，不影响全局

#### 3.目录结构设计

```text
2026_2_3dockingwork/
├── IRP2NEW26.pdbqt
├── config260203autobox.txt
├── dock_chunk_v1.py
├── run_chunk.lsf
├── chunks/
│   ├── chunk_001/
│   ├── chunk_002/
│   └── ...
├── results/
│   ├── chunk_001/
│   │   ├── docking_success.tsv
│   │   ├── docking_failure.tsv
│   │   └── docking_summary.txt
│   └── ...
└── logs/
    ├── vina_70445360.out
    └── vina_70445360.err
```

#### 4.核心 LSF 提交脚本（run_chunk.lsf）

```bash
#!/bin/bash
#BSUB -J vina_IRP2_260203autobox
#BSUB -q high
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o logs/vina_%J.out
#BSUB -e logs/vina_%J.err

set -euo pipefail

WORKDIR="/public/home/hxsun25/mimedb2.0/2026_2_3dockingwork"
cd "$WORKDIR"

RECEPTOR="$WORKDIR/IRP2NEW26.pdbqt"
CONFIG="$WORKDIR/config260203autobox.txt"

: "${CHUNK:?ERROR: CHUNK is not set (e.g. chunk_001)}"
CHUNK_DIR="$WORKDIR/chunks/$CHUNK"

OUTDIR="$WORKDIR/results/$CHUNK"
mkdir -p "$OUTDIR" logs

source /public/home/hxsun25/miniconda3/etc/profile.d/conda.sh
conda activate vina23

echo "CHUNK     : $CHUNK"
echo "CHUNK_DIR : $CHUNK_DIR"
echo "OUTDIR    : $OUTDIR"
echo "VINA      : $(which vina)"
echo "PYTHON    : $(python3 --version)"

python3 dock_chunk_v1.py \
  --chunk_dir "$CHUNK_DIR" \
  --outdir "$OUTDIR" \
  --config "$CONFIG" \
  --receptor "$RECEPTOR" \
  --nproc 4
```

#### 5.单个 chunk 提交示例

```bash
bsub -env "all,CHUNK=chunk_001" < run_chunk.lsf
```

验证方式：

```bash
bjobs -w
tail -n 50 logs/vina_<JOBID>.out
```

#### 6.多队列投递(分散投递 high normal smp 等 队列)

##### high 队列

```bash
for i in $(seq -w 041 050); do
  bsub -q high -env "all,CHUNK=chunk_$i" < run_chunk.lsf
done
```

##### normal 队列

```bash
for i in $(seq -w 012 021); do
  bsub -q normal -env "all,CHUNK=chunk_$i" < run_chunk.lsf
done
```

#####  smp 队列

```bash
for i in $(seq -w 022 040); do
  bsub -q smp -env "all,CHUNK=chunk_$i" < run_chunk.lsf
done
```

##### q2680v2 队列

```bash
for i in $(seq -w 051 058); do
  bsub -q q2680v2 -env "all,CHUNK=chunk_$i" < run_chunk.lsf
done
```

#### 7.进度监控命令

##### 已完成 chunk 数量（最准）

```bash
find results -maxdepth 2 -name docking_summary.txt | wc -l
```

##### 查看正在 RUN 的作业

```bash
bjobs -w | awk 'NR==1 || $3=="RUN"'
```

