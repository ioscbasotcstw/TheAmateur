import json
from io import BytesIO
from typing import  Tuple, Dict

import PIL
from PIL import Image
from google import genai
from google.colab import files
from rich.console import Console
from rich.table import Table

console = Console()

class RainboltParody:
    def __init__(self, title: str, api_key: str):
        self.title = title
        self.api_key = api_key

    def upload_image(self) -> PIL.PngImagePlugin.PngImageFile:
        uploaded = files.upload()

        for filename in uploaded.keys():
            img = Image.open(BytesIO(uploaded[filename]))
            print(f"Uploaded and opened: {filename}")

        return img

    def get_info(self, SYSTEM_PROMPT: str, img: PIL.PngImagePlugin.PngImageFile) -> Tuple[Dict[str, str], str, str]:
        try:
            client = genai.Client(api_key=self.api_key)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[SYSTEM_PROMPT, img]
            )

            if (response.text != "" or response.text is not None) and type(response.text) == str:
                clean_text = response.text.strip().replace('```json', '').replace('```', '')
                return json.loads(clean_text), response.usage_metadata.thoughts_token_count, response.usage_metadata.total_token_count

        except Exception as e:
            print(f"Unfortunately happened an error: {e}")

    def pretty_print_data(self, data: Dict[str, str]) -> None:
        if not data:
            print("No data to display.")
            return

        table = Table(
            title=f"[bold dark_green]{self.title}[/bold dark_green]",
            show_header=True,
            header_style="bold magenta",
            border_style="blue"
        )

        table.add_column("Attribute", style="cyan", no_wrap=True, justify="right")
        table.add_column("Value", style="white")

        for key, value in data.items():
            if key == "confidence_score":
                table.add_row(key, f"[bold yellow]{value}%[/bold yellow]")
            else:
                table.add_row(key, f"[bold yellow]{value}[/bold yellow]")
        console.print(table)
