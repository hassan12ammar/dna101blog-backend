# import libraries
from django.contrib.auth import get_user_model
# import files
from dataclasses import dataclass
User = get_user_model()

@dataclass
class Error:
    status: int
    message: str

    def __str__(self) -> str:
        return f"{self.status}: {self.message}"

