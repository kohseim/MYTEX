import re
import os


def replace_punctuation(tex_file, output_file):
    if not os.path.exists(tex_file):
        print(f"警告: {tex_file} が存在しません。処理をスキップします。")
        return None
    encodings = [
        "utf-8",
        "shift-jis",
        "euc-jp",
        "iso-2022-jp",
        "cp932",
        "utf-8-sig",
        "latin1",
    ]
    content = None
    for encoding in encodings:
        try:
            with open(tex_file, "r", encoding=encoding) as f:
                content = f.read()
            print(f"{encoding} でファイルを読み込みました。")
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if content is None:
        print(
            f"警告: {tex_file} のエンコーディングを特定できません。空のファイルとして処理します。"
        )
        content = ""

    content = content.replace("。", ".")  # 。を.に変える
    content = content.replace("、", ",")  # 、を,に変える

    content = re.sub(r"\.(?! )", ". ", content)  # .の後にスペースを追加
    content = re.sub(r",(?! )", ", ", content)  # ,の後にスペースを追加

    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"処理が完了しました。結果は {output_file} に保存されました。")
    except IOError as e:
        print(f"警告: {output_file} に書き込めません。エラー: {e}")
        return content

    return content


if __name__ == "__main__":
    input_file = "/root/tex/ml_math.tex"
    output_file = "/root/tex/ml_math.tex"

    result = replace_punctuation(input_file, output_file)
    if result is not None:
        print("処理が成功しました。")
        if not result:
            print("ただし、入力ファイルは空か読み取り不可でした。")
    else:
        print("処理に失敗しました。")
