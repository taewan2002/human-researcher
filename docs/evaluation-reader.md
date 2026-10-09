# HTML 읽기 화면과 근거 표기 검증

2026-10-09에 추가한 HTML proposal, 출처 카드, 직관적인 비교 설명의 개발 검증 기록입니다. [이전 검증](evaluation-v0.1.0.md)을 대체하거나 이전 45개 사례를 모두 재실행한 기록은 아닙니다. 저장소에는 새 사례 4개를 포함해 49개 행동 사례가 있습니다.

## 이번에 확인한 동작

- 한국어 proposal을 실제 HTML·Markdown 파일로 만들고, 연구의 필요성·변경점·고정 조건·검증을 연결합니다.
- 같은 저자·연도의 서로 다른 논문을 제목·버전·원문 링크로 구분합니다. 인용 관계의 양쪽 논문과 읽은 근거로 돌아갈 수 있어야 합니다.
- URL이 없는 초록은 링크·DOI·본문 위치를 만들어 채우지 않습니다.
- 세 문장의 텍스트만 요청하면 파일·표·그림을 강제하지 않습니다.

픽스처는 합성 자료입니다. 실행 모델에는 요청과 원자료, 해당 스킬만 주고 판정 기준은 숨겼습니다. 외부 검색 없이 Read·Glob·Grep·Write·Edit를 사용했으며 실제 도구 출력에 생성된 HTML과 Markdown을 수집했습니다. 실행은 네이티브 Claude Code 2.1.294의 `claude-sonnet-5-5`, `claude-opus-5-5`, effort low이며, 별도 Codex CLI `gpt-6-astra`, low가 기준별 판정을 수행했습니다. 이번에는 스킬 사용 조건의 회귀 검사만 실행했습니다. 스킬 유무의 효과 비교가 아닙니다.

## 최초 실패와 재검사

숫자는 모든 기준을 통과한 사례 수 / 실행한 사례 수입니다. 서로 다른 단계의 숫자를 합쳐 성공률로 제시하지 않습니다.

| 단계 | Sonnet 5.5 | Opus 5.5 |
|---|---:|---:|
| 새 4개 사례 최초 실행 | 3/4 | 2/4 |
| 관련 지침 수정 후 선택 재검사 | 1/2 | 2/3 |

- 첫 Sonnet HTML은 가상의 링크임을 표시했지만 논문 자체가 합성 자료라는 표시가 충분하지 않아 출처 기준에서 실패했습니다. 출처의 성격을 유지하도록 명시한 뒤 재검사에서는 해당 기준을 통과했습니다.
- 첫 Opus 읽기 목록은 후속 논문의 URL만 포함하고 기준 논문의 URL을 빠뜨렸습니다. 인용 관계의 양쪽 링크를 명시한 뒤 해당 사례를 통과했습니다.
- **남은 실패:** Sonnet의 재검사 HTML은 정밀도가 부족할 때 판단을 유보하는 결과 해석을 빠뜨렸습니다. Opus는 세 문장 제한을 최초·재검사 모두 위반했고, 제공 자료에 없는 날짜 결측의 빈도를 일반 사실처럼 표현했습니다. 관련 지침을 넣는 것만으로 이러한 행동이 보장되지 않습니다.
- Sonnet의 세 문장 요청과 두 모델의 URL 없는 paper card는 통과했습니다. Opus의 HTML 사례는 두 단계 모두 텍스트 판정 6개 기준을 통과했습니다.

원래 실패 판정을 유지합니다. 사례별 한 번의 실행이며 출력·판정의 변동을 추정하지 않았습니다. 자동 채점은 연구 품질이나 화면 가독성의 검증을 대신하지 않습니다. description은 바꾸지 않았으므로 이번에 라우팅 평가는 다시 실행하지 않았습니다.

## 실제 파일 확인

[공개 HTML 예제](../examples/quantized-adaptation/proposal-reader.html)는 기존 [Markdown proposal](../examples/quantized-adaptation/proposal.md)과 [출처 메모](../examples/quantized-adaptation/sources.md)를 바탕으로 직접 편집한 예제입니다. 모델이 한 번에 만든 결과나 성능 사례로 제시하지 않습니다.

- Chrome에서 1440px·390px 너비를 확인했습니다. 페이지 전체의 가로 넘침, 누락된 내부 링크 대상, 남은 템플릿 자리표시자가 없었습니다. 외부 폰트·스크립트·이미지 요청 없이 로컬 파일로 열렸습니다.
- 방법 비교와 모바일 출처 카드, 인쇄된 전체 페이지를 시각적으로 확인했습니다. 최종 예제의 A4 인쇄본은 **5쪽**이며, 접힌 통제·측정 설명과 두 논문의 원문 URL이 포함됐습니다. 전체 proposal용 형식이므로 한 쪽으로 강제하지 않습니다.
- 두 실제 arXiv 링크는 이번 HEAD 요청에서 HTTP 200과 기대한 HTML/PDF 형식을 반환했습니다. 이는 링크 확인이며 원문 전체를 새로 읽거나 주장을 재검증한 것은 아닙니다. 읽은 범위는 기존 출처 메모의 날짜를 유지합니다.
- Claude의 최초·재검사 HTML은 별도로 화면 너비·내부 링크·외부 의존성·인쇄 스타일을 확인했습니다. 과학적 내용의 남은 실패와 화면 구조 검사는 별개입니다. Safari·Firefox와 실제 휴대폰에서는 검사하지 않았습니다.
- 구조 검증, 단위 테스트 64개, Codex·Claude Code용 8개 패키지의 임시 설치와 바이트 일치를 확인했습니다.

## 재현 자료

[추가 실행 기록](https://github.com/taewan2002/human-researcher/releases/download/v0.1.0/human-researcher-v0.1.0-reader-checks.tar.gz) · [SHA-256](https://github.com/taewan2002/human-researcher/releases/download/v0.1.0/human-researcher-v0.1.0-reader-checks.tar.gz.sha256)

압축 파일에는 각 단계의 입력·스킬 스냅샷·출력·실제 파일·판정·해시와 브라우저 확인 기록을 넣었습니다. `release-skills/`와 manifest는 이번 HTML 개선을 포함한 최종 패키지를 식별합니다. 기존 평가 압축 파일은 HTML 개선 전 스냅샷으로 계속 보존합니다. 인증 정보와 호스트 진단·세션 초기화 로그는 포함하지 않습니다.

```sh
python3 scripts/evaluate.py --engine claude --model sonnet \
  --run-dir eval-runs/reader-reproduction --conditions with_skill \
  --cases browser-readable-proposal recognizable-paper-card \
  recognizable-citation-list text-only-proposal-section
```

이 명령은 새 실행을 만들며 모델의 기존 로그인과 사용량을 사용합니다. 같은 결과를 보장하지 않으며, 모델이 생성한 HTML의 화면·인쇄 상태는 별도로 확인해야 합니다.
