# Selenium WebDriver
[![SeleniumHQ](http://www.seleniumhq.org/images/big-logo.png)](http://www.seleniumhq.org/)

## Introduction
- 단순한 API들로 구성된 개발자 중심의 웹 UI 테스트 자동화 도구
- 다양한 브라우저(FireFox, Internet Explorer, Safari, Chrome...)에서 일관성 있는 테스트 가능
- multiple frames, multiple browser windows, popups, and alerts, Page navigation, Drag-and-drop, AJAX-based UI elements등 테스트 가능

## Why Selenium WebDriver?
- Driver 변경만으로 다양한 환경에서 테스트 수행이 가능
- 표준 API 지원을 통해 개발자 UI 테스트에 최적화
- Real browser 외에도 HtmlUnitDriver 지원을 통한 빠른 테스트 피드백이 가능
- 현재 Selenium과 연계를 통해 장단점 상호 보완 중

## Requirements
#### ∙ Git Clone

```python
$ git clone https://github.com/XXOK/Selenium_automation.git
```

#### ∙ Python 3

https://www.python.org/downloads/

#### ∙ Chromedriver

https://chromedriver.storage.googleapis.com/index.html (LATEST_RELEASE 확인)

PATH : `/Users/{사용자명}/Selenium_automation/drivers` (mac OS)

#### ∙ Virtualenv

`virtualenv` is a tool to create isolated Python environments.
  
home directory 설치 권장 (Git 사용 시 이슈 발생)

```python
$ cd /Users/{사용자명}
$ python3 -m venv {가상환경 이름}
```

#### ∙ Install-Package

```python
$ pip install -r requirements.txt
```

## Usage

#### ∙ Using the Python Interpreter

`Preferences[command + ,] -> Project interpreter -> ⚙️(click) -> Add local -> Virtualenv location -> apply`

#### ∙ Testing with pytest

```python
$ pytest -v -s wwwauto/
```

## Reference
#### WebDriver를 이용한 UI 테스트
http://wiki.gurubee.net/pages/viewpage.action?pageId=6259762#Selenium%EC%9D%84%EC%9D%B4%EC%9A%A9%ED%95%9CUI%ED%85%8C%EC%8A%A4%ED%8A%B8-4.WebDriver%EB%A5%BC%EC%9D%B4%EC%9A%A9%ED%95%9CUI%ED%85%8C%EC%8A%A4%ED%8A%B8
