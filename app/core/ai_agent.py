from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, SystemMessage

from app.config.settings import settings


def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):

    if not query:
        return "No input provided"

    # Convert list query to string
    if isinstance(query, list):
        query = " ".join(query)

    # Initialize model
    llm = ChatGroq(
        model=llm_id,
        api_key=settings.GROQ_API_KEY
    )

    messages = []

    # Strong system prompt
    if system_prompt:

        strict_prompt = f"""
        You are a strict AI assistant.

        Role:
        {system_prompt}

        Only answer questions related to this role.

        If the user asks unrelated questions,
        politely refuse.
        """

        messages.append(
            SystemMessage(content=strict_prompt)
        )

    # User query
    messages.append(
        HumanMessage(content=query)
    )

    # Tavily Search
    if allow_search:
        try:
            search_tool = TavilySearch(max_results=2)

            search_results = search_tool.invoke(query)

            messages.append(
                SystemMessage(
                    content=f"Relevant web search results:\n{search_results}"
                )
            )

        except Exception as e:
            print("Search failed:", e)

    # Generate response
    response = llm.invoke(messages)

    return response.content