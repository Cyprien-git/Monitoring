import os
import psutil
from fastapi import FastAPI
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio

app = FastAPI()

URL = os.getenv("DOCKER_INFLUXDB_INIT_URL", "http://influxdb:8086")
TOKEN = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
ORG = os.getenv("DOCKER_INFLUXDB_INIT_ORG", "my-org")
BUCKET = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET", "my-bucket")

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

async def monitor_task():
    while True:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        point = Point("system_stats") \
            .tag("host", "raspberry") \
            .field("cpu_usage", cpu) \
            .field("ram_usage", ram) \
            .field("disk_usage", disk)

        try:
            write_api.write(bucket=BUCKET, org=ORG, record=point)
            print(f"✅ API Sent: CPU {cpu}% | RAM {ram}% | DISK {disk}%")
        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_task())

@app.get("/")
def read_root():
    return {"status": "Monitoring is running", "target": URL}
