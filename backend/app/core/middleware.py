import time
import uuid
import logging
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request information"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        ip = request.client.host
        method = request.method
        path = request.url.path
        
        # Log request
        logger.info(f"RequestID: {request_id} - Started {method} {path} from {ip}")
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            status_code = response.status_code
            logger.info(
                f"RequestID: {request_id} - Completed {method} {path} with {status_code} in {process_time:.3f}s"
            )
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.exception(
                f"RequestID: {request_id} - Error during {method} {path} after {process_time:.3f}s: {str(e)}"
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for simple rate limiting"""
    
    def __init__(self, app: FastAPI, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_timestamps = {}
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Get current time
        current_time = time.time()
        
        # Clean up old timestamps (older than 1 minute)
        if client_ip in self.request_timestamps:
            self.request_timestamps[client_ip] = [
                timestamp for timestamp in self.request_timestamps[client_ip]
                if current_time - timestamp < 60
            ]
        else:
            self.request_timestamps[client_ip] = []
        
        # Check if rate limit is exceeded
        if len(self.request_timestamps[client_ip]) >= self.requests_per_minute:
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"Retry-After": "60"}
            )
        
        # Add current timestamp to list
        self.request_timestamps[client_ip].append(current_time)
        
        # Process request
        return await call_next(request)


def add_middleware(app: FastAPI):
    """Add all middleware to FastAPI app"""
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # This should be configured in settings
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Add rate limiting middleware
    app.add_middleware(RateLimitMiddleware, requests_per_minute=60)