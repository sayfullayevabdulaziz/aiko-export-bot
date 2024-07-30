import base64
from typing import TypeVar
import aiohttp
from pydantic import BaseModel
from bot.utils.singleton import SingletonMeta
from bot.core.config import settings

T = TypeVar('T', bound=BaseModel)

class ONECClient(metaclass=SingletonMeta):
    def __init__(self, username: str = settings.ONEC_USERNAME, password: str = settings.ONEC_PASSWORD):
        if not hasattr(self, 'initialized'):  # Ensures __init__ is called only once
            self.auth = aiohttp.BasicAuth(username, password)
            self.url = None
            self.session = None
            self.initialized = True
            self._headers = {"Content-Type": "application/json", "Accept": "*/*"}

    async def __aenter__(self):
        if self.session is None:
            self.session = await aiohttp.ClientSession(auth=self.auth).__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
            self.session = None

    async def fetch_data(self, data, model: T, brand: str | None = None):
        if not self.session:
            self.session = await aiohttp.ClientSession(auth=self.auth).__aenter__()
        
        
        if brand == "wood":
            self.url = settings.ONEC_WOOD_ENDPOINT
        elif brand == "rattan":
            self.url = settings.ONEC_RATTAN_ENDPOINT

        async with self.session.post(self.url, json=data) as response:
            response.raise_for_status()
            response_data = await response.json()
            return model.model_validate(response_data)


    async def create_order(self, 
                           data, 
                           login: str = settings.ONEC_USERNAME, 
                           password: str = settings.ONEC_PASSWORD, 
                           brand: str | None = None
                        ):
        """ Create order in 1C """
        # auth = aiohttp.BasicAuth(login, password)
        # if not self.session:
        #     self.session = await aiohttp.ClientSession(auth=self.auth).__aenter__()
        # Encode login and password manually in base64
        credentials = f"{login}:{password}"
        b64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        headers = self._headers.copy()
        headers["Authorization"] = f"Basic {b64_credentials}"


        if brand == "wood":
            self.url = settings.ONEC_WOOD_ORDER
        elif brand == "rattan":
            self.url = settings.ONEC_RATTAN_ORDER

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, json=data, headers=headers) as response:
                response.raise_for_status()
                # return await response.json()

        # async with self.session.get(self.url, json=data, headers=self._headers) as response:
        #     response.raise_for_status()
            # return await response.json()
            