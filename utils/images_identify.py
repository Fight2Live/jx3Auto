import cv2
import numpy

ART_ICON = r'./resource/artIcon.png'
# main_path = r'E:\study_infor\Project\AutoStand\resource\temp\jx3Screen.jpg'
# main_path = r'E:\study_infor\Project\AutoStand\resource\mainLayout.png'
# sub_path = r'E:\study_infor\Project\AutoStand\resource\artIcon.png'


def get_target_position(main_path, sub_path=ART_ICON, show_result=False):
    main_image = cv2.imread(main_path)
    sub_image = cv2.imread(sub_path)
    x_click, y_click = 0, 0
    result = cv2.matchTemplate(main_image, sub_image, cv2.TM_CCOEFF_NORMED)

    # 设置匹配结果的阈值
    threshold = 0.8

    # 将匹配结果中大于阈值的部分标记出来
    locations = numpy.where(result >= threshold)

    for point in zip(*locations[::-1]):
        cv2.rectangle(main_image, point, (point[0] + sub_image.shape[1], point[1] + sub_image.shape[0]), (0, 255, 0), 2)
        x_click, y_click = point[0] + 10, point[1] + 10  # 目标点击点

    if show_result:
        show_match_result(main_image)

    return x_click, y_click

def show_match_result(main_image):
    cv2.imshow('Matched Image', main_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    get_target_position(main_path, sub_path, True)