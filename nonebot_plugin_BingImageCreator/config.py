from pydantic import Extra, BaseModel
from typing import List, Optional


class Config(BaseModel, extra=Extra.ignore):
    bing_cookies: Optional[List[str]] = ""
    bing_proxy : Optional[str] = ""


class ConfigError(Exception):
    pass
