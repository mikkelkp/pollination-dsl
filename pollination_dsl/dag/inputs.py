from typing import Any, Dict, List
from dataclasses import dataclass
from queenbee.io.inputs.dag import (
    DAGGenericInput, DAGStringInput, DAGIntegerInput, DAGNumberInput,
    DAGBooleanInput, DAGFolderInput, DAGFileInput, DAGPathInput,
    DAGJSONObjectInput, DAGArrayInput
)
from queenbee.base.basemodel import BaseModel, Field, validator
from queenbee.io.common import ItemType

from ..alias.inputs import InputAliasTypes


__all__ = ('Inputs', )

_inputs_mapper = {
    'GenericInput': DAGGenericInput,
    'StringInput': DAGStringInput,
    'IntegerInput': DAGIntegerInput,
    'NumberInput': DAGNumberInput,
    'BooleanInput': DAGBooleanInput,
    'FolderInput': DAGFolderInput,
    'FileInput': DAGFileInput,
    'PathInput': DAGPathInput,
    'DictInput': DAGJSONObjectInput,
    'ListInput': DAGArrayInput
}


class _InputBase(BaseModel):

    annotations: Dict = None
    description: str = None
    default: Any = None
    default_local: Any = None
    spec: Dict = None
    alias: List[InputAliasTypes] = None
    optional: bool = False

    @validator('alias', always=True)
    def empty_list_alias(cls, v):
        return v if v is not None else []

    @property
    def __decorator__(self) -> str:
        """Queenbee decorator for inputs."""
        return 'input'

    @property
    def required(self):
        if self.optional:
            return False
        elif self.default is not None:
            return False
        else:
            return True

    def to_queenbee(self, name):
        """Convert this input to a Queenbee input."""
        func = _inputs_mapper[self.__class__.__name__]

        annotations = self.annotations or {}
        if self.default_local:
            annotations['__default_local__'] = self.default_local

        data = {
            'required': self.required,
            'name': name.replace('_', '-'),
            'default': self.default,
            'description': self.description,
            'annotations': annotations,
            'spec': self.spec,
            'alias': [al.to_queenbee().dict() for al in self.alias]
        }

        if hasattr(self, 'extensions'):
            data['extensions'] = self.extensions

        if hasattr(self, 'items_type'):
            data['items_type'] = self.items_type

        return func.parse_obj(data)

    @property
    def is_artifact(self):
        return False

    @property
    def reference_type(self):
        return 'InputReference'


class GenericInput(_InputBase):
    """ A DAG generic input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    ...


class StringInput(GenericInput):
    """ A DAG string input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    default: str = None
    default_local: str = None


class IntegerInput(StringInput):
    """ A DAG integer input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    default: int = None
    default_local: int = None


class NumberInput(StringInput):
    """ A DAG number input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    default: float = None
    default_local: float = None


class BooleanInput(StringInput):
    """ A DAG boolean input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    default: bool = None
    default_local: bool = None


class DictInput(StringInput):
    """ A DAG dictionary input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    default: Dict = None
    default_local: Dict = None


class ListInput(StringInput):
    """ A DAG list input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        items_type: 'Type of items in list. All the items in an array must be from '
        'the same type.'
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    default: List = None
    default_local: List = None

    items_type: ItemType = Field(
        ItemType.String,
        description='Type of items in an array. All the items in an array must be from '
        'the same type.'
    )


class FolderInput(StringInput):
    """ A DAG folder input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    @property
    def is_artifact(self):
        return True

    @property
    def reference_type(self):
        return 'InputFolderReference'


class FileInput(FolderInput):
    """ A DAG file input.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        extensions: An optional list of valid extensions for input file.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """
    extensions: List[str] = None

    @property
    def reference_type(self):
        return 'InputFileReference'


class PathInput(FileInput):
    """ A DAG path input. A path can be a file or a folder.

    Args:
        annotations: An optional annotation dictionary.
        description: Input description.
        default: Default value.
        default_local: Default value for local runs. This value overwrites
            the default value when the recipe is translated for local runs.
        extensions: An optional list of valid extensions for input file.
        spec: A JSONSchema specification to validate input values.
        alias: A list of aliases for this input in different platforms.

    """

    @property
    def reference_type(self):
        return 'InputPathReference'


@dataclass
class Inputs:
    """DAG inputs enumeration."""
    any = GenericInput
    str = StringInput
    int = IntegerInput
    float = NumberInput
    bool = BooleanInput
    file = FileInput
    folder = FolderInput
    path = PathInput
    dict = DictInput
    list = ListInput
