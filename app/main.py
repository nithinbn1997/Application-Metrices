from app.logger import get_logger
from app.routes import (
    internal_api, 
    qcl_cc_api, 
    db_api, 
    qcl_orders_api,
    qcl_attachments_api
)
from app.actions import transaction_actions
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from fastapi import (
    Response
)  

from fastapi import FastAPI, HTTPException

log = get_logger()

app = FastAPI(
    title="Lattice QCL Transaction Handler",
    version="0.1",
    description="Handles all the Lattice transactions",
    docs_url="/docs",
)



@app.get("/metrics")
async def metrics():
   
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
async def root():
    """_summary_

    Returns:
        _type_: _description_
    """    
    return {"message":
                "Welcome to QCL Transaction Handler. Please go to "
                "'/docs' route for Swagger/OpenAPI Documentation."
            }

@app.get("/ping")
async def ping():
    """_summary_

    Returns:
        _type_: _description_
    """    
    return {"message": "pong"}

@app.on_event("startup")
async def startup_event():
    """_summary_
    """    
    await transaction_actions.update_transactions_status()


@app.get("/health/server/")
async def server_ping():
    try:
        return {"status": "ok"}
    except:
        raise HTTPException(status_code=503, detail="Service Unavailable")


app.include_router(qcl_cc_api.router)
app.include_router(qcl_orders_api.router)
app.include_router(qcl_attachments_api.router)
app.include_router(db_api.router)
app.include_router(internal_api.router)
