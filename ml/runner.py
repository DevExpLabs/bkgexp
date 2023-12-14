import runpod
from handler import Handler
from model.model import Model


model = Model()
handler = Handler(model)

runpod.serverless.start({"handler": handler})
