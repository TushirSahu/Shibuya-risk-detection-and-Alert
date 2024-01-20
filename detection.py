from library import *
from config import coco_classes,client,device,Config,model,sahi_model
from utils.risk_detector import detectPersonRisk
from utils.extract import extract_images

def build_sahi_results(result_sahi_obj):

    object_prediction_list  = result_sahi_obj.object_prediction_list

    res_sahi_list = []

    for ind, _ in enumerate(object_prediction_list):
        boxes = object_prediction_list[ind].bbox.minx, object_prediction_list[ind].bbox.miny, object_prediction_list[ind].bbox.maxx, object_prediction_list[ind].bbox.maxy
        clss = object_prediction_list[ind].category.id
        conf = object_prediction_list[ind].score.value
        boxes = list(boxes)

        if clss in coco_classes:
            res_sahi_list.append(boxes + [conf,clss])

    return res_sahi_list

def pipeline_from_predictions(result_array, img):

    position_frame = pd.DataFrame(result_array,
                               columns = ['xmin', 'ymin', 'xmax',
                                          'ymax', 'conf', 'class'])

    position_frame['class'] = position_frame['class'].replace({0:'person', 2:'car'})

    count_person_roi, risk_detections,bbox_image = detectPersonRisk(position_frame,
                                                                     croswalk_points,
                                                                     img)

    video_height,video_width,_ = bbox_image.shape

    cv2.putText(bbox_image,f'Danger: {count_person_roi}',
            (video_width-200,video_height-(video_height -100)),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (0,0,255),
            2)
    sms_sent = False
    if not sms_sent and count_person_roi > 0:
        print("SENDING SMS!!!")
        message = client.messages.create( body="Someone is not following the rules",
            from_='+19387770682',
              to='+919993205568')
        sms_sent = True
        print("Hope you got the message on your phone")
    return bbox_image



#Extrac a frame of video to example image
extract_images(Config.infe_video, './example_image.png')
#polygon points of risk area
croswalk_points = {

    1: np.array([[223,607], [135,400],[227,299], [570,147], [682,133], [826,148],[900,205], [428,603]],dtype =int),
    2: np.array([[179,274], [37,199], [176,121],[491,136]],dtype =int),
    3: np.array([[852,123],[725,108], [822,58], [900,81]],dtype =int),

}

exp_image = cv2.imread('./example_image.png')
exp_image_sahi = cv2.imread('./example_image.png')

results = model.predict(exp_image,
                        conf = 0.5,
                        classes = coco_classes,
                        device = device,
                        verbose = False)

result_sahi = get_sliced_prediction(
    exp_image_sahi,
    sahi_model,
    slice_height=256,
    slice_width=256,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2,
    verbose= True
)

res_sahi_list =  build_sahi_results(result_sahi)



bbox_image = pipeline_from_predictions(result_array = results[0].cpu().numpy().boxes.data,
                          img = exp_image)

bbox_image_sahi = pipeline_from_predictions(result_array = res_sahi_list,
                          img = exp_image_sahi)




cv2.imwrite('./example_image_bbox.png', bbox_image)
cv2.imwrite('./example_image_bbox_sahi.png', bbox_image_sahi)



from tqdm import tqdm

cap = cv2.VideoCapture(Config.infe_video)

video_width = int(cap.get(3))
video_height = int(cap.get(4))
size = (video_width, video_height)
fourcc = 'MP4V'

tmp_output_path = './tmp_output_video.mp4'
out = cv2.VideoWriter(tmp_output_path,
                      cv2.VideoWriter_fourcc(*fourcc),
                      30, # fps
                      size)

tmp_output_path_sahi = './tmp_output_video_sahi.mp4'
out_sahi = cv2.VideoWriter(tmp_output_path_sahi,
                      cv2.VideoWriter_fourcc(*fourcc),
                      30, # fps
                      size)


for i in tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):

    frame_exists, frame = cap.read()


    if  frame_exists:

        results = model.predict(frame,
                        conf = Config.conf,
                        classes = coco_classes,
                        device = device,
                        verbose = False)

        result_sahi = get_sliced_prediction(
            frame,
            sahi_model,
            slice_height=256,
            slice_width=256,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2,
            verbose= False
        )

        res_sahi_list =  build_sahi_results(result_sahi)



        bbox_image = pipeline_from_predictions(result_array = results[0].cpu().numpy().boxes.data,
                                  img = frame)

        bbox_image_sahi = pipeline_from_predictions(result_array = res_sahi_list,
                                  img = frame)

        out.write(bbox_image)
        out_sahi.write(bbox_image_sahi)
    else:
        print("\nCan't receive frame (stream end?). Exiting...\n")
        break


cap.release()
out.release()
out_sahi.release()
cv2.destroyAllWindows()

if os.path.exists(Config.output_path):
    os.remove(Config.output_path)

if os.path.exists(Config.output_path_sahi):
    os.remove(Config.output_path_sahi)

subprocess.run(
    ["ffmpeg",  "-i", tmp_output_path,"-crf","18","-preset","veryfast","-hide_banner","-loglevel","error","-vcodec","libx264",Config.output_path])

subprocess.run(
    ["ffmpeg",  "-i", tmp_output_path_sahi,"-crf","18","-preset","veryfast","-hide_banner","-loglevel","error","-vcodec","libx264",Config.output_path_sahi])


os.remove(tmp_output_path)
os.remove(tmp_output_path_sahi)


frac = 0.7
display(Video(data=Config.output_path, height=int(720*frac), width=int(1280*frac), embed=True))