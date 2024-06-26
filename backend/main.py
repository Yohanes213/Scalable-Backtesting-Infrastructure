from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from  .routers import user_router
from  .routers import scenes_route
import uvicorn
from .utils.database_connection import create_all_tables, drop_all_tables


app = FastAPI(
        title="Scalable Backtesting",
        description="",
        version="1"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Drop tables
drop_all_tables

#Create tables  
create_all_tables()
# populate_data()
   

#routers 
app.include_router(user_router.router)
app.include_router(scenes_route.router)

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
