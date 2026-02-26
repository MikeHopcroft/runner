from pydantic import BaseModel


class Prompt:
    def __init__(self, message: str):
        self.message = message

def get_missing_fields(obj: BaseModel, path: str = "") -> list[str]:
    errors: list[str] = []
    model_fields = type(obj).model_fields
    for field_name, field_info in model_fields.items():
        field_path = f"{path}.{field_name}" if path else field_name
        value = getattr(obj, field_name)
        if value is None:
            # Check if this None is a "Prompt" field vs legitimately optional
            for meta in field_info.metadata:
                if isinstance(meta, Prompt):
                    errors.append(f"{field_path}: {meta.message}")
                    break
        elif isinstance(value, BaseModel):
            errors.extend(get_missing_fields(value, field_path))
    return errors
