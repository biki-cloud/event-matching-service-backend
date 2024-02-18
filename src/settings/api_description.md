## 概要
イベントマッチングサービスを提供するAPIです。

## レスポンスについて
### 原則
- ステータスコードで成功か失敗を判断してください
  - 200: 成功
  - 400: リクエストが不正
  - 401: 認証が必要
  - 403: 認可が必要
  - 404: リソースが見つからない
  - 500: サーバーエラー

### 成功時のレスポンス 
- status code: 200
- body
```
{
    "message": "<APIごとのメッセージ>",
    "data": [<APIごとの対象のリソース>]
}
```

### エラー時のレスポンス
- status code: 200以外
- body
```
{
    "detail": "<エラーの詳細>"
}
```

## API
### Event

You will be able to:

* **Register event** 
* **Read event** 
* **Update event** 
* **Delete eventer** 

### Eventer

You will be able to:

* **Register eventer** 
* **Read eventer** 
* **Update eventer** 
* **Delete eventer** 