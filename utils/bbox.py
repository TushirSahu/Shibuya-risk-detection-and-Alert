from library import *


def draw_bbox(df_coords,img,thickness=1):
  cords = df_coords[['xmin','xmax','ymin','ymax']].values.astype(int)
  classes = df_coords['class'].values
  for i, person_cords in enumerate(cords):
    start_point = (person_cords[0],person_cords[-1])
    end_point  = (person_cords[1],person_cords[2])
    class_detected = classes[i]
    if class_detected == 'car':
            cv2.rectangle(img, start_point, end_point, (255,0,0), thickness)
    if class_detected == 'person':
            cv2.rectangle(img, start_point, end_point, (255,0,0), thickness)
    if class_detected == 'crosswalk':
            cv2.rectangle(img, start_point, end_point, (28,226,233), thickness)

    return img
  


def createPolygon(img,dict_vertices):

    for cw_id,vertices in zip(dict_vertices.keys(),dict_vertices.values()):
        cv2.polylines(img, [vertices.reshape(-1,1,2)], True, (0,0,255), 0)

        mod = img.copy()
        mod = cv2.fillPoly(mod, pts = [vertices], color=(0,0,255))
        background = img.copy()
        overlay = mod.copy()

        img = cv2.addWeighted(background, 0.9,overlay, 0.1,0.1, overlay)

    return img