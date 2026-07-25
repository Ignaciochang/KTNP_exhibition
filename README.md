# KTNP Exhibition

Ignacio Bird Taxidermy 的 Hugo 靜態網站，部署至 GitHub Pages。

- 網站來源：`static/`
- GitHub Actions：`.github/workflows/hugo.yaml`
- 正式網址：<https://ignaciochang.github.io/KTNP_exhibition/>

`pixnet_backup/` 是本機原始備份，不包含在此 repository。

## 本地預覽

安裝 Hugo Extended 0.164.0 後：

```bash
hugo server --source static
```

## 建置

```bash
hugo \
  --source static \
  --destination public \
  --cleanDestinationDir \
  --minify \
  --panicOnWarning
```

推送到 `main` 後，GitHub Actions 會自動建置並部署 GitHub Pages。

## Disqus

留言元件已經預留，但預設不載入。取得 Disqus shortname 後，在
`static/hugo.yaml` 設定：

```yaml
params:
  disqusShortname: "your-shortname"
```

訪客必須點擊「載入留言」後，網站才會連線到 Disqus。
