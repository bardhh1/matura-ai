import os
from pathlib import Path

import uvicorn

if __name__ == "__main__":
    backend_directory = Path(__file__).resolve().parents[1]
    os.chdir(backend_directory)
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(backend_directory)],
        env_file=backend_directory / ".env",
        app_dir=str(backend_directory),
    )
