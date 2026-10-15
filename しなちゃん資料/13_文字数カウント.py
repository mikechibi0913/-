import sys
import re

def count_chars(text):
    cleaned = re.sub(r'[\s　]', '', text)
    return len(cleaned)

def main():
    if len(sys.argv) < 2:
        text = sys.stdin.read()
        label = "入力テキスト"
    else:
        filepath = sys.argv[1]
        with open(filepath, encoding='utf-8') as f:
            text = f.read()
        label = filepath

    total = count_chars(text)
    # 2026-09-23：目標は「元ネタの純文字数の±10%」（健志さん決定）
    # 使い方：python3 文字数カウント.py ファイル 元ネタの文字数
    # 元ネタの文字数を省略した場合だけ、昔の目安（9,000〜11,000字）を使う
    if len(sys.argv) >= 3:
        base = int(sys.argv[2])
        target_low = int(base * 0.9)
        target_high = int(base * 1.1)
    else:
        target_low = 9000
        target_high = 11000
    diff_low = total - target_low
    diff_high = total - target_high

    print(f"ファイル：{label}")
    print(f"純文字数（空白・改行除外）：{total:,}字")
    print(f"目標レンジ：{target_low:,}字〜{target_high:,}字")

    if target_low <= total <= target_high:
        print("判定：OK（目標レンジ内）")
    elif total < target_low:
        print(f"判定：不足（あと{abs(diff_low):,}字必要）")
    else:
        print(f"判定：超過（{abs(diff_high):,}字オーバー）")

if __name__ == '__main__':
    main()
