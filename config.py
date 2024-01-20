from twilio.rest import Client
from library import *

twilio_phone_number = "+aaaaaaaa"
destination_number = "aaaaaaaaa"
account_sid = 'ACV3647e661b468cc671512ea36fb94b81'
auth_token = 'wefs7b56582136dca1118cdbaf41ca957'
client = Client(account_sid, auth_token)


class Config():
    crosswalk_folder = '/content/crosswalk-2'
    train_results = '/content/runs/detect/train'
    infe_video = '/content/predestrian_walk.mp4'
    output_path = './output_video.mp4'
    output_path_sahi = './output_video_sahi.mp4'
    conf = 0.2
    weights = 'yolov8x.pt'


device = 'cuda:0' if torch.cuda.is_available() else "cpu"

coco_classes = [0,2]
model = YOLO(Config.weights)
weights_path = f'/content/{Config.weights}'
sahi_model = AutoDetectionModel.from_pretrained(
    model_type = 'yolov8',
    model_path = weights_path,
    confidence_threshold=Config.conf,
    device=device
)