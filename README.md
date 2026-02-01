# Calorie Management API (カロリー管理サーバー)

本プロジェクトは、標準テンプレート（ゴールドマスター：`apibase`）を継承し、高品質なAPI基盤の上に構築された**カロリー管理システム**です。

## 概要

個人の食事記録、カロリー計算、および日次の目標達成管理を提供します。

## 主な機能

- **食事記録 (Meal Logging)**: 食べたものとカロリーを記録。
- **目標設定 (Goal Setting)**: 1日の摂取カロリー目標を設定。
- **日次レポート (Summary)**: 目標に対する現在の進捗をリアルタイムに集計。
- **標準基盤 (Standard Base)**:
    - 認証: Keystone互換。
    - DB: `oslo.db` (SQLAlchemy)。
    - ログ: `oslo.log`。

## クイックスタート

### 1. 新しいプロジェクトの開始
1. GitHubの「Use this template」ボタンから新しいリポジトリを作成します。
2. ローカルにクローンします。
3. マスター（本リポジトリ）を `upstream` として登録します：
   ```bash
   git remote add upstream https://github.com/knishi/api-server-test.git
   ```

### 2. 起動
```bash
docker compose up --build
```

## ドキュメント一覧

プロジェクトの目的、設計、運用の詳細は、以下のドキュメントに体系化されています。

1.  **[設計詳細 (ARCHITECTURE.md)](docs/ARCHITECTURE.md)**: システム協調図、ディレクトリ構造、DB設計、認証フロー。
2.  **[運用ガイド (OPERATIONS.md)](docs/OPERATIONS.md)**: デプロイ手順、ログ監視、CI/CD、マスター同期。
3.  **[AI開発ガイド (AI_DEVELOPMENT.md)](docs/AI_DEVELOPMENT.md)**: anさん（AI）との協働フロー、TDD、AIプロセスの全体像。
4.  **[日本語解説ガイド (SKILL_GUIDE_JP.md)](docs/SKILL_GUIDE_JP.md)**: AIの思考規約（SKILL.md）の日本語詳細解説。

## 開発ルール（マネージャー・AIエージェント用）

本プロジェクトには、AIエージェントと人間が安全に協働するための「憲法」が定義されています。詳細は [SKILL.md](.agent/skills/api_development/SKILL.md) を確認してください。
