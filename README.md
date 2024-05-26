
# 開発環境設定を指定して実行
```bash
$ python manage.py runserver --settings config.settings.development
```


# デプロイメント
## hostted-runnerの指示に従い実行
https://github.com/biki-cloud/miccle-full-stack-app/settings/actions/runners/new?arch=x64&os=linux

## ずっと起動し続ける設定
$ nohup ./run.sh &

[GitHub Actionsのセルフホステッドランナーを構築する #GitHub - Qiita](https://qiita.com/h_tyokinuhata/items/7a9297f75d0513572f4a)