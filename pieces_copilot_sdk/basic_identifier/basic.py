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
	def delete(self):
		pass