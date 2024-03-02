from typing import Callable, Union
from typing import List
from pynamodb.exceptions import DoesNotExist
from src.model.eventer_model import (
    EventerModel,
    EventerPynamoModel,
    get_eventer_model_from_eventer_pynamo_model,
    get_eventer_pynamo_model_from_eventer_model
)


class EventerRepository:
    def __init__(self, model_get_func: Callable) -> None:
        self.__model: EventerPynamoModel = model_get_func()

    def get_all_eventers(self) -> List[EventerModel]:
        try:
            pynamodb_eventers = list(self.__model.scan())
        except DoesNotExist:
            # テーブルが存在しない場合、空のリストを返す
            return []
        
        eventers = []
        for pynamodb_eventer in pynamodb_eventers:
            res = get_eventer_model_from_eventer_pynamo_model(pynamodb_eventer)
            eventers.append(res)
        
        return eventers

    def get_eventer(self, id: str) -> EventerModel:
        try:
            # 指定されたIDでアイテムを取得
            eventer = self.__model.get(hash_key=id)
            # アイテムの属性を辞書に変換
            res = get_eventer_model_from_eventer_pynamo_model(eventer)
            return res
        except DoesNotExist:
            # アイテムが見つからない場合の処理
            raise ValueError(f"Eventer with id '{id}' not found")

    
    def register_eventer(self, eventer: EventerModel) -> EventerModel:
        # PynamoDBモデルのインスタンスを作成
        new_eventer = get_eventer_pynamo_model_from_eventer_model(eventer)
        # DynamoDBに保存
        new_eventer.save()

        # 保存されたアイテムの属性を辞書形式で返す
        return eventer

    def update_eventer(self, eventer: EventerModel) -> EventerModel:
        try:
            # まずIDに基づいてアイテムを取得
            eventer_item = self.__model.get(hash_key=str(eventer.id))

            # アイテムの属性を更新
            eventer_item.update(actions=[
                self.__model.info.set(eventer.info),
                self.__model.account_id.set(str(eventer.account_id))
            ])

            return get_eventer_model_from_eventer_pynamo_model(eventer_item)
        except DoesNotExist:
            # アイテムが存在しない場合のエラー処理
            raise ValueError(f"Eventer with id {eventer.id} does not exist")
        except Exception as e:
            # その他のエラー処理
            raise ValueError(f"An error occurred: {e}")

    def delete_eventer(self, id: str) -> bool:
        try:
            eventer = self.__model.get(hash_key=id)
            eventer.delete()
            return True
        except DoesNotExist:
            raise ValueError(f"Eventer with id {id} does not exist")
