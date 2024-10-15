import requests
import logging
from decouple import config

logger = logging.getLogger(__name__)


def get_iam_token():
    response = requests.post(
        config('AIM_TOKEN'),
        json={'yandexPassportOauthToken': config('OAUTH_TOKEN')}
    )
    response.raise_for_status()
    return response.json()['iamToken']


async def send_request(iam_token, user_text):
    data = {
        "modelUri": f"gpt://{config('FOLDER_ID')}/yandexgpt",
        "completionOptions": {"temperature": 0.3, "maxTokens": 1000},
        "messages": [
            {"role": "system", "text": "отвечу на любые ваши  впоросы!"},
            {"role": "user", "text": user_text}
        ]
    }
    try:
        response = requests.post(
            config('API_URL'),
            headers={"Accept": "application/json", "Authorization": f"Bearer {iam_token}"},
            json=data
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f'Успешно получен ответ от Yandex GPT')
        answer = result.get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text',
                                                                                              'Ошибка получения ответа.')
    except requests.RequestException as e:
        logger.error(f'Ошибка при запросе к Yandex GPT: {e}')
        answer = 'Произошла ошибка при запросе к Yandex GPT.'
    return answer
