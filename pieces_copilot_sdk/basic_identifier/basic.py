from abc import ABC,abstractmethod
from typing import  Optional
from pieces_os_client import Annotations

class Basic(ABC):
	@property
	def description(self):
		"""
		Retrieve the description.

		:return: The description text or None if not available.
		"""
		annotations = self.annotations
		if not annotations:
			return
		annotations = sorted(annotations, key=lambda x: x.updated.value, reverse=True)
		d = None
		for annotation in annotations:
			if annotation.type == "DESCRIPTION":
				d = annotation
		
		return d.text if d else None

	@property
	@abstractmethod
	def annotations(self)  -> Optional[Annotations]:
		"""
		Get all the annotations.

		Returns:
			Optional[Annotations]: The annotations if available, otherwise None.
		"""
		pass

	@abstractmethod
	def id(self):
		pass

	@abstractmethod
	def name(self):
		pass

	@abstractmethod
	def delete(self):
		pass

	def __repr__(self):
		"""
		Returns a detailed string representation of the object.
		"""
		return f"<{self.__class__.__name__}(id={self.id}, name={self.name})>"

	def __eq__(self, other):
		"""
		Checks equality between two instances.
		"""
		if isinstance(other, self.__class__):
			return self.id == other.id
		return False

	def __str__(self):
		"""
		Returns a user-friendly string representation of the object.
		"""
		return f"ID: {self.id}, Name: {self.name}"


	def __hash__(self):
		"""
		Returns a hash of the instance.
		"""
		return hash(self.id)

