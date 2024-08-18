from fastapi import FastAPI
# import uvicorn
from . import settings, schemas


core= settings.Settings()
app = FastAPI()

@app.get("/webhook", name="Webhook")
def read_root(req:schemas.WebhookRequest):
    return {"Hello": f"World {core.port}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=core.port)