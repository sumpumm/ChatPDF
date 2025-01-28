from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import logging,sys,time

logger=logging.getLogger()

#formatting the logs
formatter=logging.Formatter(fmt="%(asctime)s - %(levelno)s - %(message)s")

stream_handler=logging.StreamHandler(sys.stdout)
file_handler=logging.FileHandler('app.log')

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers=[stream_handler,file_handler]

logger.setLevel(logging.INFO)

def register_middleware(app:FastAPI):
    @app.middleware("http")
    async def log_middleware(request: Request,call_next):
        start=time.time()
        response= await call_next(request)
        process_time=time.time()-start
        log_dict={
        'url': request.url.path,
        'method': request.method,
        "status_code": response.status_code,
        'process_time':process_time
        }
        logger.info(log_dict)
        return response

    origins=["http://localhost:8051"]    
    
    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)