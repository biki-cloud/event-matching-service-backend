import os


def get_api_description() -> str:
    # このファイルが配置されているディレクトリのapi_description.mdを読み込み返す
    # このディクトりが配置されているパスを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return open(f"{current_dir}/api_description.md", "r").read()

