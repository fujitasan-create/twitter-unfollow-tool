from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_follow_link(driver: WebDriver, mode="following") -> bool:
    wait = WebDriverWait(driver, 10)

    if mode == "following":
        href_part = "/following"
    elif mode == "followers":
        href_part = "/followers"
    else:
        raise ValueError("mode must be 'following' or 'followers'")

    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[contains(@href, "{href_part}")]')))
        driver.execute_script("window.scrollBy(0, 200);")
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", button)  # ← 最後の手段
        print(f"✅ {mode} のリンクをクリックしました")
        return True
    except Exception as e:
        print(f"⚠️ '{mode}' のリンクがクリックできませんでした: {e}")
        return False


def scroll_until_loaded(driver: WebDriver, mode="following", scroll_pause=1.0, max_scrolls=100):
    wait = WebDriverWait(driver, 10)

    if not click_follow_link(driver, mode):
        return

    try:
        modal = wait.until(EC.presence_of_element_located((
            By.XPATH, '//div[@aria-label="Timeline: Followers" or @aria-label="Timeline: Following"]'
        )))
    except:
        print("⚠️ モーダルが開かれませんでした")
        return

    prev_usernames = set()
    same_count = 0

    for i in range(max_scrolls):
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", modal)
        time.sleep(scroll_pause)

        usernames = set()
        try:
            # 新しいセレクタでユーザーID（@xxxx）を取得
            elements = modal.find_elements(By.XPATH, './/div[@dir="ltr"]/span[starts-with(text(), "@")]')
            print(f"🧪 検出ユーザー数（{i+1}回目）: {len(elements)}")
            for el in elements:
                username = el.text.strip()
                usernames.add(username)
        except Exception as e:
            print(f"⚠️ ユーザー名の取得でエラー: {e}")
            continue

        # 同じユーザーしかいなければ打ち切り
        if usernames == prev_usernames:
            same_count += 1
        else:
            same_count = 0
            prev_usernames = usernames

        if same_count >= 3:
            print(f"✅ スクロール完了（{i+1}回）")
            break

    print(f"✅ 合計ユーザー数: {len(usernames)}")
    return usernames
