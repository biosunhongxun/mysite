# AlphaFold 3 蛋白质复合物结构预测教程

## 1.蛋白质折叠：从物理佯谬到信息重构

#### 1.1 赌约与佯谬 (1972)

1972年，斯德哥尔摩。克里斯蒂安·安芬森（Christian Anfinsen）在诺贝尔奖台上留下了结构生物学的“圣经”：**蛋白质折叠的全部信息，已编码在其一维氨基酸序列中。**

这听起来像是一个胜券在握的赌约，但物理学家列文索尔（Cyrus Levinthal）随即抛出了冷酷的数学事实：一个普通蛋白质若通过随机尝试来寻找最低能量构象，所需时间将超过宇宙寿命。

**这就是“列文索尔佯谬”：** 大自然在毫秒级内完成的优雅动作，在经典计算物理面前却是一个无解的死循环。

#### 1.2 苦行僧时代

为了破解这本“魔法书”，人类开始了长达五十年的苦行。

- **X射线晶体学：** 科学家像是在祈求神迹，耗时数年“诱骗”蛋白质长成规则晶体。
- **冷冻电镜：** 在几万分之一秒内捕捉分子的瞬间定格。

每一个原子坐标的确定，往往意味着数十万美元的投入和一名博士生数年的青春。此时，基因测序技术的爆发让序列数据呈指数级增长，但已知的结构数据却像沙漏般缓慢滴落。**序列与结构之间的鸿沟，成为了生物学最大的暗区。**

#### 1.3 进化的“密信” (1994-2010)

转机并非来自算力的暴力破解，而是来自对进化痕迹的重新审视。

1994年，CASP（蛋白质结构预测关键评估）竞赛成立。在前二十年的黑暗探索中，科学家们翻开了大自然的“草稿本”——**多序列比对（MSA）**。

他们发现：如果蛋白质上两个位点在空间上相邻，当其中一个发生突变，另一个往往会发生**协同突变**以维持结构稳定。这就像一对跨越亿万年的舞伴，舞步始终耦合。

**人类猛然醒悟：我们不需要算透复杂的物理力场，大自然早已在物种演化的序列遗迹中，标示出了折叠的“坐标点”。**

#### 1.4 硅基智能的接力 (2016-2020)

当生物学家试图手动解析这些耦合点时，深度学习飓风席卷而来。

- **战术飞跃：** 科学家不再直接预测三维坐标，而是利用深度残差网络（ResNet）处理“残基接触图”。这本质上是将结构问题转化为了图像识别问题。
- **捕风者的入场：** 2016年，刚在围棋界封神的DeepMind团队转场生命科学。在他们眼中，蛋白质折叠不再是纯粹的物理模拟，而是一个**模式识别**与**信息论**问题。

#### 1.5 时代的破折号

那是AlphaFold 1诞生前最寂静的时刻，也是旧时代结构生物学最后一道防线松动的时刻。一场名为深度学习的飓风，正悄然逼近那座修筑了半个世纪的堡垒。

两年后，2018年的冬天，CASP竞赛的会场上，当DeepMind团队带着名为AlphaFold的程序首次亮出成绩时，全场寂静，随即是雷鸣般的掌声。它以碾压性的优势，将过往数十年的积累与挣扎，化为了一个旧时代的句号，和一个崭新时代的破折号。

从1972年的诺贝尔奖台到DeepMind的算力集群，这场接力赛跑了五十年。**人类终于在物理规律的死胡同里，通过信息技术的后门，窥见了生命的底牌。**

#### 1.6 Alphafold 介绍

**AlphaFold** 是由 [Alphabet](https://en.wikipedia.org/wiki/Alphabet_Inc.) 旗下子公司 DeepMind 开发的人工智能 （AI）程序，用于[预测蛋白质结构 ](https://en.wikipedia.org/wiki/Protein_structure_prediction)。 它采用[深度学习](https://en.wikipedia.org/wiki/Deep_learning)技术设计。

AlphaFold 1 (2018) 在 2018 年 12 月举行的第 13 届[结构预测关键评估 ](https://en.wikipedia.org/wiki/Critical_Assessment_of_Structure_Prediction)(CASP) 中获得了总排名第一。它尤其成功地预测了被竞赛组织者评为最困难的目标的最准确结构，这些目标没有来自具有部分相似序列的[蛋白质的](https://en.wikipedia.org/wiki/Proteins)现有模板结构 。

AlphaFold 2 (2020) 在 2020 年 11 月的 CASP14 竞赛中再次取得佳绩。其准确率远高于其他参赛作品。 在 CASP 的[全局距离测试 ](https://en.wikipedia.org/wiki/Global_distance_test)(GDT) 中，约三分之二的蛋白质的得分超过 90 分。该测试衡量计算预测结构与实验确定结构之间的相似性，100 分代表完全匹配。 [宏基因组](https://en.wikipedia.org/wiki/Metagenomics)数据的加入提高了[多序列比](https://en.wikipedia.org/wiki/Multiple_sequence_alignment)对预测的质量。训练数据的主要来源之一是定制的 Big Fantastic Database，该数据库包含 65,983,866 个蛋白质家族，以多序列比对和[隐马尔可夫模型的](https://en.wikipedia.org/wiki/Hidden_Markov_model)形式呈现，涵盖了来自参考数据库、宏基因组和宏转录组的 2,204,359,010 条蛋白质序列。

AlphaFold 2 在 CASP14 上的结果被形容为“惊人” 和“变革性的”。然而，一些研究人员指出，其三分之一的预测准确率不足，并且它没有揭示[蛋白质折叠](https://en.wikipedia.org/wiki/Protein_folding)问题的潜在机制或规则，而[蛋白质折叠问题](https://en.wikipedia.org/wiki/Protein_folding_problem)至今仍未解决。

尽管如此，这项技术成就仍得到了广泛认可。2021 年 7 月 15 日，AlphaFold 2 论文以提前在线发表的形式发表在 *[《自然》杂志](https://en.wikipedia.org/wiki/Nature_(journal))*上，同时发布的[还有开源软件](https://en.wikipedia.org/wiki/Open-source_software)和一个可搜索的物种[蛋白质组](https://en.wikipedia.org/wiki/Proteome)数据库。截至 2025 年 11 月，该论文已被引用近 43,000 次。

AlphaFold 3 于 2024 年 5 月 8 日发布。它可以预测蛋白质与 [DNA](https://en.wikipedia.org/wiki/DNA) 、 [RNA](https://en.wikipedia.org/wiki/RNA) 、各种[配体](https://en.wikipedia.org/wiki/Ligand_(biochemistry))和[离子](https://en.wikipedia.org/wiki/Ion)形成的复合物的结构。与现有方法相比，这种新的预测方法在蛋白质与其他分子相互作用的准确率方面至少提高了 50%。

[德米斯·哈萨比斯](https://en.wikipedia.org/wiki/Demis_Hassabis)和[约翰·詹珀](https://en.wikipedia.org/wiki/John_M._Jumper)因“蛋白质结构预测”而共同获得 2024 年[诺贝尔化学奖 ](https://en.wikipedia.org/wiki/Nobel_Prize_in_Chemistry)，另一半奖项授予[大卫·贝克 ](https://en.wikipedia.org/wiki/David_Baker_(biochemist))，以表彰其在“计算蛋白质设计”方面的贡献。哈萨比斯和詹珀此前曾因领导 AlphaFold 项目而获得 2023 年诺贝尔[生命科学突破奖](https://en.wikipedia.org/wiki/Breakthrough_Prize_in_Life_Sciences)和[阿尔伯特·拉斯克基础医学研究奖 ](https://en.wikipedia.org/wiki/Albert_Lasker_Award_for_Basic_Medical_Research)。



值得一提的是，字节跳动公司有 Alphafold3的克隆衍生版 地址：https://protenix-server.com/login



### 2. Alphafold3 使用指南

#### 说明：此笔记适合华中农业大学LSF调度系统的超算平台，其它环境请修改脚本

#### 示例目标

```
#假设你想预测一下三种分子构成的复合物结构
① IRP2（Iron-Responsive Element Binding Protein 2）— 蛋白质
② FTH1 基因 5'UTR 中的 IRE 元件（Iron-Responsive Element）— RNA 茎环
③ 橙皮素（3',5,7-三羟基-4'-甲氧基黄烷酮）— 小分子配体

```

#### 2.1申请GPU队列权限

```
AF3 推理步骤必须在 GPU 队列中运行，普通队列无法完成结构预测。
请联系计算平台管理员申请 GPU 队列（gpu）使用权限，否则后续作业会提交失败。
```

#### 2.2 获取各组件序列

```
# IRP2蛋白序列（人类）
访问 UniProt 数据库，检索人类 IRP2（IREB2 基因）：
•	网址：https://www.uniprot.org/uniprotkb/P48200
•	在页面找到 "Sequences" 板块
•	复制完整的氨基酸序列（去掉 > 开头的 FASTA 描述行，只要字母部分）

#FTH1的IRE RNA序列
人类 FTH1（铁蛋白重链）5'UTR 中经典 IRE 茎环序列（约 30 nt）：
GGGCUUCCUGCUUCAACAGUGCUUGACACUUC
RNA 序列使用大写字母：A、U、G、C（不是 T）

#橙皮素的 SMILES 结构式
COc1ccc(C2CC(=O)c3c(O)cc(O)cc3O2)cc1O
可在PubChem搜索橙皮素的英文名或者专业学术名
```

#### 2.3 配置input.json文件

``` 
# input.json 是整个工作流中唯一需要修改的文件。它描述了你要预测的分子体系。下面是三元复合物的完整模板：
{
  "name": "IRP2_FTH_IRE",
  "sequences": [
    {
      "protein": {
        "id": "A",
        "sequence": "在此粘贴 IRP2 完整氨基酸序列"
      }
    },
    {
      "rna": {
        "id": "B",
        "sequence": "GAGUCGUCGGGGUUUCCUGCUUCAACAGUGCUUGGACGGAACCCGGCGCUCGUU"
      }
    }
  ],
  "modelSeeds": [1, 2, 3],
  "dialect": "alphafold3",
  "version": 1
}

# 字段说明
字段	说明
name	任务名称，作为输出文件夹的前缀，可自定义
id	链标识符（"A"、"B"、"C"…），每个分子用不同字母
modelSeeds	随机种子，设置多个（如 [1,2,3]）可生成多组模型供比较
dialect	固定填写 "alphafold3"，不可更改
version	固定填写 1，不可更改
**预测不同种类复合物是修改 sequences**,以下是一个例子：
IRP2 + IRE + 橙皮素（三元复合物）
"sequences": [
  { "protein": { "id": "A", "sequence": "IRP2序列..." } },
  { "rna":     { "id": "B", "sequence": "GGGCUUCCUGCUUCAACAGUGCUUGACACUUC" } },
  { "ligand":  { "id": "C", "smiles": "橙皮素 SIMLES" } }
]
```

#### 2.3 创建工作目录

```
# 建立文件夹并移动输入文件
# 创建工作目录（推荐使用绝对路径）
mkdir /public/home/zhangsan/af3_IRP2_run
# 将 input.json 移入工作目录
mv input.json /public/home/zhangsan/af3_IRP2_run/
# 确认文件存在
ls /public/home/zhangsan/af3_IRP2_run/
```

#### 2.4 作业1-CPU计算

```
# 创建 run_data_af3.sh
#BSUB -J IRP2_IRE
#BSUB -n 16
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -q smp

# 加载 Singularity 环境
module load Singularity/3.7.3

# 执行容器命令
singularity exec \
    --nv \
    --bind /public/home/hxsun25/af3_work/irp2_ire:/af3_run \
    --bind /public/home/software/opt/af3_weights/:/af3_weights \
    --bind /public/home/software/opt/af3_db/:/af3_db \
    $IMAGE/alphafold/3.0.1.sif \
    /alphafold3_venv/bin/python /app/alphafold/run_alphafold.py \
    --json_path=/af3_run/input.json \
    --model_dir=/af3_weights \
    --db_dir=/af3_db \
    --norun_inference \
    --output_dir=/af3_run
    
 **参数说明**
 字段	说明
#BSUB -J	作业名称，可自定义，方便在 bjobs 里识别
#BSUB -n 16	申请 16 个 CPU 核心，用于数据管线阶段的序列比对
#BSUB -q gpu	提交到 GPU 队列（必须，需提前申请权限）
--nv	启用 NVIDIA GPU 支持，AF3 推理必需
--bind 主机:容器	将主机目录挂载到容器内，前半部分填你的绝对路径
$IMAGE	集群预设环境变量，指向 /share/Singularity，无需修改
--json_path	输入文件在容器内的路径，固定为 /af3_run/input.json
--model_dir	模型权重目录，已挂载到 /af3_weights，无需修改
--db_dir	遗传数据库目录，已挂载到 /af3_db，无需修改
--output_dir	结果输出目录，固定为 /af3_run，无需修改

# 提交与监控
# 提交作业
bsub < run_af3.sh

# 查看作业状态（PEND=排队, RUN=运行中, DONE=完成, EXIT=报错）
bjobs

# 实时查看运行日志（把 12345 换成你的作业ID）
tail -f 12345.out

# 查看错误信息
cat 12345.err

  
```

#### 2.5 作业2-GPU计算

```
Q1：为什么要分步计算？
AF3 的两个阶段对资源需求截然不同：数据管线只用 CPU，可以在普通队列大量并行；推理只用 GPU，资源有限。如果你有多个蛋白要预测，分步运行可以大幅提高效率。

# 创建 run_inference.sh
#BSUB -J IRP2_Inference
#BSUB -n 4
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -q gpu

module load Singularity/3.7.3


singularity exec \
    --nv \
    --bind /public/home/hxsun25/af3_work/irp2_ire:/af3_run \
    --bind /public/home/software/opt/af3_weights/:/af3_weights \
    --bind /public/home/software/opt/af3_db/:/af3_db \
    $IMAGE/alphafold/3.0.1.sif \
    /alphafold3_venv/bin/python /app/alphafold/run_alphafold.py \
    --json_path=/af3_run/irp2_fth_ire/irp2_fth_ire_data.json \
    --model_dir=/af3_weights \
    --db_dir=/af3_db \
    --norun_data_pipeline \
    --output_dir=/af3_run

```

#### 2.6结果解读

```
# 文件结构
af3_IRP2_run/
├── input.json                          ← 你的输入文件
├── irp2_ire_apigenin/                  ← 数据管线中间文件
│   └── irp2_ire_apigenin_data.json
└── irp2_ire_apigenin_20250326_120000/  ← 最终结果目录
    ├── irp2_ire_apigenin_model.cif      ← 最优预测结构
    ├── irp2_ire_apigenin_confidences.json
    ├── irp2_ire_apigenin_summary_confidences.json
    ├── ranking_scores.csv               ← 多模型排名
    ├── seed-1_sample-0/
    │   ├── model.cif
    │   └── confidences.json
    ├── seed-1_sample-1/
    ├── seed-1_sample-2/
    └── ...

# 指标解读
字段	说明
pTM	预测 TM 分数，>0.5 表示整体折叠可信，值越大越好（最高 1.0）
ipTM	界面 pTM，>0.6 表示结合界面（蛋白-RNA、蛋白-小分子）预测可信
pLDDT	逐残基置信度，0–100 分，>70 为高置信，<50 需谨慎对待
ranking_score	综合排名分数，AF3 自动选出最优模型放在顶层目录

# 结构可视化
使用pymol或者商业软件薛定谔进行符合结构查看和分析
```
