# AI AGENT NOMAD CODER
## INTRODUCTION
- 아직까지 업계 표준으로 정해진 ai 프레임워크가 없음
- 여러 프레임워크를 가볍게 배워볼 예정
## ENVIORNMENT
- uv
  - 니콜라스 기준 파이썬 패키지 매니저중 uv가 가장 좋음
  - uv sync
    - pyproject.toml에 있는 dependencies 설치
  - uv add
    - 패키지 설치
    - .venv
      - 매번 add를 할 때마다 혹은 uv sync를 처음 할 때 가상 환경 생성
      - 시스템 전체에 전역으로 패키지를 설치하는 대신 .venv라는 독립된 폴더에 설치
      - 가상 환경 활성화
        - source .venv/bin/activate
        - uv run main.py
    - dev
      - dev flag를 통해 개발자가 필요한 패키지 설치
- jupyter
  - 코드를 작성할 때 더 좋은 개발자 경험을 제공

## YOUR FIRST AI AGENT

- agent
  - 사용자를 대신해서 어떤 행동을 해줄 수 있는 시스템
  - 자율적으로 행동하는 시스템이라는 말은 거짓. 단순히 제공된 텍스트를 기반으로 함수를 실행하는 시스템
  - 단순히 LLM이 개발자에게 코드를 실행해달라고 부탁하는 것이라고도 말할 수 있음
  - 실행 과정
    1. AI가 tool 호출을 요청함 (tool_call 발생)
    2. 호출할 함수명과 필요한 인자를 파악함
    3. 인자(Arguments)를 문자열에서 딕셔너리로 변환함
    4. 해당 함수(Function)를 실제로 실행함
    5. 실행 결과를 AI에게 전달함 (role=tool)