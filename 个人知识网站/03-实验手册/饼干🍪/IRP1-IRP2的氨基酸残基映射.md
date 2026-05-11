## IRP1-IRP2的氨基酸残基映射

#### 更新时间：2026年2月1日

````
### 0）加载与清理水（如果不需要水分子可以跳过）

```pymol
reinitialize
load hand_clean_IRP1.pdb, cplx
load IRP2.pdb, irp2

# 可选：去水，确保清理掉水分子
remove cplx and solvent
remove cplx and resn HOH
```

---

### 1）将复合物中的 IRP1 和 IRE 分开成选择集

```pymol
# 选择 IRP1
select irp1, cplx and polymer.protein

# 选择 IRE (RNA)
select ire, cplx and polymer.nucleic
```

确认是否能看到 RNA：

```pymol
show sticks, ire
```

---

### 2）IRP1 对齐到 IRP2（只用 CA 对齐）

```pymol
# 用 CA 原子对齐 IRP1 和 IRP2
align irp1 and name CA, irp2 and name CA
```

这一步会通过 CA 原子对齐 IRP1 和 IRP2，生成最佳的空间匹配。

---

### 3）找 IRP1 上“直接接触 IRE”的残基

根据你的目标，3.5 Å 是“接触”距离的标准，而 4.5 Å 是更广泛的界面残基。你可以先使用 4.0 Å 作为折中值来筛选接触残基：

```pymol
# 选择 IRP1 上与 IRE 相接触的残基，接触范围 4 Å
select irp1_iface, byres (irp1 within 4.0 of ire)
```

自检一下残基数量，确保符合预期：

```pymol
count_atoms irp1_iface and name CA
```

如果你希望查看更多细节（例如如何标记），可以对接触残基做进一步的显示：

```pymol
show sticks, irp1_iface
color yellow, irp1_iface
```

---

### 4）将 IRP1 的接触残基投射到 IRP2 上

投射到 IRP2 的口袋区域，你可以选择一个合理的阈值，比如 5 Å 或 6 Å，来找到 IRP2 中可能与 IRP1 接触的残基。你可以试试 5 Å 作为默认值，来更精确地限制口袋区域：

```pymol
# 选择 IRP2 中与 IRP1 接触的残基，接触范围 5 Å
select irp2_pocket, byres (irp2 within 5.0 of irp1_iface)

# 查看 IRP2 中的接触残基数量
count_atoms irp2_pocket and name CA
```

---

### 5）显示、上色、标注，以便于分析

通过可视化，让你一眼看到口袋的位置与接触残基。你可以使用不同的颜色区分 IRP1、IRE 和 IRP2，以及其相互作用的区域。

```pymol
# 隐藏其他元素，只显示所需部分
hide everything
show cartoon, irp2
show cartoon, irp1
show sticks, ire

# 上色区分
color cyan, irp2  # IRP2 为青色
color green, irp1  # IRP1 为绿色
color yellow, irp1_iface  # IRP1 接触 IRE 的残基为黄色
color magenta, irp2_pocket  # IRP2 接触 IRP1 的口袋为品红色

# 标签显示，显示 CA 原子的标签
set label_size, 16
set label_color, white
label irp2_pocket and name CA, "%s%s" % (resn,resi)
```

这会使你在 PyMOL 中看到 IRP2 的接触口袋与 IRP1 的接触残基，并且能清晰地标注出来。

---

### 6）保存结果（可选）

如果你需要保存这些结果，建议导出为 `.pse` 格式以保存 PyMOL 状态，或者导出为 `.pdb` 格式以便进一步分析：

```pymol
# 保存 PyMOL 会话文件
save IRP2_IRE_mapping.pse

# 保存投射到 IRP2 上的接触残基（IRP2 口袋）
save IRP2_pocket_residues.pdb, irp2_pocket
```

---

## 备注：

1. **检查对接残基的合理性**：可以根据实验数据进一步验证是否接触到关注的残基区域。如果得到的投射残基较多，可以适当调整阈值（比如改成 4.0 或 6.0 Å）。

2. **手动验证**：对于手动验证（目的3和目的4），你可以通过 PyMOL 输出的列表，再结合已有的文献验证每个残基的功能和相互作用。


````

