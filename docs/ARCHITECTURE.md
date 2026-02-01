# アーキテクチャ詳細

本プロジェクトの内部構造と、各コンポーネントがどのように協調して動作するかを説明します。

## 1. システム協調フロー (Coordination Flow)

本システムは Docker Compose によってオーケストレーションされ、Nginx がリバースプロキシとして、Gunicorn が WSGI サーバーとして機能します。

```mermaid
graph TD
    User((ユーザー/クライアント)) -->|HTTP 3000| GUI[Frontend / Static]
    GUI -->|REST API 8080| Nginx[Nginx Container]
    
    subgraph "Docker Compose Network"
        Nginx -->|Proxy Pass| Gunicorn[Gunicorn / WSGI]
        Gunicorn -->|Load App| App[apibase.app]
        App -->|SQLAlchemy| DB[(Database / SQLite)]
    end
    
    subgraph "Logic Layer"
        App -->|Dispatch| Controllers[Controllers]
        Controllers -->|Access| DBApi[DB API]
        Controllers -->|Calc| Utils[Common Utils]
        DBApi -->|Query| Models[Models]
    end

    style GUI fill:#ffd,stroke:#333,stroke-width:2px
    style App fill:#f9f,stroke:#333,stroke-width:2px
    style Nginx fill:#bbf,stroke:#333,stroke-width:2px
    style Gunicorn fill:#dfd,stroke:#333,stroke-width:2px
```

## 2. ディレクトリ構造

```text
├── etc/                   # 設定ファイル類
│   ├── apibase/
│   │   └── config.py      # アプリケーション設定 (Pecan config)
│   └── nginx/
├── build/                 # ビルド・デプロイ関連ファイル
├── bin/                   # 運用補助スクリプト (manage.sh 等)
├── public/                # 疎結合なGUIアセット (index.html, JS, CSS)
├── apibase/               # アプリケーション・パッケージ
│   ├── app.py             # WSGIエントリポイント
│   ├── api/               # Webレイヤー (Controllers)
│   ├── common/            # 共通ユーティリティ (計算ロジック等)
│   ├── db/                # DBレイヤー (Models, API)
│   └── ...
├── pyproject.toml         # プロジェクトメタデータ・設定集約
└── docker-compose.yml     # コンテナオーケストレーション
```

## 3. 認証フロー

1. クライアントが `X-Auth-Token` を付けてリクエスト。
2. `FakeAuthMiddleware` がトークンを検証（現在は模倣実装）。
3. 検証成功時、`X-User-Id` などのヘッダーを付与して後続へ渡す。
4. アプリ側は、既に認証されたものとしてヘッダーから情報を取得。

## 4. エラーハンドリング (Global Error Hook)

- 開発者は、コントローラー内で `raise exception.ItemNotFound()` のように例外を投げるだけでOK。
- `ErrorHook` が自動的に捕捉し、以下のフォーマットでクライアントに返却します。
  ```json
  {"error": {"code": 404, "message": "Item not found"}}
  ```

## 5. データベース管理

- `oslo.db` を利用し、トランザクション管理やコネクションプールを最適化しています。
- 設定ファイル (`etc/apibase/config.py`) を編集するだけで、SQLite, MySQL, PostgreSQL等へ切り替え可能です。
- **マイグレーション**: `apibase/db/migrations/` 配下の Alembic 定義を使用して、本番環境のスキーマ変更を管理します。
