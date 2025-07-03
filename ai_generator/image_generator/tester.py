import uuid
import json
import urllib.request
import urllib.parse
import websocket

class ComfyClient:
    def __init__(self, server: str):
        self.server = server
        self.client_id = str(uuid.uuid4())
        self.ws = None

    def connect_ws(self):
        if self.ws is None or not self.ws.connected:
            self.ws = websocket.create_connection(
                f"ws://{self.server}/ws?clientId={self.client_id}"
            )

    def queue_prompt(self, workflow: dict) -> str:
        payload = {"prompt": workflow, "client_id": self.client_id}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server}/prompt", data=data)
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read())
        return resp_data['prompt_id']

    def wait_for_completion(self, prompt_id: str):
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break

    def get_history(self, prompt_id: str) -> dict:
        with urllib.request.urlopen(f"http://{self.server}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def get_image_bytes(self, filename: str, subfolder: str, folder_type: str) -> bytes:
        params = urllib.parse.urlencode({
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type
        })
        with urllib.request.urlopen(f"http://{self.server}/view?{params}") as response:
            return response.read()

    def generate_images(self, workflow: dict) -> dict:
        """
        1. Submit the workflow prompt
        2. Wait for execution
        3. Retrieve all generated images
        Returns:
            Dict[node_id] = List[image_bytes]
        """
        self.connect_ws()
        prompt_id = self.queue_prompt(workflow)
        self.wait_for_completion(prompt_id)

        history = self.get_history(prompt_id)[prompt_id]
        output_images = {}

        for node_id, node_output in history['outputs'].items():
            if 'images' in node_output:
                images_data = []
                for img in node_output['images']:
                    img_bytes = self.get_image_bytes(img['filename'], img['subfolder'], img['type'])
                    images_data.append(img_bytes)
                output_images[node_id] = images_data

        return output_images
