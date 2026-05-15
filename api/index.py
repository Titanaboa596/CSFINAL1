#!/usr/bin/env python3
"""
WebSocket server for CS Game 2
Uses Python's native socket and asyncio (no external dependencies)
"""
import asyncio
import json
import hashlib
import base64
import logging
from typing import Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketConnection:
    """Simple WebSocket connection handler"""
    
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.closed = False
    
    async def send(self, data: dict):
        """Send a JSON message"""
        try:
            message = json.dumps(data).encode('utf-8')
            # WebSocket frame format
            frame = bytearray()
            frame.append(0x81)  # FIN + TEXT frame
            
            length = len(message)
            if length < 126:
                frame.append(length)
            elif length < 65536:
                frame.append(126)
                frame.extend(length.to_bytes(2, 'big'))
            else:
                frame.append(127)
                frame.extend(length.to_bytes(8, 'big'))
            
            frame.extend(message)
            self.writer.write(bytes(frame))
            await self.writer.drain()
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.closed = True
    
    async def receive(self):
        """Receive a JSON message"""
        try:
            # Read first byte (FIN + opcode)
            data = await self.reader.readexactly(1)
            if not data:
                self.closed = True
                return None
            
            opcode = data[0] & 0x0f
            
            # Read second byte (MASK + length)
            data = await self.reader.readexactly(1)
            masked = bool(data[0] & 0x80)
            length = data[0] & 0x7f
            
            # Read extended length if needed
            if length == 126:
                data = await self.reader.readexactly(2)
                length = int.from_bytes(data, 'big')
            elif length == 127:
                data = await self.reader.readexactly(8)
                length = int.from_bytes(data, 'big')
            
            # Read mask if present
            if masked:
                mask = await self.reader.readexactly(4)
            
            # Read payload
            payload = await self.reader.readexactly(length)
            
            # Unmask if needed
            if masked:
                unmasked = bytearray()
                for i, byte in enumerate(payload):
                    unmasked.append(byte ^ mask[i % 4])
                payload = bytes(unmasked)
            
            # Handle different opcodes
            if opcode == 1:  # Text frame
                try:
                    return json.loads(payload.decode('utf-8'))
                except json.JSONDecodeError:
                    return None
            elif opcode == 8:  # Close frame
                self.closed = True
                return None
            
            return None
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            self.closed = True
            return None
    
    async def close(self):
        """Close the connection"""
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except:
            pass
        self.closed = True

class ConnectionManager:
    """Manage all WebSocket connections"""
    
    def __init__(self):
        self.connections: Set[WebSocketConnection] = set()
    
    async def add(self, conn: WebSocketConnection):
        self.connections.add(conn)
        logger.info(f"✅ Client connected. Total: {len(self.connections)}")
    
    async def remove(self, conn: WebSocketConnection):
        self.connections.discard(conn)
        logger.info(f"❌ Client disconnected. Total: {len(self.connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all clients"""
        disconnected = set()
        for conn in self.connections:
            try:
                await conn.send(message)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
                disconnected.add(conn)
        
        for conn in disconnected:
            await self.remove(conn)

manager = ConnectionManager()

async def handle_websocket(reader, writer):
    """Handle a WebSocket connection"""
    # Perform WebSocket handshake
    try:
        # Read HTTP request line
        request_line = await reader.readline()
        headers = {}
        
        while True:
            line = await reader.readline()
            if line == b'\r\n' or line == b'\n':
                break
            
            if b':' in line:
                key, value = line.split(b':', 1)
                headers[key.strip().lower()] = value.strip()
        
        # Check for required headers
        if b'sec-websocket-key' not in headers:
            logger.error("Missing Sec-WebSocket-Key header")
            writer.close()
            return
        
        # Perform handshake
        key = headers[b'sec-websocket-key'].decode()
        accept = base64.b64encode(
            hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()
        ).decode()
        
        response = (
            b"HTTP/1.1 101 Switching Protocols\r\n"
            b"Upgrade: websocket\r\n"
            b"Connection: Upgrade\r\n"
            b"Sec-WebSocket-Accept: " + accept.encode() + b"\r\n"
            b"\r\n"
        )
        writer.write(response)
        await writer.drain()
        
        logger.info("🔗 WebSocket handshake successful")
        
    except Exception as e:
        logger.error(f"Handshake error: {e}")
        writer.close()
        return
    
    # Create connection object
    conn = WebSocketConnection(reader, writer)
    await manager.add(conn)
    
    try:
        # Handle messages
        while not conn.closed:
            message = await conn.receive()
            if message and isinstance(message, dict):
                # Broadcast to all clients
                await manager.broadcast(message)
    
    except Exception as e:
        logger.error(f"Connection error: {e}")
    
    finally:
        await manager.remove(conn)
        await conn.close()

async def main():
    """Start the WebSocket server"""
    import os
    port = int(os.environ.get("PORT", 8081))
    server = await asyncio.start_server(
        handle_websocket,
        '0.0.0.0',
        port
    )
    
    logger.info("=" * 50)
    logger.info("🎮 CS Game 2 WebSocket Server")
    logger.info("=" * 50)
    logger.info("✅ Server running on ws://localhost:8081")
    logger.info("   For remote access: ws://YOUR_IP:8081")
    logger.info("=" * 50)
    
    async with server:
        try:
            await server.serve_forever()
        except KeyboardInterrupt:
            logger.info("\n📴 Shutting down server...")

if __name__ == "__main__":
    asyncio.run(main())
