from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import csv

def get_usernames_from_current_page(driver: WebDriver) -> list[str]:
    """
    モーダル内のフォロー or フォロワー一覧からユーザーID（@なし）を抽出する。
    """
    modal = driver.find_element(
        By.XPATH, '//div[@aria-label="Timeline: Followers" or @aria-label="Timeline: Following"]'
    )

    # 正しいセレクタでユーザーIDを取得
    elements = modal.find_elements(By.XPATH, './/div[@dir="ltr"]/span[starts-with(text(), "@")]')

    usernames = set()
    for el in elements:
        at_name = el.text.strip()
        if at_name.startswith("@"):
            usernames.add(at_name[1:])  # 「@」を除く

    return list(usernames)


def get_followings(driver: WebDriver) -> list[str]:
    return get_usernames_from_current_page(driver)

def get_followers(driver: WebDriver) -> list[str]:
    return get_usernames_from_current_page(driver)


def get_non_mutuals(followings: list[str], followers: list[str]) -> list[str]:
    return [u for u in followings if u not in followers]


def save_usernames_to_csv(usernames: list[str], filename: str, limit: int = None):
    if limit is not None:
        usernames = usernames[:limit]

    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username"])
        for u in usernames:
            writer.writerow([u])


def load_usernames_from_csv(filename: str) -> list[str]:
    usernames = []
    with open(filename, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            usernames.append(row["username"])
    return usernames
