from distutils.core import setup

setup(
    name="cgt_map_backend",
    version="0.1",
    packages=["cgt_map_backend"],
    install_requires=[
        "pydantic >= 2",
        "pydantic-settings",
        "fastapi",
        "uvicorn",
        "motor",
        "click",
        "mangum",
        "mongoengine",
    ],
)
