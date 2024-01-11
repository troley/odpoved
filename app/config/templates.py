from fastapi.templating import Jinja2Templates

from app.util.paths import templates_dir


templates = Jinja2Templates(directory=templates_dir)
