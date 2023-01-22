from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class BaseRecipe(BaseModel):
    name: str
    author: str
    rating: int | None
    prep_time: float | None
    cook_time: float | None
    ingredients: list[str]
    instructions: list[str] | None

class RecipeNew(BaseRecipe):
    pass

class RecipeInDB(BaseRecipe):
    recipe_id: UUID
    created_at: datetime
    modified_at: datetime

class RecipeOut(RecipeInDB):
    pass