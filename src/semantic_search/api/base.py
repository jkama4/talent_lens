from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import constants, llm, models
from .utils import typesense_utils as ts_utils
from ..db.session import setup_database
from ..db.pipeline import index_all_candidates
from ..data.seed import seed

from typing import Dict, List


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    ts_utils.generate_collection()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Semantic search API — candidate discovery via RAG"}


@app.post("/seed")
async def seed_endpoint() -> Dict:
    seed()
    count = index_all_candidates()
    return {"seeded": True, "indexed": count}


@app.get("/search")
async def search_endpoint(
    user_prompt: str,
    status: str | None = None,
) -> Dict:
    search_params: Dict = {
        "q": user_prompt,
        "query_by": "embedding",
        "prefix": False,
        "per_page": 10,
    }

    if status:
        search_params["filter_by"] = f"status:={status}"

    results: Dict = (
        constants.TS_CLIENT
        .collections[constants.CONSULTANT_SCHEMA["name"]]
        .documents.search(search_params)
    )

    hits: List[Dict] = []
    for hit in results["hits"]:
        doc: Dict = hit["document"]
        hits.append({
            "id": doc["id"],
            "name": doc.get("name", ""),
            "search_text": doc["search_text"],
            "status": doc["status"],
        })

    return {"results": hits}


@app.post("/chat")
async def chat_endpoint(body: models.ChatRequest) -> Dict:
    messages: List[Dict] = [constants.INITIAL_MESSAGES_STATE] + body.history

    if body.inject_info:
        user_query: str = str(body.history[-1]["content"])
        search_results: Dict = await search_endpoint(user_prompt=user_query)

        if search_results["results"]:
            candidates_text = "\n\n".join(
                f"[{hit['name']} | {hit['status']}]\n{hit['search_text']}"
                for hit in search_results["results"]
            )
            messages.append({
                "role": "user",
                "content": (
                    f"Here are the most relevant candidates retrieved from the database "
                    f"for the query above:\n\n{candidates_text}"
                ),
            })

    response: str = llm.call(messages=messages)
    return {"response": response}
