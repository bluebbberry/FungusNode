import os
from dotenv import load_dotenv, dotenv_values
# loading variables from .env file
load_dotenv()

class FungusService:
    def extract_config(self, statuses):
        values = [None, None]
        for status in statuses:
            content = status['content']
            if "num-server-rounds" in content:
                index = content.index("num-server-rounds")
                value = content[index + len("num-server-rounds") + 1:index + len("num-server-rounds") + 2]
                values[0] = int(value)
            if "fraction-fit" in content:
                index = content.index("fraction-fit")
                value = content[index + len("fraction-fit") + 1:index + len("fraction-fit") + 2]
                values[1] = int(value)
        return values
