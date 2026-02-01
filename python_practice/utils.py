"""
ユーティリティ関数モジュール

ゲームで使用するヘルパー関数を定義
学べる概念: モジュール分割、例外処理、型ヒント
"""


def display_welcome() -> None:
    """ウェルカムメッセージを表示する"""
    print("=" * 40)
    print("    数当てゲームへようこそ！")
    print("=" * 40)
    print("\nルール:")
    print("- コンピュータが選んだ数字を当ててください")
    print("- ヒントを頼りに正解を見つけましょう")


def display_result(attempts: int) -> None:
    """結果を表示する"""
    print(f"\n{'*' * 30}")
    print(f"  {attempts}回で正解しました！")

    if attempts == 1:
        message = "すごい！一発正解！"
    elif attempts <= 5:
        message = "素晴らしい！"
    elif attempts <= 10:
        message = "なかなか良いですね！"
    else:
        message = "次はもっと少ない回数で！"

    print(f"  {message}")
    print(f"{'*' * 30}")


def get_valid_input(min_val: int, max_val: int) -> int:
    """有効な数値入力を取得する（例外処理の練習）"""
    while True:
        try:
            guess = int(input(f"\n予想を入力してください ({min_val}-{max_val}): "))
            if min_val <= guess <= max_val:
                return guess
            else:
                print(f"エラー: {min_val}から{max_val}の間で入力してください")
        except ValueError:
            print("エラー: 数字を入力してください")
