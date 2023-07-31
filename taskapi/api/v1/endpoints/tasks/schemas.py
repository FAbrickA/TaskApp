import datetime as dt

from pydantic import BaseModel, ConfigDict, constr, model_validator, RootModel


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # orm_mode = True

    id: int
    title: constr(max_length=100)
    description: constr(max_length=2000) | None = None
    is_done: bool = False
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class AddNewTask(BaseModel):
    title: constr(max_length=100)
    description: constr(max_length=2000) | None = None
    is_done: bool = False


class UpdateTask(BaseModel):
    # use self.model_dump(exclude_unset=True) to get actual data to update

    title: constr(max_length=100) = None
    description: constr(max_length=2000) | None = None
    is_done: bool = None

    @model_validator(mode='after')
    def validate_not_all_is_empty(self):
        if not self.model_fields_set:
            raise ValueError("Empty model")
        return self


class TasksList(RootModel):
    root: list[Task]
