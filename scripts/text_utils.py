# scripts/text_utils.py
def normalize_text(raw_text: str) -> str:
    """
    全组统一文本预处理规则：
    1. 全部转为小写
    2. 连续空白字符（空格/换行/tab）折叠为单个空格
    3. 保留 <#> <DECIMAL> 等占位符，不做删除
    """
    text_lower = raw_text.lower()
    text_clean = " ".join(text_lower.split())
    return text_clean