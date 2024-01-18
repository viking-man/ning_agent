import logging
from translatepy import Translate  # 使用Google翻译API
import pytesseract
from PIL import Image
import cv2
import numpy as np

def decode_predictions(scores, geometry,min_confidence):
	# grab the number of rows and columns from the scores volume, then
	# initialize our set of bounding box rectangles and corresponding
	# confidence scores
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []

	# loop over the number of rows
	for y in range(0, numRows):
		# extract the scores (probabilities), followed by the
		# geometrical data used to derive potential bounding box
		# coordinates that surround text
		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability,
			# ignore it
			if scoresData[x] < min_confidence:
				continue

			# compute the offset factor as our resulting feature
			# maps will be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)

			# extract the rotation angle for the prediction and
			# then compute the sin and cosine
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)

			# use the geometry volume to derive the width and height
			# of the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]

			# compute both the starting and ending (x, y)-coordinates
			# for the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)

			# add the bounding box coordinates and probability score
			# to our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])

	# return a tuple of the bounding boxes and associated confidences
	return (rects, confidences)
# 使用Tesseract进行OCR识别
def ocr_text_from_image(image_path, orginal_lang):
    import cv2
    import pytesseract
    from PIL import Image

    # 载入EAST模型
    east_model = "model/frozen_east_text_detection.pb"  # 替换为您的模型路径

    # 读取图像
    image = cv2.imread(image_path)
    orig = image.copy()
    (H, W) = image.shape[:2]

    # 设置EAST检测器的预期尺寸
    (newW, newH) = (320, 320)
    rW = W / float(newW)
    rH = H / float(newH)

    # 调整图像大小并预处理
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # 定义输出层名称
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # 载入EAST模型
    net = cv2.dnn.readNet(east_model)

    # 构建一个blob并通过模型传递
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # 解析检测结果
    min_confidence = 0.5
    (rects, confidences) = decode_predictions(scores, geometry,min_confidence)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # 循环处理边框
    text = ''
    for (startX, startY, endX, endY) in boxes:
        # 缩放边框
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # 提取边框内的文本
        roi = orig[startY:endY, startX:endX]

        # 使用Tesseract进行OCR
        text += pytesseract.image_to_string(roi, config="--psm 6")
        print(text)

    return text


# 使用Google翻译API进行翻译
def translate_text(image_text, target_language='zh-CN'):
    translator = Translate()
    translated_text = translator.translate(image_text, target_language).result
    return translated_text


def extract_words(image_path, orginal_lang, target_lang):
    # 识别韩文文本
    image_text = ocr_text_from_image(image_path, orginal_lang)
    logging.info(f'extracted_original_text->{image_text}')
    # 翻译为中文
    translated_text = translate_text(image_text, target_lang)

    return translated_text, image_text


# 非极大值抑制函数
def non_max_suppression(boxes, probs=None, overlapThresh=0.3):
    # 如果没有提供置信度，则创建一个等于1的数组
    if probs is None:
        probs = np.ones(len(boxes))
    # 确保所有的边界框都是整数
    boxes = boxes.astype("int")
    # 应用置信度阈值
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    # 计算每个边界框的面积
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    # 对置信度进行排序
    idxs = np.argsort(probs)
    # 初始化保留的边界框列表
    pick = []
    # 循环遍历每一个边界框
    while len(idxs) > 0:
        # 获取当前置信度最大的边界框的索引
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # 找到与当前边界框重叠的所有边界框
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # 计算相交的面积
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / area[idxs[:last]]
        # 保留不重叠的边界框
        idxs = np.delete(idxs, np.where(overlap > overlapThresh)[0])
    return boxes[pick]



def extract_word_glm(image_path):
    import cv2
    import numpy as np
    from PIL import Image
    import pytesseract

    image = cv2.imread(image_path)
    # 确保图像的通道数量是3（BGR格式）
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # 加载EAST文本检测器
    # 注意：请确保您有正确的文件路径
    text_detector = cv2.dnn.readNet("model/frozen_east_text_detection.pb")
    # 获取图像尺寸
    height, width = image.shape[:2]
    # 设置EAST文本检测器的输入尺寸
    input_size = (width, height)
    # 输入图像的尺寸必须是可以被32整除的
    if width % 32 != 0:
        input_size = (width - (width % 32), height)
    if height % 32 != 0:
        input_size = (input_size[0], height - (height % 32))
    # 构建一个blob，设置输入尺寸，然后执行文本检测器
    blob = cv2.dnn.blobFromImage(image, 1.0, input_size, (123.68, 116.78, 103.94), swapRB=True, crop=False)
    text_detector.setInput(blob)
    scores, geometry = text_detector.forward(text_detector.getUnconnectedOutLayersNames())
    # 解码检测结果
    rects = []
    confidences = []
    for i in range(scores.shape[2]):
        # 对于每个类别的得分
        if np.any(scores[0][0][i] < 0.5):
            continue
        # 计算边界框的尺寸
        box = geometry[0, 0, i]
        x1 = int(box[0] * width)
        y1 = int(box[1] * height)
        x2 = int(box[2] * width)
        y2 = int(box[3] * height)
        # 计算边界框的置信度
        confidence = scores[0][0][i]
        # 添加边界框和置信度
        rects.append((x1, y1, x2, y2))
        confidences.append(confidence)
    # 应用非极大值抑制来抑制弱、重叠边界框
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    # 循环遍历每个边界框
    text = ''
    for (x1, y1, x2, y2) in boxes:
        # 截取文本区域
        roi = image[y1:y2, x1:x2]
        # 使用Pillow的Image.fromarray方法将OpenCV的图像转换为PIL图像
        text_image = Image.fromarray(roi)
        # 使用pytesseract进行文本识别
        text += pytesseract.image_to_string(text_image, lang='kor')
        # 打印识别的文本
        print(text)

    translated_text = translate_text(text, 'zh')
    return translated_text


if __name__ == "__main__":
    image_path = '../../static/ning_poem.JPG'
    # text = extract_word_glm(image_path)
    # print(text)

    translate_text, original_text = extract_words('../../static/ning_poem.JPG', 'kor', 'zh')
    print("原始文本（韩语）：", original_text)
    print("翻译文本（中文）：", translate_text)
