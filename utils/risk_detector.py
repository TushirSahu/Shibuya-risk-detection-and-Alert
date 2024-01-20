from library import *
from utils.bbox import createPolygon

def detectPersonRisk(frame_df, dict_vertices, img,thickness=1):
        count_person_roi = 0
        risk_detections = [0 for x in range(len(frame_df))]
        img = createPolygon(img=img,dict_vertices=dict_vertices)
        classes = frame_df['class'].values

        for i, person_detected in enumerate(frame_df[['xmin','xmax','ymin','ymax']].values.astype(int)):

            start_point = (person_detected[0], person_detected[-1])
            end_point = (person_detected[1], person_detected[2])
            class_detected = classes[i]
            title_x = int(person_detected[0] + ((person_detected[1]-person_detected[0])/2))
            title_y = int(person_detected[2] - (person_detected[2] *0.05))

            if class_detected == 'car':
                cv2.rectangle(img, start_point, end_point, (255,0,0), thickness) # red: in danger
                cv2.putText(img,'C', (title_x, title_y), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,0,0), 2)
            if class_detected == 'person':


                x_min, x_max = person_detected[0], person_detected[1]
                y_max = person_detected[-1]


                foot_1 = (int(x_min),int(y_max))
                foot_2 = (int(x_max),int(y_max))

                person_detected_in_risk = False
                for cw_id,vertices in zip(dict_vertices.keys(),dict_vertices.values()):
                    inside1 = cv2.pointPolygonTest(vertices, foot_1, False)
                    inside2 = cv2.pointPolygonTest(vertices, foot_2, False)

                    if inside1 == 1 or inside2 == 1:
                        person_detected_in_risk = True
                        count_person_roi += 1
                        risk_detections[i] = 1


                color_bbox_person = (0,0,255) if person_detected_in_risk else (0,255,0)
                cv2.rectangle(img, start_point, end_point, color_bbox_person, thickness)
                cv2.putText(img,'P', (title_x, title_y), cv2.FONT_HERSHEY_TRIPLEX, 1, color_bbox_person, 2)
            if class_detected == 'crosswalk':
                cv2.rectangle(img, start_point, end_point, (28,226,233), thickness)



        return count_person_roi, risk_detections, img