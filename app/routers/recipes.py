from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter

from ..schemas.recipe import RecipeNew, RecipeInDB, RecipeOut

fake_recipes_db = [
    RecipeInDB(recipe_id=uuid4(), created_at=datetime.now(), modified_at=datetime.now(), name="korean beef", author="Rex Tavington", rating=8, ingredients=["ground beef", "soy sauce", "garlic", "ginger"]),
    RecipeInDB(recipe_id=uuid4(), created_at=datetime.now(), modified_at=datetime.now(), name="mac & cheese", author="Joe", rating=9, ingredients=["macaroni pasta", "cheddar cheese", "pepperjack cheese", "milk"]),
    RecipeInDB(recipe_id=uuid4(), created_at=datetime.now(), modified_at=datetime.now(), name="dan dan noodles", author="oshagshennesy", rating=6, ingredients=["egg noodles", "soy sauce", "chili oil", "ginger", "pork"])
    # {"recipe_id": uuid4(), "name": "korean beef", "author": "Rex Tavington"},
    # {"recipe_id": uuid4(), "name": "mac & cheese", "author": "Joe"},
    # {"recipe_id": uuid4(), "name": "dan dan noodles", "author": "Oshagshennesy"},
     ]

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)

@router.get("/")
async def read_recipes():
    #face_recipes_out = [RecipeOut(**x.dict() for x in len(fake_recipes_db))]
    fake_recipes_out: [RecipeOut] = []
    for recipe in fake_recipes_db:
        recipe_out = RecipeOut(**recipe.dict())
        fake_recipes_out.append(recipe_out)
    return fake_recipes_out

@router.post("/")
async def create_recipe(new_recipe: RecipeNew):
    saved_recipe = save_recipe(new_recipe)
    recipe = RecipeOut(**saved_recipe.dict())
    return recipe


def save_recipe(recipe_to_save: RecipeNew):
    recipe_id = UUID()
    created_at = datetime.now()
    modified_at = created_at
    recipe_in_db = RecipeInDB(**recipe_to_save.dict(), recipe_id=recipe_id, created_at=created_at, modified_at=modified_at)
    print(f"Saved {recipe_in_db.name}")
    return recipe_in_db