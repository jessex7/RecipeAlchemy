from fastapi import APIRouter

fake_recipes = [
    {"recipe_name": "korean beef","author": "Rex Tavington"},
    {"recipe_name": "mac & cheese", "author": "Joe"}]

router = APIRouter(
    prefix="/recipes",
    tags=["items"]
)

@router.get("/")
async def read_recipes():
    return fake_recipes