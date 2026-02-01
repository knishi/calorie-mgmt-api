# API Reference - Calorie Management

## 0. Meals API (Phase 1 実装済み)

### POST /v1/meals
食べたものを登録します。

**Request Body**:
```json
{
  "food_name": "りんご",
  "calories": 95
}
```

**Response (201 Created)**:
```json
{
  "id": 1,
  "food_name": "りんご",
  "calories": 95,
  "consumed_at": "2026-02-01T15:06:00Z",
  "user_id": "default-user"
}
```

---

## 1. User Profile API

### GET /v1/profile
現在のユーザープロファイルを取得します。

**Response (200 OK)**:
```json
{
  "user_id": "user-uuid",
  "gender": "male",
  "age": 30,
  "height": 175,
  "weight": 70,
  "activity_level": 1.375
}
```

### POST /v1/profile
プロファイルを新規作成または更新します。

**Request Body**:
Same as Response above.

---

## 2. Goals API

### GET /v1/goals
現在の目標設定と、算出された1日の目標カロリーを取得します。

**Response (200 OK)**:
```json
{
  "target_weight": 65,
  "target_date": "2026-03-01",
  "daily_calories": 1850
}
```

### POST /v1/goals
目標を登録し、目標カロリーを自動算出します。

**Request Body**:
```json
{
  "target_weight": 65,
  "target_date": "2026-03-01"
}
```

---

## 3. Summary API

### GET /v1/summary
今日の摂取状況のサマリーを取得します。

**Response (200 OK)**:
```json
{
  "date": "2026-02-01",
  "total_consumed": 1200,
  "daily_goal": 1850,
  "remaining": 650,
  "status": "under_limit"
}
```
