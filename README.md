# twitter-unfollow-tool

Twitterの非相互フォローを自動で検出・解除できるPythonライブラリです。

---

## 🔧 機能一覧

- Twitterのフォロー中・フォロワーを自動で取得
- 非相互フォロー（フォロー返しされていない相手）を抽出
- CSVに保存
- CSVに基づいた自動アンフォロー処理
- アカウントBANの可能性を限りなく0に近くした設計
- 今後も機能の追加の可能性があります

---

## 📦 インストール方法

```bash
pip install twitter-unfollow-tool
```

---

## ⚠️ 注意事項

- Twitterに**ログイン済みのプロファイル**を使ってください  
- **EdgeやChromeのすべてのウィンドウを閉じてから実行**してください（ユーザーデータがロックされるため）  
- TwitterのUI変更により、今後動作しなくなる可能性があります  
- バグ報告は **blackokayu@yahoo.co.jp** までお願いします  

---

## 🚀 使用例

```python
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

# Edgeのログイン済みプロフィールを起動（ChromeでもOK）
options = Options()
options.add_argument("user-data-dir=C:/Users/your_name/AppData/Local/Microsoft/Edge/User Data")
options.add_argument("profile-directory=Default")
driver = webdriver.Edge(options=options)

driver.get("https://twitter.com/your_username")
input("▶ ページが開いたら Enter を押してください...")

# フォロー中・フォロワー一覧を取得
scroll_until_loaded(driver, mode="following")
followings = get_followings(driver)

scroll_until_loaded(driver, mode="followers")
followers = get_followers(driver)

# 非相互を抽出しCSV保存
non_mutuals = get_non_mutuals(followings, followers)
save_usernames_to_csv(non_mutuals, "non_mutuals.csv", limit=30)

# CSVから読み込み、自動でアンフォロー
usernames = load_usernames_from_csv("non_mutuals.csv")
unfollow_users(driver, usernames, max_unfollow=10)

driver.quit()
```

---

## 📄 ライセンス

MIT License

