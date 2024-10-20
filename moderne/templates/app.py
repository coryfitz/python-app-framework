from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import os

# Define a simple handler to serve the HTML file
async def homepage(request):
    app_root = os.path.dirname(__file__)
    file_path = os.path.join(app_root, 'app', 'static', 'index.html') 
    return FileResponse(file_path)

routes = [
    Route("/", homepage),
    Mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'app', 'static')), name='static')
]

# Create the ASGI app
app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
