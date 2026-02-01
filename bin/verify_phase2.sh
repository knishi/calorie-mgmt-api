#!/bin/bash
# Phase 2 動作確認用スクリプト

API_URL="http://localhost:8080/v1"
AUTH_HEADER="X-Auth-Token: SECRET_TOKEN"
JSON_HEADER="Content-Type: application/json"

echo "=== 1. プロフィールの登録 ==="
curl -X POST "$API_URL/profile" \
     -H "$AUTH_HEADER" -H "$JSON_HEADER" \
     -d '{
       "gender": "male",
       "age": 30,
       "height": 175,
       "weight": 80,
       "activity_level": 1.375
     }'
echo -e "\n"

echo "=== 2. 目標設定（10日後に75kg） ==="
# 10日後の日付を算出 (Mac/Linux互換性を考慮)
TARGET_DATE=$(date -v+10d +%Y-%m-%d 2>/dev/null || date -d "+10 days" +%Y-%m-%d)
curl -X POST "$API_URL/goals" \
     -H "$AUTH_HEADER" -H "$JSON_HEADER" \
     -d "{
       \"target_weight\": 75,
       \"target_date\": \"$TARGET_DATE\"
     }"
echo -e "\n"

echo "=== 3. 食事の記録 ==="
curl -X POST "$API_URL/meals" \
     -H "$AUTH_HEADER" -H "$JSON_HEADER" \
     -d '{
       "food_name": "カレーライス",
       "calories": 850
     }'
echo -e "\n"

echo "=== 4. サマリーの確認 ==="
curl -X GET "$API_URL/summary" \
     -H "$AUTH_HEADER"
echo -e "\n"
