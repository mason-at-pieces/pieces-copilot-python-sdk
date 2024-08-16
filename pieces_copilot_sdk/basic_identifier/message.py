from typing import Literal, Optional,TYPE_CHECKING
from pieces_os_client.models.conversation_message import ConversationMessage

if TYPE_CHECKING:
    from ..client import PiecesClient

class BasicMessage:
    """
    A class to represent a basic message in the Pieces client.

    Attributes:
    ----------
    pieces_client : PiecesClient
        An instance of the PiecesClient to interact with the API.
    message_id : str
        The ID of the message to be retrieved.

    Methods:
    -------
    raw:
        Gets or sets the raw content of the message.
    role:
        Gets the role of the message.
    id:
        Gets the ID of the message.
    delete():
        Deletes the message.
    """

    def __init__(self, pieces_client:"PiecesClient", message_id: str) -> None:
        """
        Constructs all the necessary attributes for the BasicMessage object.

        Parameters:
        ----------
        pieces_client : PiecesClient
            An instance of the PiecesClient to interact with the API.
        message_id : str
            The ID of the message to be retrieved.
        """
        try:
            self.message:ConversationMessage = pieces_client.conversation_message_api.message_specific_message_snapshot(
                message=message_id, transferables=True
            )
        except:
            raise ValueError("Error in retrieving the message")
        self.pieces_client = pieces_client

    @property
    def raw(self) -> Optional[str]:
        """
        Gets the raw content of the message.

        Returns:
        -------
        Optional[str]
            The raw content of the message if available, otherwise None.
        """
        try:
            return self.message.fragment.string.raw
        except:
            pass

    @raw.setter
    def raw(self, value: str) -> None:
        """
        Sets the raw content of the message and updates it in the API.

        Parameters:
        ----------
        value : str
            The new raw content of the message.
        """
        self.message.fragment.string.raw = value
        self.pieces_client.conversation_message_api.message_update_value(
            False, self.message
        )

    @property
    def role(self) -> Literal["USER", "SYSTEM", "ASSISTANT"]:
        """
        Gets the role of the message.

        Returns:
        -------
        Literal["USER", "SYSTEM", "ASSISTANT"]
            The role of the message.
        """
        return self.message.role.value

    @property
    def id(self) -> str:
        """
        Gets the ID of the message.

        Returns:
        -------
        str
            The ID of the message.
        """
        return self.message.id

    def delete(self) -> None:
        """
        Deletes the message from the API.
        """
        self.pieces_client.conversation_messages_api.messages_delete_specific_message(
            self.message.id
        )
