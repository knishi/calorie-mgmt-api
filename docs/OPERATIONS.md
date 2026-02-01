# 運用・デプロイガイド

本プロジェクトのデプロイ、ログ監視、およびマスターとの同期方法について説明します。

## 1. ログ監視

`oslo.log` を使用しており、標準出力およびログファイルに出力されます。

- **相関ID (Correlation ID)**: リクエストごとにユニークなIDが付与され、複数の処理をまたいで追跡可能です。
- **ログレベルの変更**: `config.py` または起動引数で `debug = true` に設定することで、詳細なデバッグログが出力されます。

## 2. Dockerによる実行

### ビルドと起動
```bash
docker compose up -d --build
```

### ログの確認
```bash
docker compose logs -f
```

## 3. ローカル環境での直接実行 (非Docker)

開発・検証目的で Docker を介さずに実行する場合の手順です。

### 準備
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:.
```

### APIサーバーの起動 (Port 8080)
```bash
gunicorn --bind 0.0.0.0:8080 apibase.app:application
```

### GUIサーバーの起動 (Port 3000)
```bash
cd public
python3 -m http.server 3000
```

### 動作検証スクリプト (Phase 2 API)
```bash
./bin/verify_phase2.sh
```

### GUI 自動テスト (E2E)
Playwright を使用してブラウザ操作を自動検証します。テスト実行時に API と Web サーバーが自動でバックグラウンド起動されます。
```bash
# ヘッドレスモード（通常）
pytest tests/test_gui.py

# ブラウザを表示して実行（デバッグ用）
pytest tests/test_gui.py --headed
```

## 3. CI/CDパイプライン (GitHub Actions)

GitHubリポジトリにプッシュされると以下のフローが自動実行されます：

1. **テスト段階**: `tox` (pytest) を実行し、全テストの通過を確認。
2. **ビルド段階**: Dockerイメージを構築。
3. **デプロイ段階**: **GitHub Container Registry (GHCR)** へイメージを保存。
   - イメージ名: `ghcr.io/[User]/api-server-test:latest`

## 4. マスターリポジトリとの同期 (ゴールドマスター運用)

本プロジェクトがアップデートされた場合、子プロジェクトで以下のコマンドを実行して最新の基盤を取り込みます。

```bash
# マスター（本家）の更新を取得
git fetch upstream

# 変更をマージ（自分のコードとの衝突は手動で解決）
git merge upstream/main
```

## 5. セキュリティ

- **非root実行**: Dockerコンテナはセキュリティ向上のため、`apibase` という一般ユーザーで実行されます。
- **依存関係の固定**: `pyproject.toml` および `requirements.txt` ですべてのパッケージのバージョンを固定し、予期せぬアップデートによる脆弱性混入を防ぎます。
