from fastapi import FastAPI
from environment import Env

app = FastAPI()
env = Env()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/reset")
def reset(task: str = "easy"):
    obs = env.reset(task)
    return {"observation": obs}

@app.post("/step")
def step(action: str):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
