from types import SimpleNamespace
from typing import List

# Define the MyDocMetaData class
class MyDocMetaData:
    def __init__(self, source: str, is_chunk: bool, id: str, window_ids: List[str]):
        self.source = source
        self.is_chunk = is_chunk
        self.id = id
        self.window_ids = window_ids

    def __repr__(self):
        return (
            f"MyDocMetaData(source={self.source!r}, is_chunk={self.is_chunk}, "
            f"id={self.id!r}, window_ids={self.window_ids!r})"
        )

# Define the MyDoc class
class MyDoc:
    def __init__(self, content: str, metadata: MyDocMetaData):
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        return f"MyDoc(content={self.content!r}, metadata={self.metadata})"
    def to_dict(self):
        """
        Converts the MyDoc object into a dictionary.
        """
        return {
            "content": self.content,
            "metadata": {
                "source": self.metadata.source,
                "is_chunk": self.metadata.is_chunk,
                "id": self.metadata.id,
                "window_ids": self.metadata.window_ids,
            },
        }

# Define the phrases


# Function to create MyDoc objects
def create_docs(phrases: SimpleNamespace) -> List[MyDoc]:
    docs = []
    for i, (key, value) in enumerate(phrases.__dict__.items()):
        metadata = MyDocMetaData(
            source="context", is_chunk=False, id=str(i), window_ids=[]
        )
        docs.append(MyDoc(content=value, metadata=metadata))
    return docs

# Create the MyDoc objects
# my_docs = create_docs(phrases)
import uuid

# Define the maybe_add_ids function
def maybe_add_ids(docs: List[MyDoc]):
    """
    Adds a uuid4 to the 'id' field of the metadata of each MyDoc object
    if the 'id' field is not already set or is empty.
    """
    for doc in docs:
        if not doc.metadata.id or doc.metadata.id.strip() == "":
            doc.metadata.id = str(uuid.uuid4())

# Print the result
# print(my_docs)