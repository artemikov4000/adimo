from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
def generate_image_caption(image_url):
    # Ваш API ключ Clarifai
    api_key = '6c67386c2a86400a9aad5caa530bbfee'

    # Создание канала и клиента
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    # Создание запроса
    metadata = (('authorization', f'Key {api_key}'),)
    request = service_pb2.PostModelOutputsRequest(
        model_id='general-image-recognition',  # Используем модель общего назначения
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        url=image_url
                    )
                )
            )
        ]
    )

    # Отправка запроса
    response = stub.PostModelOutputs(request, metadata=metadata)

    # Проверка ответа
    if response.status.code != status_code_pb2.SUCCESS:
        print(f"Ошибка при выполнении запроса: {response.status.description}")
        return None

    # Генерация описания
    captions = [concept.name for concept in response.outputs[0].data.concepts]
    return captions

if name == "main":
    image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6uyFU_JaRQhqHhtQ1AxawsxDNO7y8EV8MOg&s'  # Замените на URL вашего изображения
    captions = generate_image_caption(image_url)
    if captions:
        print("Описание изображения:")
        for caption in captions:
            print(caption)