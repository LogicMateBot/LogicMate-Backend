from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetJsonSchemaHandler


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetJsonSchemaHandler):
        return {
            "type": "string",
            "format": "ObjectId",
            "description": "MongoDB ObjectId as a 24-char hex string",
        }

    @classmethod
    def validate(cls, v, _info):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            try:
                return ObjectId(v)
            except Exception:
                raise ValueError(f"Invalid ObjectId string: {v}")
        raise TypeError(f"Expected ObjectId or str, got {type(v)}")
