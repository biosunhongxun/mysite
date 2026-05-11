GMX_MMPBSA环境配置与运行

#### 更新时间：2026年5月9日

#### 1. 环境安装

1. 首先安装miniconda3

2. 创建虚拟环境，配置文件如下,把以下文件写入env.yml

   ```
   name:
   channels:
     - conda-forge
     - bioconda
     - defaults
   dependencies:
     - python=3.9
     - ambertools=21.12
     - mpi4py=3.1.3
     - compilers
     - gromacs==2021.3
     - pip
     - pip: 
       - pyqt5==5.15.6
       - gmx-mmpbsa
       - pandas>=1.2.2
       - seaborn>=0.11.2
       - scipy>=1.6.1
       - matplotlib>=3.5.1
       - h5py==3.7.0
   ```

3. 运行命令

   ```
   conda env create -n gmxMMPBSA --file env.yml
   ```

4. 还需要手动安装一个软件：ParmED

   ```
   软件项目地址：https://github.com/Valdes-Tresanco-MS/ParmEd
   #放入虚拟环境下，然后解压缩，安装
   /home/user/miniconda3/envs/gmxMMPBSA/  #自行替换user名称
   unzip ParmEd-master.zip
   cd ParmED-master/
   python -m pip install . -U
   
   #运行以下命令，检查安装是否成功
   gmx_MMPBSA --help
   ```

### 2. 文件准备

```
1，力场文件夹charmm36-jul2022.ff
2，经过优化过的md100.xtc文件，目的是蛋白居中，消除漂移，断裂等问题
#对轨迹进行周期性矫正
gmx trjconv -s md100.tpr -f md100.xtc -o md100_nojump.xtc -pbc nojump -ur compact
0
3. md100.tpr 二进制文件
4.topol.top文件
5.配体的prm itp文件
6.mmpbsa.in文件，文件内容如下：
Sample input file for PB calculation
This input file is meant to show only that gmx_MMPBSA works. Althought,
we tried to used the input files as recommended in the Amber manual,
some parameters have been changed to perform more expensive calculations
in a reasonable amount of time. Feel free to change the parameters 
according to what is better for your system.

&general
sys_name="Prot-Lig-CHARMM",
startframe=1, #始末帧数
endframe=100, #此处设置为100 单纯为了测试流程
interval=2
# In gmx_MMPBSA v1.5.0 we have added a new PB radii set named charmm_radii. 
# This radii set should be used only with systems prepared with CHARMM force fields. 
# Uncomment the line below to use charmm_radii set
PBRadii=5,
/
&pb
# radiopt=0 is recommended which means using radii from the prmtop file for both the PB calculation and for the NP
# calculation
istrng=0.15, fillratio=4.0, radiopt=0
/

```

### 3. 重要转换

```
# 按道理说，以上步骤就完成了运行前准备，但是个人流程还存在一些特殊情况
# 在autodl上进行分子动力学模拟使用的是GROMACS2025版本
# 但是在ubuntu系统按照如上结果配置的是gmxMMPBSA虚拟环境内置2021版的GROMACS，这就造成两个版本的不兼容

#解决方法：
为了减少环境配置造成的麻烦，使用 PDB 代替 TPR
gmx_MMPBSA 在构建拓扑时，受体结构可以使用 PDB 格式。PDB 是通用格式，不存在版本兼容问题。
1 、用你 2025 版的 GROMACS 把 TPR 转为一个 PDB：
# 选 0 (System) 导出
gmx editconf -f md100.tpr -o reference.pdb

2 生成兼容的索引文件
echo "q" | gmx make_ndx -f md100.tpr -o final_index.ndx

```

### 4. 运行命令

```
由于以上置换，采用新的运行命令
conda activate gmxMMPBSA

mpirun -np 8 gmx_MMPBSA MPI -O \
  -i mmpbsa.in \
  -cs reference.pdb \
  -ci final_index.ndx \
  -cg 1 13 \
  -ct md100_nojump.xtc \
  -cp topol.top \
  -o FINAL_RESULTS_MMPBSA.dat \
  -eo FINAL_RESULTS_MMPBSA.csv
```

### 5. 如果运行失败，使用以下临时方案

````
### 1. 清理临时文件（清场）
这是为了防止上次失败的残留文件（尤其是索引和临时拓扑）干扰新的计算。
```bash
rm -rf _GMXMMPBSA_* rm -f FINAL_RESULTS_MMPBSA.* reference.pdb final_index.ndx
```

### 2. 轨迹预处理（核心：三步走）
对于蛋白和小分子复合物，目标是让它们在盒子中心“纹丝不动”，且不发生跨盒破碎。

按顺序执行：
* **Step 1: 解决分子破碎**
    ```bash
    echo "0" | gmx trjconv -f md100_nojump.xtc -s md100.tpr -pbc whole -o complex_whole.xtc
    ```
* **Step 2: 蛋白质居中 + 移除跳跃**
    ```bash
    # 选 1 (Protein) 居中，选 0 (System) 输出
    echo "1 0" | gmx trjconv -f complex_whole.xtc -s md100.tpr -pbc nojump -center -o complex_centered.xtc
    ```
* **Step 3: 旋转平移拟合（消除整体位移）**
    这是最关键的一步，能防止 PB 计算格点因为蛋白质的漂移而产生误差。
    ```bash
    # 选 1 (Protein) 进行拟合，选 0 (System) 输出
    echo "1 0" | gmx trjconv -f complex_centered.xtc -s md100.tpr -fit rot+trans -o complex_final.xtc
    ```

### 3. 切换为 GB 模式（提升鲁棒性）
修改 `mmpbsa.in`，将 `&pb` 部分替换为 `&gb`：
```fortran
&general
  startframe=1, endframe=10000, interval=10,
  PBRadii=2, # 使用 mbondi2 
/
&gb
  igb=2, saltcon=0.150,
/
```
*注：`igb=2` (OBC模型) 是目前公认在蛋白质-小分子体系中表现最稳健的 GB 模型。*

### 4. 重新提交计算
使用新生成的 `complex_final.xtc` 运行：
```bash
mpirun -np 16 gmx_MMPBSA MPI -O \
  -i mmpbsa.in \
  -cs reference.pdb \
  -ci final_index.ndx \
  -cg 1 13 \
  -ct complex_final.xtc \
  -cp topol.top \
  -o FINAL_RESULTS_MMPBSA.dat \
  -eo FINAL_RESULTS_MMPBSA.csv
  -n
```
-n的意思是禁止启用GUI
````

### 参数解读

```
### 一、 参数与文件详解

| 参数 | 对应文件/值 | 含义 |
| :--- | :--- | :--- |
| **`mpirun -np 8`** | `8` | 使用 MPI 并行协议，调用 **8 个 CPU 核心**同时计算，显著缩短时间。 |
| **`-i`** | `mmpbsa.in` | **输入配置文件**：控制计算模型（GB/PB）、帧数（interval）、盐浓度等核心参数。 |
| **`-cs`** | `reference.pdb` | **结构文件**：提供受体和配体的初始坐标。使用 PDB 可避开 GROMACS 版本冲突。 |
| **`-ci`** | `final_index.ndx`| **索引文件**：告诉程序哪一部分是蛋白质，哪一部分是配体。 |
| **`-cg`** | `1 13` | **索引组编号**：对应 `.ndx` 中的组。`1` 通常是 Protein，`13` 是你的配体。 |
| **`-ct`** | `complex_final.xtc`| **轨迹文件**：经过拟合（Fit）和居中处理后的动力学轨迹。 |
| **`-cp`** | `topol.top` | **拓扑文件**：包含分子的力场参数、电荷和质量信息。 |
| **`-O`** | (开屏参数) | **覆盖模式**：如果文件夹中已有同名输出文件，直接覆盖而不报错。 |
| **`-o`** | `... .dat` | **主结果文件**：包含最终的结合能平均值、标准差等汇总统计。 |
| **`-eo`** | `... .csv` | **明细文件**：每一帧的具体能量项（范德华、静电、溶剂化能等）列表。 |

---

### 二、 计算逻辑与数学原理

`gmx_MMPBSA` 遵循 **单轨迹法（Single Trajectory Protocol）**，其计算过程可概括为：

#### 1. 拓扑与结构准备
程序自动从 `topol.top` 中提取出复合物（Complex）、受体（Receptor）和配体（Ligand）的参数，并将其转换为 Amber 能够识别的格式（`prmtop`）。

#### 2. 能量分帧计算
程序将轨迹按 `interval` 抽出的每一帧拆分为三部分：受体、配体、复合物。然后计算以下能量项：
* **$E_{MM}$（分子力学能）**：范德华力（$E_{vdw}$）+ 静电相互作用（$E_{ele}$）。
* **$G_{solv}$（溶剂化自由能）**：极性溶剂化能（$\Delta G_{GB/PB}$）+ 非极性溶剂化能（$\Delta G_{SA}$）。

#### 3. 结合能合并
对于每一帧，根据以下公式计算结合自由能（$\Delta G_{bind}$）：

$$\Delta G_{bind} = \langle G_{complex} \rangle - \langle G_{receptor} \rangle - \langle G_{ligand} \rangle$$

其中，每一项 $G$ 的构成如下：
$$G = E_{vdw} + E_{ele} + G_{GB/PB} + G_{SA} - T \Delta S$$
*(注：默认情况下不计熵变 $-T \Delta S$)*

#### 4. 统计汇总
计算所有抽取帧的平均值（Average）和标准误差（SEM），生成你看到的 `.dat` 报告。

### 三、 简要运行流程图

1.  **解析**：读取参数，检查 `sander` 等工具是否可用。
2.  **转换**：将 GMX 拓扑 $\rightarrow$ Amber 拓扑。
3.  **计算**：8 个核心分工，各算一部分轨迹帧。
4.  **汇总**：收集各核计算结果，消除能量项中的异常值（NaN）。
5.  **输出**：生成结果表格。
```

