以下是整理好的 Markdown 笔记，系统介绍了 `.bed/.bim/.fam` 三种文件的来源和转换过程

------

~~~markdown
# 📦 PLINK `.bed` `.bim` `.fam` 文件是怎么来的？

在进行 GWAS（全基因组关联分析）时，最常见的数据格式是 PLINK 的二进制三件套文件：`.bed`、`.bim`、`.fam`。本笔记将介绍这些文件的来源、用途，以及如何从原始数据一步步生成它们。

---

## 🧬 为什么使用 `.bed/.bim/.fam` 三件套？

PLINK 最初使用的是 `.ped` 和 `.map`（文本格式），但当样本和 SNP 数量很大时，`.ped` 文件太大太慢。为此，PLINK 设计了更高效的**二进制格式**：

- `.bed`：二进制存储基因型矩阵（不可读）
- `.bim`：每个 SNP 的注释（文本）
- `.fam`：每个样本的基本信息与表型（文本）

---

## 📂 三件套文件的来源路径

最常见的生成路径如下：

```text
原始基因型数据（VCF / 芯片 / 测序） + 表型信息
           ↓
    转换或整理成 .ped / .map 文件（纯文本格式）
           ↓
      使用 plink --make-bed 命令
           ↓
   生成 .bed + .bim + .fam 三件套（二进制格式）
~~~

------

## 📝 什么是 `.ped` 和 `.map`？

### `.ped` 文件格式（文本）

- 每行一个样本（个体）

- 前 6 列是：

  ```
  FID IID 父母ID 母亲ID 性别 表型
  ```

- 后面是每个位点的两个等位基因（如 A G C T ...）

**示例：**

```
FAM001 IND001 0 0 1 2 A G C C T T
FAM002 IND002 0 0 2 1 G G T T T T
```

### `.map` 文件格式（文本）

- 每行一个 SNP（位点），4 列：

  ```
  染色体 SNP名 遗传距离 物理位置(bp)
  ```

**示例：**

```
1 rs12345 0 1234567
1 rs67890 0 2345678
```

------

## 🔁 `.ped` + `.map` 转换为 `.bed/.bim/.fam`

使用以下命令即可：

```bash
plink --file your_data_prefix --make-bed --out output_prefix
```

参数说明：

- `--file`：输入 `.ped/.map` 文件（不带扩展名）
- `--make-bed`：表示生成二进制文件
- `--out`：输出文件前缀

------

## 🔄 直接从 VCF 文件转换

在现代分析中，我们常用 VCF 格式（如从 GATK 或测序平台得到）作为起点。

```bash
plink --vcf input.vcf --make-bed --out output_prefix
```

还可加上一些筛选参数（如只保留常见变异）：

```bash
plink --vcf input.vcf --maf 0.01 --geno 0.1 --make-bed --out filtered_data
```

------

## 🧰 其他常见来源

| 来源类型                             | 转换工具               | 说明                   |
| ------------------------------------ | ---------------------- | ---------------------- |
| Illumina 芯片数据（如 Final Report） | GenomeStudio → PED/MAP | 导出时指定格式         |
| Affymetrix 芯片数据                  | apt-tools → PED/MAP    | Affymetrix Power Tools |
| GATK/FreeBayes VCF 文件              | PLINK                  | 常规测序输出           |
| STRUCTURE/GENEPOP 格式               | PGDSpider              | 人群遗传格式           |
| 自定义表格                           | 脚本转 PED/MAP         | 用 R / Python 编写     |

------

## 🧪 `.bed/.bim/.fam` 的意义

| 文件   | 内容                                  | 可读性   | 必须配套？ |
| ------ | ------------------------------------- | -------- | ---------- |
| `.bed` | 所有样本的基因型（2-bit编码）         | ❌ 二进制 | ✅ 是       |
| `.bim` | 每个 SNP 的注释（ID、位置、等位基因） | ✅ 文本   | ✅ 是       |
| `.fam` | 每个样本的基本信息（性别/表型）       | ✅ 文本   | ✅ 是       |

------

## 📌 常用命令汇总

### 1. 从 `.ped/.map` → `.bed/.bim/.fam`：

```bash
plink --file data --make-bed --out data_bin
```

### 2. 从 `.vcf` → `.bed/.bim/.fam`：

```bash
plink --vcf data.vcf --make-bed --out data_bin
```

### 3. 查看 `.bim` 或 `.fam` 文件：

```bash
head data.bim
head data.fam
```

------

## 📚 推荐参考

- PLINK 官方文档：https://www.cog-genomics.org/plink/1.9/formats
- GWAS 教程论文（质量控制）：
   [A tutorial on conducting GWAS: QC and analysis](https://www.ncbi.nlm.nih.gov/pubmed/29484742)

------

```
---

### ✅ 后续建议

是否需要我帮你：

- 保存为 `.md` 文件并打包？
- 加入图片说明（如 `.bed` 是怎么编码的）？
- 增加一个 shell 脚本，一键把 VCF 转换为 `.bed`？

你只需要说一声，我可以继续补充完善。
```