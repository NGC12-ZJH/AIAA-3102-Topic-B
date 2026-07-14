import pandas as pd
import os
from text_utils import normalize_text

# ===================== 全局配置路径 =====================
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_SMS_PATH = os.path.join(ROOT_DIR, "data", "SMSSpamCollection")
SPLIT_MANIFEST_PATH = os.path.join(ROOT_DIR, "data", "split_manifest.csv")
OUTPUT_TABLE_PATH = os.path.join(ROOT_DIR, "outputs", "canonical_table.csv")

# 自动创建outputs文件夹（不存在则新建）
os.makedirs(os.path.join(ROOT_DIR, "outputs"), exist_ok=True)

# ===================== 步骤1：读取UCI原始短信文件，生成uci_row_number（从1开始） =====================
def load_raw_sms() -> pd.DataFrame:
    raw_rows = []
    with open(RAW_SMS_PATH, "r", encoding="latin-1") as f:
        for line_idx, line in enumerate(f):
            # uci_row_number = 行号+1，1起始
            uci_row = line_idx + 1
            line = line.rstrip("\n")
            # 制表符分割 label 和 text
            label, text = line.split("\t", maxsplit=1)
            raw_rows.append({
                "uci_row_number": uci_row,
                "label": label,
                "text": text,
                "norm_text": normalize_text(text)  # 提前存归一化文本方便后续探针
            })
    df_raw = pd.DataFrame(raw_rows)
    print(f"原始UCI数据集加载完成，总行数：{len(df_raw)}")
    return df_raw

# ===================== 步骤2：读取划分清单，左连接原始短信数据 =====================
def merge_manifest_and_raw(df_raw: pd.DataFrame) -> pd.DataFrame:
    df_split = pd.read_csv(SPLIT_MANIFEST_PATH)
    print(f"划分清单加载完成，总行数：{len(df_split)}")

    # 左连接：以split_manifest为基准，匹配uci_row_number获取文本与标签
    df_merged = pd.merge(
        left=df_split,
        right=df_raw,
        on="uci_row_number",
        how="left"
    )
    return df_merged

# ===================== 步骤3：数据校验、统计输出 =====================
def data_quality_check(df: pd.DataFrame):
    print("\n===== 数据完整性校验 =====")
    # 1. 总样本量校验（标准应为5574）
    total_samples = len(df)
    print(f"合并后总样本数：{total_samples}，标准预期：5574")
    if total_samples != 5574:
        raise ValueError(f"样本数量异常！当前{total_samples}，必须等于5574")

    # 2. 缺失值检查
    missing_count = df.isna().sum()
    print("\n各字段缺失值数量：")
    print(missing_count)
    if missing_count.sum() > 0:
        raise ValueError("数据存在缺失值，匹配失败，请检查uci_row_number是否对齐")

    # 3. 划分split分布统计
    print("\n===== 数据集划分分布 =====")
    split_dist = df["split"].value_counts()
    print(split_dist)

    # 4. 标签ham/spam类别分布
    print("\n===== 标签类别分布 =====")
    label_dist = df["label"].value_counts()
    print(label_dist)
    ham_num = label_dist["ham"]
    spam_num = label_dist["spam"]
    spam_ratio = spam_num / total_samples
    print(f"垃圾短信占比：{spam_ratio:.2%}")

# ===================== 主执行流程 =====================
if __name__ == "__main__":
    # 1. 加载原始短信
    df_sms = load_raw_sms()
    # 2. 与划分表合并
    df_canonical = merge_manifest_and_raw(df_sms)
    # 3. 执行数据校验
    data_quality_check(df_canonical)

    # 4. 输出标准工作表（只保留题目要求的固定字段）
    output_cols = ["id", "split", "uci_row_number", "text", "label"]
    df_export = df_canonical[output_cols].copy()
    df_export.to_csv(OUTPUT_TABLE_PATH, index=False, encoding="utf-8")
    print(f"\n标准工作表已保存至：{OUTPUT_TABLE_PATH}")
    print("输出字段：id,split,uci_row_number,text,label")