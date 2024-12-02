from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
def generate_image_caption(image_url):
    api_key = '6c67386c2a86400a9aad5caa530bbfee'

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

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

    response = stub.PostModelOutputs(request, metadata=metadata)
    if response.status.code != status_code_pb2.SUCCESS:
        print(f"Ошибка при выполнении запроса: {response.status.description}")
        return None
    captions = [concept.name for concept in response.outputs[0].data.concepts]
    return captions


image_url = ('https://i.pinimg.com/originals/8c/02/b4/8c02b4293087c1fe27641e068c8f624d.jpg')  # Замените на URL вашего изображения
captions = generate_image_caption(image_url)
if captions:
    print("Описание изображения:")
    for caption in captions:
        print(caption)