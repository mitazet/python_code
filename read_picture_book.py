import requests
import json
import base64
import io
import Image
import console
import photos
import speech

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
API_KEY = 'SET_YOUR_API_KEY'
def goog_cloud_vison (image_content):
	api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
	req_body = json.dumps({
		'requests': [{
			'image': {
				'content': image_content
			},
			'features': [{
				'type': 'TEXT_DETECTION',
				'maxResults': 10,
			}]
		}]
	})
	res = requests.post(api_url, data=req_body)
	return res.json()

def get_text_from_return(res_json):
	text = res_json['responses'][0]['fullTextAnnotation']['text']
	return text

##
## main
##
console.alert("ページを写して", "", "Ok")
pil_img=photos.capture_image()

size = (int(pil_img.size[0]*0.2), int(pil_img.size[1]*0.2))
pil_img = pil_img.resize(size)

#空のインスタンスに保存し、バイナリデータを取得する
img = io.BytesIO()
pil_img.save(img,"JPEG")
img_byte = img.getvalue()

img_str = str(base64.b64encode(img_byte),"utf-8")

#Cloud Vision APIで文字を認識させてTEXTデータを取得する
res_json = goog_cloud_vison(img_str)
text_json = get_text_from_return(res_json)

##内容の確認と読み上げ
print(text_json)
speech.say(text_json)
