# Ignacio Bird Taxidermy — Hugo site

這個目錄是獨立的 Hugo 網站專案。上層的 `pixnet_backup/` 是唯讀來源，不屬於網站建置輸出。

## 匯入文章

從專案上層執行：

```bash
venv/bin/python static/scripts/import_pixnet.py
```

## 本地預覽

```bash
tools/hugo server --source static --buildDrafts
```

## 正式建置

```bash
tools/hugo --source static --destination public --cleanDestinationDir --panicOnWarning
```

產生的網站位於 `static/public/`，不應提交進版本控制。

## 驗證

```bash
venv/bin/python static/scripts/validate_site.py
```

驗證文章數、搜尋索引、RSS、sitemap、404、站內連結、響應式圖片，以及是否意外依賴外部執行資源。
