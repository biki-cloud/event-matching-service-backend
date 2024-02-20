from typing import Callable, List
from boto3.resources.base import ServiceResource
from typing import List
from pynamodb.exceptions import DoesNotExist
from pynamodb.models import Model
from pynamodb.exceptions import DoesNotExist
from src.model.eventer import EventerModel, EventerPynamoModel, get_eventer_model_from_eventer_pynamo_model




class EventerRepository:
    def __init__(self, model_get_func: Callable) -> None:
        self.__model = model_get_func()

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
        new_eventer = EventerPynamoModel(
            id=eventer.id,
            info=eventer.info,
            account_id=eventer.account_id
        )
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

    def search_eventers(self, eventer_name: str) -> List[EventerModel]:
        # `scan`メソッドを使用して、`eventer_name`が指定された文字列を含むすべてのアイテムを検索します。
        pynamo_eventers = self.__model.scan(self.__model.eventer_name.contains(eventer_name))
        
        eventers = []
        for pynamodb_eventer in pynamo_eventers:
            res = get_eventer_model_from_eventer_pynamo_model(pynamodb_eventer)
            eventers.append(res)
        
        return eventers