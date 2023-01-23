from uuid import uuid4, UUID
from datetime import datetime
from fastapi import APIRouter

from ..schemas.recipe import RecipeNew, Recipe#, RecipeOut

fake_recipes_db = [
    Recipe(recipe_id=UUID("7309c6a3-36d0-45cf-ac4c-daada6155f25"), created_at=datetime.now(), modified_at=datetime.now(), name="korean beef", author="Rex Tavington", rating=8, ingredients=["ground beef", "soy sauce", "garlic", "ginger"]),
    Recipe(recipe_id=UUID("55405d41-1ab9-4894-9734-4e4f1058a1ad"), created_at=datetime.now(), modified_at=datetime.now(), name="mac & cheese", author="Joe", rating=9, ingredients=["macaroni pasta", "cheddar cheese", "pepperjack cheese", "milk"]),
    Recipe(recipe_id=UUID("06ea4ac3-bac9-44f2-8b86-acaa83b0fc4b"), created_at=datetime.now(), modified_at=datetime.now(), name="dan dan noodles", author="oshagshennesy", rating=6, ingredients=["egg noodles", "soy sauce", "chili oil", "ginger", "pork"])
    # {"recipe_id": uuid4(), "name": "korean beef", "author": "Rex Tavington"},
    # {"recipe_id": uuid4(), "name": "mac & cheese", "author": "Joe"},
    # {"recipe_id": uuid4(), "name": "dan dan noodles", "author": "Oshagshennesy"},
     ]

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)

@router.get("/{recipe_id}")
async def read_recipe(recipe_id: UUID) -> Recipe:
    recipe_in_db = next((item for item in fake_recipes_db if item.recipe_id == recipe_id), None)
    # return RecipeOut(**recipe_in_db.dict())
    return recipe_in_db

## TODO: support a GET with multiple query strings. E.g. /recipes/?author=joe&ingredient=macaroni
## TODO: update ingredient query item to be a list. E.g. /recipes/?ingredient=macaroni&ingredient=cheddar cheese
@router.get("/")
async def read_recipes(name: str | None = None, author: str | None = None, ingredient: str | None = None) -> list[Recipe]:
    if name:
        recipe_in_db = next((item for item in fake_recipes_db if item.name == name), None)
        #return RecipeOut(**recipe_in_db.dict())
        return [recipe_in_db]
    if author:
        recipe_in_db = next((item for item in fake_recipes_db if item.author == author), None)
        return [recipe_in_db]
        # recipes_out: [RecipeOut] = []
        # for recipe in fake_recipes_db:
        #     recipe_out = RecipeOut(**recipe.dict())
        #     recipes_out.append(recipe_out)
        # return recipes_out
    if ingredient:
        recipes = [recipe for recipe in fake_recipes_db for ingred in recipe.ingredients if ingred == ingredient]
        return recipes
        # recipes_out: [RecipeOut] = []
        # for recipe in recipes:
        #     recipe_out = RecipeOut(**recipe.dict())
        #     recipes_out.append(recipe_out)
        # return recipes_out
        
    ## NOTE: if no query is provided, simply provide all the recipes. Works for now
    ## NOTE...: but obviously does not scale. 
    return fake_recipes_db

    # recipes_out: [RecipeOut] = []
    # for recipe in fake_recipes_db:
    #     recipe_out = RecipeOut(**recipe.dict())
    #     recipes_out.append(recipe_out)
    # return recipes_out

@router.post("/")
async def create_recipe(new_recipe: RecipeNew) -> Recipe:
    saved_recipe = save_recipe(new_recipe)
    # recipe = RecipeOut(**saved_recipe.dict())
    return saved_recipe

@router.put("/{recipe_id}")
async def update_recipe(recipe_id: UUID, recipe: Recipe) -> Recipe:
    recipe.modified_at = datetime.now()
    for stored_recipe in fake_recipes_db:
        if stored_recipe.recipe_id == recipe_id:
            # do not want to lose original creation time
            recipe.created_at = stored_recipe.created_at 
            fake_recipes_db.remove(stored_recipe)
            fake_recipes_db.append(recipe)
    return recipe
    # return RecipeOut(**recipe.dict())

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: UUID, status_code=204):
    for recipe in fake_recipes_db:
        if recipe.recipe_id == recipe_id:
            fake_recipes_db.remove(recipe)


def save_recipe(recipe_to_save: RecipeNew) -> Recipe:
    recipe_id = uuid4()
    created_at = datetime.now()
    modified_at = created_at
    recipe_in_db = Recipe(**recipe_to_save.dict(), recipe_id=recipe_id, created_at=created_at, modified_at=modified_at)
    print(f"Saved {recipe_in_db.name}")
    return recipe_in_db

