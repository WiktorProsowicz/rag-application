import os
import multiprocessing

import uvicorn


if __name__ == "__main__":

    host = os.environ["HOST"]
    port = int(os.environ["PORT"])
    dev_mode = bool(os.environ["DEV_MODE"])
    n_workers = (multiprocessing.cpu_count() * 2) + 1

    if dev_mode:
        reload_args = {
            "reload": True,
            "reload_dirs": ["src"], 
        }
    
    else:
        reload_args = {
            "reload": False,
        }

    uvicorn.run("api:app",
                host=host,
                port=port,
                workers=n_workers,
                log_level="info",
                access_log=True,
                limit_concurrency=1000,
                timeout_keep_alive=5,
                **reload_args)