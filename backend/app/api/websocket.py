from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import logging
from app.models import QueryRequest
from app.services.chat_service import chat_service

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.conversation_histories: Dict[str, List[Dict[str, str]]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.conversation_histories[client_id] = []
        logger.info(f"Client {client_id} connected")
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        if client_id in self.conversation_histories:
            del self.conversation_histories[client_id]
        logger.info(f"Client {client_id} disconnected")
    
    def add_to_history(self, client_id: str, role: str, content: str):
        if client_id not in self.conversation_histories:
            self.conversation_histories[client_id] = []
            self.conversation_histories[client_id].append({"role": role,"content": content})

    def get_history(self, client_id: str) -> List[Dict[str, str]]:
        return self.conversation_histories.get(client_id, [])

manager = ConnectionManager()

@router.websocket("/ws/chat/{client_id}")

async def websocket_chat(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            query = message_data.get("query", "")
            if not query:
                await websocket.send_json({
                    "error": "Empty query received."
                })
                continue
            
            # Add user message to history
            manager.add_to_history(client_id, "user", query)
            
            history = manager.get_history(client_id)

            # Create QueryRequest
            request = QueryRequest(
                query=query,
                conversation_history=history[:-1], #Exclude current message
                max_sources=message_data.get("max_sources", 3)
            )

            # Generate Response
            try:
                response = chat_service.generate_response(request)

                # Add assistant message to history
                manager.add_to_history(client_id, "assistant", response.answer)
            
                # Send response back to client
                await websocket.send_json({
                    "answer": response.answer,
                    "sources": [source.dict() for source in response.sources],
                    "conversation_id": client_id
                })

            except Exception as e:
                logger.error(f"Error generating response: {e}")
                await websocket.send_json({
                    "error": str(e)
                })


    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
    except Exception as e:
        logger.error(f"Error in websocket chat for client {client_id}: {e}")
        manager.disconnec(websocket, client_id)