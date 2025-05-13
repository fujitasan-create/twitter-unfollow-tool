import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


def unfollow_user(driver: WebDriver, username: str) -> bool:
    """
    指定ユーザーのプロフィールに移動し、フォロー解除を実行する。

    Returns:
        成功時 True、失敗時 False
    """
    try:
        profile_url = f"https://twitter.com/{username}"
        driver.get(profile_url)
        time.sleep(random.uniform(2.0, 3.5))  # ページ読み込み待機（人間っぽく）

        # 「フォロー中」ボタンを探す（英語・日本語対応）
        follow_button = None
        button_candidates = driver.find_elements(By.XPATH, '//span[text()="Following" or text()="フォロー中"]')
        if button_candidates:
            follow_button = button_candidates[0]
            follow_button.click()
        else:
            print(f"[{username}] フォロー中ボタンが見つかりませんでした。")
            return False

        time.sleep(random.uniform(1.0, 2.0))

        # 確認ダイアログの「Unfollow」ボタンを探してクリック
        confirm_button = None
        confirm_candidates = driver.find_elements(By.XPATH, '//span[text()="Unfollow" or text()="フォロー解除"]')
        if confirm_candidates:
            confirm_button = confirm_candidates[0]
            confirm_button.click()
            print(f"[{username}] フォロー解除成功")
            return True
        else:
            print(f"[{username}] 確認ボタンが見つかりませんでした。")
            return False

    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"[{username}] エラー: {e}")
        return False


def unfollow_users(driver: WebDriver, usernames: list[str], max_unfollow: int = None):
    """
    ユーザー一覧を順に処理し、フォロー解除する。
    max_unfollowを指定すれば上限件数まで。
    """
    count = 0
    for username in usernames:
        if max_unfollow is not None and count >= max_unfollow:
            print(f"上限 {max_unfollow} 件に達したため終了します。")
            break

        success = unfollow_user(driver, username)
        if success:
            count += 1

        if count > 0 and count % 10 == 0:
            print(f"🛌 10人解除したので休憩中...（10〜12秒）")
            time.sleep(random.uniform(10.0, 12.0))
        else:
            wait = random.uniform(4.0, 7.0)
            time.sleep(wait)
