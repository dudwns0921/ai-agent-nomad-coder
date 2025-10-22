# AI AGENT NOMAD CODER
## INTRODUCTION
- 아직까지 업계 표준으로 정해진 ai 프레임워크가 없음
- 여러 프레임워크를 가볍게 배워볼 예정
## ENVIORNMENT
### uv

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

### agent

- 사용자를 대신해서 어떤 행동을 해줄 수 있는 시스템
- 자율적으로 행동하는 시스템이라는 말은 거짓. 단순히 제공된 텍스트를 기반으로 함수를 실행하는 시스템
- 단순히 LLM이 개발자에게 코드를 실행해달라고 부탁하는 것이라고도 말할 수 있음
- 실행 과정
  1. AI가 tool 호출을 요청함 (tool_call 발생)
  2. 호출할 함수명과 필요한 인자를 파악함
  3. 인자(Arguments)를 문자열에서 딕셔너리로 변환함
  4. 해당 함수(Function)를 실제로 실행함
  5. 실행 결과를 AI에게 전달함 (role=tool)

## CREWAI: NEWS READER AGENT

### CrewAI

- 파이썬 기반의 멀티에이전트 프레임워크로, 여러 AI 에이전트를 “팀(Crew)”처럼 묶어서 협업하게 설계할 수 있는 도구

- 특징
  - 직관적이고 간단한 API → 빠르게 에이전트 생성 가능
  - 특정 역할(Role)과 도구(Tool)를 부여해 “에이전트 팀”을 구성할 수 있음
  - 워크플로우(작업 흐름) 정의가 쉬움 → 대화형 협업 구조 구현에 유리
  - LangChain, LlamaIndex 같은 복잡한 프레임워크에 비해 진입 장벽이 낮음
- 구현
  - Agent
    - 필수 요소
      - 필수 요소들을 구체적으로 작성할수록 성능 향상
      - 필수 요소들은 설정 파일로 분리하는 것을 추천
      - Role
      - Goal
      - Backstory
  - Task
    - 필수 요소
      - Description
      - Expected Output
    - context
      - 특정 task에서 이전 task의 결과값을 참조할 때 사용

### Pydantic

- Python 데이터 검증 및 설정 관리 라이브러리로, 타입 힌트를 활용해 데이터를 쉽게 검증하고 직렬화/역직렬화할 수 있게 해줌
  - https://docs.pydantic.dev/latest/

## CREWAI: CONTENT PIPELINE AGENT
### Crew
#### Flow
- 복잡한 워크플로우를 구조화하고 제어하는 CrewAI의 고급 기능
- 여러 단계의 작업을 순차적, 병렬적, 조건부로 연결하여 실행 흐름을 정의할 수 있음

- 주요 데코레이터
  - `@start()`
    - Flow의 시작점을 정의
    - Flow가 실행될 때 가장 먼저 호출되는 메서드
  
  - `@listen()`
    - 특정 메서드나 이벤트의 완료를 감지하여 실행
    - 이전 단계의 출력을 입력으로 받을 수 있음
    - 단일 메서드 또는 논리 연산자와 함께 사용 가능
  
  - `@router()`
    - 조건에 따라 다음 실행 경로를 결정
    - 반환값(문자열)에 따라 분기 처리
    - if-else 로직으로 동적 워크플로우 구현
  
  - 논리 연산자
    - `and_()`: 모든 지정된 단계가 완료되면 실행
    - `or_()`: 지정된 단계 중 하나라도 완료되면 실행

- 주요 메서드
  - `flow.kickoff()`
    - Flow 실행 시작
  
  - `flow.plot()`
    - Flow의 실행 구조를 시각화
#### Flow State
- Flow 내에서 여러 메서드 간 데이터를 공유하고 전달하기 위한 상태 관리 시스템
- Pydantic의 BaseModel을 상속받아 타입 안정성을 보장하는 상태 클래스를 정의

- 주요 특징
  - Flow 클래스에 제네릭 타입으로 State 클래스를 지정: `Flow[StateClass]`
  - Pydantic BaseModel을 활용하여 상태 구조와 기본값 정의
  - 딕셔너리 방식으로 접근: `self.state["key"]`
  - Flow의 전체 실행 과정에서 데이터 일관성 유지

#### CrewAI와 Pydantic 연동 시 주의사항
- **문제**: CrewAI는 `crew.kickoff(inputs={})`에서 Pydantic 객체를 직접 받을 수 없음
- **원인**: CrewAI 입력 제약 - `str`, `int`, `float`, `bool`, `dict`, `list`만 허용
- **해결방법**:
  ```python
  # ❌ 에러 발생
  inputs={"blog_post": self.state.blog_post}  # BlogPost 객체
  
  # ✅ 올바른 방법  
  inputs={"blog_post": self.state.blog_post.model_dump()}  # 딕셔너리로 변환
  ```
- **핵심 포인트**:
  - `model_dump()`: Pydantic 객체 → Python 딕셔너리 변환
  - CrewAI 호환성을 위한 필수 처리 과정
  - 모든 Pydantic 모델 전달 시 적용 필요

## AUTOGEN: GROK DEEP RESEARCH AGENT
- 주요 특징
  - Microsoft에서 만듦
  - AI AGENT계의 할아버지같은 프레임워크
  - AI AGENT를 활용한 복잡한 기능을 만들기 위해서는 별도의 Core 패키지를 깊게 학습하고 다뤄야 한다는 단점
  - Langgraph는 그 자체가 Core로, 간단한 개념 몇 가지만 익히면 복잡한 기능을 구현할 수 있음
  - 니콜라스가 보기에는 AI AGENT 프레임워크 경쟁에서는 살아남지 못할 거 같음
### AgentChat
- agent들의 그룹챗을 만들 수 있는 프레임워크
- 여러 agent들의 집합을 team이라고 하고, Microsoft에서는 여러 team preset을 지원
- Team preset
  - RoundRobinGroupChat
    - 라운드 로빈 방식으로 참가자들이 교대로 그룹 채팅을 운영하는 팀
    - 라운드 로빈 스케줄링은 시분할 시스템을 위해 설계된 선점형 스케줄링의 하나로서, 프로세스들 사이에 우선순위를 두지 않고, 순서대로 시간단위로 CPU를 할당하는 방식의 CPU 스케줄링 알고리즘
    - 모든 Agent들이 순서대로 대화를 이어나가는 형식이라고 보면 됨
  - SelectorGroupChat
    - 각 메시지 이후 ChatCompletion 모델을 사용하여 다음 발표자를 선택하는 팀
    - 라운드 로빈 그룹챗에서는 각 Agent들이 순서대로 대화를 이어가지만, SelectorGroupChat에서는 누가 말할지를 AI가 대화 히스토리 등을 참고 후 결정해 발언권을 넘기는 방식

## Introducing OpenAI Agents SDK

## 프레임워크 특징

### 장점
- **경량성**: 매우 가볍고 간단한 구조
- **낮은 학습 곡선**: 배워야 할 개념이 적음
- **낮은 추상화 레벨**: 직접적인 제어 가능 (레고 블럭을 직접 조립)
- **빌트인 트레이싱**: 에이전트 툴 호출 과정 전체 확인 가능

### 단점
- **통합성 부족**: 다른 모델 사용 시 통합이 원활하지 않음
- **수동 작업 필요**: 추상화가 적어 직접 구현해야 하는 부분이 많음

### 관련 도구
- **Streamlit**: 파이썬으로 UI를 쉽게 만들 수 있는 도구

---

## OpenAI SDK 스트리밍 이벤트 체계

### 1. `raw_response_event` (원본 응답 이벤트)

#### `response.output_text.delta`
- **기능**: 텍스트 응답의 증분 업데이트
- **데이터**: `event.data.delta` (새로 생성된 텍스트 조각)
- **용도**: 실시간 텍스트 출력

#### `response.function_call_arguments.delta`
- **기능**: 함수 호출 인자의 증분 업데이트
- **데이터**: `event.data.delta` (함수 인자 JSON 일부)
- **용도**: 함수 호출 인자 생성 과정 추적

#### `response.completed`
- **기능**: 응답 완료 신호
- **용도**: 현재 응답 종료 알림

---

### 2. `agent_updated_stream_event` (에이전트 업데이트)
- **기능**: 에이전트 전환 이벤트
- **데이터**: `event.new_agent.name` (새 에이전트 이름)
- **용도**: 멀티 에이전트 시스템에서 에이전트 전환 추적

---

### 3. `run_item_stream_event` (실행 아이템 이벤트)

#### `tool_call_item`
- **기능**: 도구 호출 정보
- **데이터**: `event.item.raw_item.to_dict()` (도구 호출 상세)
- **용도**: 호출된 도구 확인

#### `tool_call_output_item`
- **기능**: 도구 실행 결과
- **데이터**: `event.item.output` (실행 결과값)
- **용도**: 도구 실행 결과 추적

#### `message_output_item`
- **기능**: 최종 메시지 출력
- **데이터**: `ItemHelpers.text_message_output(event.item)`
- **용도**: 완성된 메시지 출력

---

### 이벤트 처리 패턴

#### 기본 이벤트 루프
```python
async for event in stream.stream_events():
    if event.type == "raw_response_event":
        # 원본 이벤트 처리
    elif event.type == "agent_updated_stream_event":
        # 에이전트 업데이트 처리
    elif event.type == "run_item_stream_event":
        # 실행 아이템 처리
```

#### 실시간 델타 스트리밍
```python
message = ""
args = ""

async for event in stream.stream_events():
    if event.type == "raw_response_event":
        if event.data.type == "response.output_text.delta":
            message += event.data.delta
            print(message)
        
        elif event.data.type == "response.function_call_arguments.delta":
            args += event.data.delta
            print(args)
        
        elif event.data.type == "response.completed":
            message = ""
            args = ""
```

---

### 이벤트 발생 흐름

#### 함수 호출 시퀀스
1. `response.function_call_arguments.delta` (여러 번 반복)
2. `tool_call_item`
3. `tool_call_output_item`

#### 텍스트 응답 시퀀스
1. `response.output_text.delta` (여러 번 반복)
2. `message_output_item`

#### 완료 시퀀스
- `response.completed`

### Memory
#### SQLiteSession 클래스
- 메모리 구현 지원
- 인자
  - 유저 id
  - db 파일 저장 경로
- 특징
  - 유저별 데이터 관리 가능
  - 지정된 경로에 DB 파일 자동 생성
    - vsc의 SQLite Viewer로 데이터 확인 가능
  - 커스텀 세션 클래스 구현 가능

### handoffs (핸즈오프)
- 에이전트가 위임할 수 있는 서브 에이전트
- 핸즈오프 목록을 제공하면, 상황에 맞게 에이전트가 해당 서브 에이전트로 작업을 위임할 수 있음
- 책임 분리(separation of concerns)와 모듈화(modularity) 가능 — 역할 분담 및 구조화에 유리
- 선택적 위임으로 시스템 유연성 향상

### graphviz
- **기능**: 에이전트 실행 구조를 그래프로 시각화
- **요구사항**:
  - Python 패키지: `graphviz`
  - 시스템 레벨 설치도 필요

### trace
- **기능**: OpenAI Platform에서 에이전트 실행 로그 확인
- **제공**: OpenAI SDK 기본 기능
- **사용법**:
  ```python
  with trace("user_1"):
      # 블록 내 실행 로그에 "user_1" 라벨 자동 부여
  ```

### streamlit
- streamlit 코드는 유저 인터렉션 시 위에서 아래로 실행. 리렌더링 개념과 같음
- 데이터를 지속시키기 위해서는 st.session_state에 저장해야 함