"""Checks reflected HTML in the local FoodBook search response."""
import argparse
import sys
import requests


def main():
    parser = argparse.ArgumentParser(description="Local FoodBook reflected-XSS check")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    payload = "<script>alert('FoodBook-XSS')</script>"
    try:
        response = requests.get(args.base_url.rstrip("/") + "/", params={"q": payload}, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        print("Не удалось обратиться к локальному сайту:", exc)
        return 2
    if payload in response.text:
        print("Небезопасный HTML отражён в ответе: проверка XSS пройдена.")
        print("Для визуальной демонстрации откройте полученный URL в браузере только на локальном сервере.")
        print("URL:", response.url)
        return 0
    print("Исходный payload не найден в HTML-ответе.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
