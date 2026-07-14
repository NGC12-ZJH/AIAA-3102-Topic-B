## 文件功能详解
- **canonical_table.csv**
  标准化后的基准数据集，统一字段格式，作为模型输入源文件。

- **scripts/01_data_merge.py**
  数据预处理主脚本：多源数据拼接、缺失值填充、特征标准化、数据集划分。

- **scripts/text_utils.py**
  封装通用文本处理函数，供主脚本调用，避免代码冗余。

- **outputs/**
  存放训练日志、可视化图表、预测结果、性能指标等全部输出文件。

- **requirements.txt**
  记录项目用到的所有第三方 Python 库，一键复现运行环境。