"""
数当てゲーム - Python練習プロジェクト

このゲームでは、コンピュータが選んだ数字を当てます。
学べる概念: 関数、条件分岐、ループ、ユーザー入力
"""

import random
from utils import display_welcome, display_result, get_valid_input


def generate_secret_number(min_val: int, max_val: int) -> int:
    """指定範囲内でランダムな数字を生成する"""
    return random.randint(min_val, max_val)


def check_guess(guess: int, secret: int) -> str:
    """予想と正解を比較してヒントを返す"""
    if guess < secret:
        return "もっと大きい数字です！"
    elif guess > secret:
        return "もっと小さい数字です！"
    else:
        return "正解！"


def play_game(min_val: int = 1, max_val: int = 100) -> int:
    """ゲームのメインロジック。試行回数を返す"""
    secret_number = generate_secret_number(min_val, max_val)
    attempts = 0

    print(f"\n{min_val}から{max_val}までの数字を当ててください！")

    while True:
        guess = get_valid_input(min_val, max_val)
        attempts += 1

        result = check_guess(guess, secret_number)
        print(result)

        if guess == secret_number:
            break

    return attempts


def main():
    """メイン関数"""
    display_welcome()

    while True:
        attempts = play_game()
        display_result(attempts)

        play_again = input("\nもう一度プレイしますか？ (y/n): ").lower()
        if play_again != 'y':
            print("遊んでくれてありがとう！")
            break


if __name__ == "__main__":
    main()
