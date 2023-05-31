import openai
from utitlities import DBUpdateARG, DBReadARG, DBRead

openai.api_key = DBRead('dalle_image_generator','API_Key')


def DalleImageEditAPI(image, prompt, numberOfImage, size, userSession):
    try:
        result = {}
        image = openai.Image.create_edit(
            image = open(image,'rb'),
            prompt = prompt,
            n = int(numberOfImage),
            size = size
        )
        images_count = int(DBReadARG("user", "images_count", "email", userSession, result))
        updatedImage = images_count+int(numberOfImage)
        DBUpdateARG('user','images_count',updatedImage,'email',userSession)
        imagesurl = [item["url"] for item in image["data"]]
        return imagesurl, updatedImage
    except Exception as e:
        images_count = int(DBReadARG("user", "images_count", "email", userSession, result))
        return e , images_count


