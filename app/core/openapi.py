from fastapi import FastAPI


def customize_openapi(app: FastAPI): # pragma: no cover
    if app.openapi_schema:
        return

    openapi_schema = app.openapi()
    openapi_schema["components"]["securitySchemes"] = {
        "BasicAuth": {
            "type": "http",
            "scheme": "basic",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BasicAuth": []}])
    app.openapi_schema = openapi_schema