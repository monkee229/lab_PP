from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from models.user import User
from models.property import Property
from models.booking import Booking


class Repository(ABC):
    @abstractmethod
    def create(self, entity: Any) -> None:
        pass

    @abstractmethod
    def read(self, entity_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    def update(self, entity: Any) -> None:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Any]:
        pass


class InMemoryRepository(Repository):
    def __init__(self) -> None:
        self._storage: Dict[str, Any] = {}

    def _get_entity_id(self, entity: Any) -> str:
        if isinstance(entity, User) and hasattr(entity, 'user_id'):
            return entity.user_id
        elif isinstance(entity, Property) and hasattr(entity, 'property_id'):
            return entity.property_id
        elif isinstance(entity, Booking) and hasattr(entity, 'booking_id'):
            return entity.booking_id
        else:
            raise ValueError("Entity must have a valid ID attribute (user_id, property_id, or booking_id)")

    def create(self, entity: Any) -> None:
        entity_id = self._get_entity_id(entity)
        if entity_id in self._storage:
            raise ValueError(f"Entity with ID {entity_id} already exists.")
        self._storage[entity_id] = entity

    def read(self, entity_id: str) -> Optional[Any]:
        return self._storage.get(entity_id)

    def update(self, entity: Any) -> None:
        entity_id = self._get_entity_id(entity)
        if entity_id not in self._storage:
            raise ValueError(f"Entity with ID {entity_id} not found for update.")
        self._storage[entity_id] = entity

    def delete(self, entity_id: str) -> None:
        if entity_id in self._storage:
            del self._storage[entity_id]
        else:
            raise ValueError(f"Entity with ID {entity_id} not found for deletion.")

    def list_all(self) -> List[Any]:
        return list(self._storage.values())