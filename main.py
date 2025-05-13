from selenium import webdriver
from selenium.webdriver.edge.options import Options
from twitter_unfollow_tool import (
    scroll_until_loaded,
    get_followings,
    get_followers,
    get_non_mutuals,
    save_usernames_to_csv,
    load_usernames_from_csv,
    unfollow_users
)

def main():
    # === 設定項目（自分で変更可） ===
    profile_url = "https://twitter.com/study_python_"  # ← 自分のプロフィールURLに変更
    max_save = 30                       # 非相互フォローの保存上限
    max_unfollow = 10                  # 実際に解除する件数の上限
    csv_path = "non_mutuals.csv"       # 保存先CSVファイル名

    # === Edge 起動 + ログイン済みプロファイルを使う ===
    options = Options()
    options.add_argument("user-data-dir=C:/Users/black/AppData/Local/Microsoft/Edge/User Data")
    options.add_argument("profile-directory=Default")
    driver = webdriver.Edge(options=options)
    driver.maximize_window()

    # === 自動で自分のプロフィールページに遷移 ===
    driver.get(profile_url)
    input("▶️ ページが開いたら Enter を押してください...")

    # === フォロー中一覧取得 ===
    print("📥 フォロー中一覧を取得中...")
    scroll_until_loaded(driver, mode="following")
    followings = get_followings(driver)

    # === フォロワー一覧取得 ===
    print("📥 フォロワー一覧を取得中...")
    scroll_until_loaded(driver, mode="followers")
    followers = get_followers(driver)

    # === 非相互を抽出・保存 ===
    non_mutuals = get_non_mutuals(followings, followers)
    print(f"🚫 非相互フォロー数: {len(non_mutuals)}")
    save_usernames_to_csv(non_mutuals, csv_path, limit=max_save)
    print(f"💾 {csv_path} に保存しました（最大 {max_save} 件）")

    # === CSVから読み込み & アンフォロー ===
    print(f"❌ フォロー解除を開始します（最大 {max_unfollow} 件）...")
    usernames = load_usernames_from_csv(csv_path)
    unfollow_users(driver, usernames, max_unfollow=max_unfollow)

    print("✅ 処理完了！お疲れさまでした！")

if __name__ == "__main__":
    main()

