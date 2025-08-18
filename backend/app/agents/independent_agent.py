from __future__ import annotations
from typing import Optional, List, Dict, Any
import contextvars

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.tools import tool

from app.services.llm import get_llm
from app.tools.weather import get_weather
from app.tools.rag_tool import rag_search
from app.tools.vit import classify_crop_disease as vit_classify_direct

_current_session_id = contextvars.ContextVar("session_id", default="default")

class AttachmentStore:
    _images_b64: Dict[str, List[str]] = {}

    @classmethod
    def put_images(cls, session_id: str, images_b64: Optional[List[str]]):
        if images_b64 is None:
            return
        cls._images_b64[session_id] = images_b64

    @classmethod
    def get_image_b64(cls, session_id: str, idx: int) -> str:
        imgs = cls._images_b64.get(session_id, [])
        if idx < 0 or idx >= len(imgs):
            raise ValueError(f"image_idx {idx} is out of range (have {len(imgs)})")
        return imgs[idx]

@tool("classify_crop_disease", return_direct=False)
def classify_crop_disease_indirect(image_idx: int = 0) -> dict:
    """Classify a crop disease from an uploaded image. Pass image_idx=0 for first image."""
    session_id = _current_session_id.get()
    b64 = AttachmentStore.get_image_b64(session_id, image_idx)
    return vit_classify_direct.invoke({"image_base64": b64})

_session_store: dict[str, ChatMessageHistory] = {}

def _get_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]

def _prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system",
             """You are AgriBot, a specialized AI assistant expert in the field of agriculture. Your sole purpose is to provide accurate, helpful, and science-based information related to farming, crop management, soil science, pest control, irrigation, agricultural technology, and livestock management.

Core Rules:
1. Strictly On-Topic: You MUST only answer questions directly related to agriculture. If a user asks about anything else (e.g., movies, politics, history, coding, general trivia), you MUST politely decline and state your purpose. Example refusal: "My expertise is limited to agriculture. I cannot answer questions about that topic. Please ask me something related to farming."
2. Handling Unknowns: If a question is about agriculture but you do not have specific or reliable information to provide a confident answer, you MUST NOT invent an answer. Instead, clearly state that you do not have the information and, if possible, suggest where the user might find it. Example: "That is a very specific question about [topic]. I do not have sufficient data to provide a reliable answer. For the most accurate information, I recommend consulting a local agricultural extension office or a specialized agronomist."
3. Tone: Your tone should be professional, clear, and helpful. Base your answers on established scientific principles and practical farming knowledge. Dont use markdown format, it is not supported.

Language Policy:
• If a Preferred Language is provided in the user context, reply in that language.
• Otherwise, infer the user's language from the latest message and reply in the same language.
• Avoid unnecessary code-switching. If language is unclear, default to English.

Tool Usage Policy:
• get_weather for weather queries (always show units).
• rag_search for factual/KB questions; cite sources briefly if available.
• classify_crop_disease only if the user asked about an image/crop disease and at least one image is attached; when calling it, pass image_idx (0 for first image).
Be concise and never make up citations."""),
            MessagesPlaceholder("chat_history"),
            ("user", "{input}"),
            ("user", "Attachments available: {attachments_overview}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

def build_independent_agent() -> AgentExecutor:
    llm = get_llm()
    tools = [get_weather, rag_search, classify_crop_disease_indirect]
    agent = create_tool_calling_agent(llm, tools, _prompt())
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        max_iterations=4,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

class IndependentAgent:
    def __init__(self) -> None:
        self.executor = build_independent_agent()

    def _with_history(self, session_id: str) -> RunnableWithMessageHistory:
        return RunnableWithMessageHistory(
            self.executor,
            lambda session_id=session_id: _get_history(session_id),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def respond(self, session_id: str, user_text: str, images_base64: Optional[List[str]] = None, stream: bool = False):
        AttachmentStore.put_images(session_id, images_base64)
        attachments_overview = f"{len(images_base64)} image(s)" if images_base64 else "none"
        _current_session_id.set(session_id)
        runnable = self._with_history(session_id)
        inputs = {"input": user_text, "attachments_overview": attachments_overview}
        result = runnable.invoke(inputs, {"configurable": {"session_id": session_id}})
        return {
            "text": result.get("output") if isinstance(result, dict) else str(result),
            "intermediate_steps": result.get("intermediate_steps", []),
        }

    def stream(self, session_id: str, inputs: Dict[str, Any], images_base64: Optional[List[str]] = None):
        AttachmentStore.put_images(session_id, images_base64)
        _current_session_id.set(session_id)
        runnable = self._with_history(session_id)
        for chunk in runnable.stream(inputs, {"configurable": {"session_id": session_id}}):
            if "output" in chunk:
                yield chunk["output"]
