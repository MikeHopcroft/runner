from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic
from pydantic import BaseModel


type UID = str

class Case(BaseModel):
    uid: UID

CASE = TypeVar('CASE', bound='Case')

class Result(BaseModel, Generic[CASE]):
    uid: UID
    case: CASE
    stages: dict[str, Any]

class Input(BaseModel):
  a: Type1

def process(input: Input[CASE]) -> Result[CASE]:

type Suite = list[CASE]

# class RunLog(BaseModel, Generic[CASE]):
# type RunLogStage = dict[UID, CASE]

class Stage(BaseModel, Generic[CASE]):
    name: str
    cases: dict[UID, CASE]

# class RunLog(BaseModel, Generic[CASE]):
#     suite: list[CASE]
#     stages: dict[str, dict[UID, Any]]


class RunLog(BaseModel, Generic[CASE]):
    results: list[Result]
    # suite: list[CASE]
    # stages: dict[str, dict[UID, Any]]

type Processor = Callable[..., None]

def run(processor: Processor):
  pass
