# 연구의 논리를 보여주는 시각화 갤러리

[프로젝트 소개](../README.md) · [연구 철학](../docs/philosophy.md) · [사용 가이드](../docs/guide.md)

**분야의 구조, 내 질문, 검증 방법, 다음에 논의할 결정까지 눈에 보이게 만듭니다.** 아래는 공개 논문 또는 합성 자료를 바탕으로 검토·편집한 예제입니다. 계획과 논문의 보고값을 구분하며, 스킬 성능 측정치로 제시하지 않습니다.

## 이 아이디어로 연구를 시작한다면 · RetoVLA proposal

[![작은 로봇 모델의 장면 요약을 행동 생성까지 연결하는 RetoVLA 예제](../docs/assets/retovla-reader-preview.png)](retovla/proposal-reader.html)

경량 VLA에 register 기반 장면 요약을 연결하는 연구를 제안합니다. 선행연구 13편, VLA taxonomy, 가설·비교군·결과별 판단과 RTX 5090 1개 기준의 조건부 견적을 담았습니다. 완료된 RetoVLA 결과를 근거로 효과를 미리 결론 내리지 않습니다. 실제 과거 proposal를 복원한 문서는 아닙니다.

[![VLA 대표 정책 8편과 RetoVLA의 위치를 보여주는 계층형 taxonomy](retovla/taxonomy.svg)](retovla/taxonomy.md)

[HTML 읽기 화면](retovla/proposal-reader.html) · [예제 안내와 요청 방법](retovla/README.md) · [수정용 Markdown](retovla/proposal.md) · [출처와 제작 기록](retovla/sources.md)

## 01 · 분야의 구조를 그립니다

[![PEFT의 주요 메커니즘을 보여주는 계층형 taxonomy](../docs/assets/peft-taxonomy-preview.png)](peft-taxonomy/README.md)

실제 논문 7편을 주요 학습 대상에 따라 분류합니다. 범주와 대표 방법을 구분하고, QLoRA의 기반 양자화는 다른 분류 축으로 표시합니다.

[예제와 요청 방법](peft-taxonomy/README.md) · [SVG](peft-taxonomy/taxonomy.svg) · [논문별 분류 근거](peft-taxonomy/evidence.md)

## 02 · 연구 계획을 한 장에 설명합니다

[![LoRA·QLoRA에서 출발한 메모리 비교 연구의 A3 proposal 포스터](../docs/assets/adaptation-proposal-preview.png)](quantized-adaptation/poster.pdf)

같은 어댑터에서 고정 기반의 정밀도를 바꾸면 무엇을 알 수 있을까요? 문헌 근거, 공정한 비교, 측정, 가능한 결론과 미정인 입력을 한 장에 연결합니다.

[PDF](quantized-adaptation/poster.pdf) · [편집 가능한 HTML](quantized-adaptation/poster.html) · [SVG](quantized-adaptation/poster.svg) · [전체 proposal](quantized-adaptation/proposal.md)

## 03 · 실험을 다음 결정으로 연결합니다

[![계획한 비교와 측정에서 메모리·품질·불확실성·OOM별 판단으로 갈라지는 검증 지도](../docs/assets/evaluation-map-preview.png)](quantized-adaptation/evaluation.svg)

메모리만 줄었다고 성공으로 결론 내리지 않습니다. 품질 기준을 충족하는 경우, 충족하지 못하는 경우, 불확실성이 큰 경우와 한 조건이 실행되지 않는 경우를 구분합니다. [Proposal의 결과 해석](quantized-adaptation/proposal.md#interpreting-outcomes)을 시각화했습니다.

[SVG](quantized-adaptation/evaluation.svg) · [문헌 근거](quantized-adaptation/sources.md)

## 04 · 미완성 초안을 좋은 미팅으로 이어갑니다

[![도서관 안내 문구 연구의 미해결 쟁점을 지도교수에게 물을 구체적인 질문으로 바꾼 미팅 브리프](../docs/assets/meeting-brief-preview.png)](research-meeting/README.md)

가상의 도서관 안내 문구 연구입니다. 문구의 효과를 어떻게 분리할지, 무엇을 측정할지, 어느 범위에서 시작할지를 논의합니다. 질문마다 그 답이 바꿀 결정을 붙였습니다.

[예제와 요청 방법](research-meeting/README.md) · [SVG](research-meeting/brief.svg) · [합성 원본 메모](../tests/fixtures/meeting-notes.md)

## 05 · 전체 proposal과 근거를 브라우저에서 읽습니다

[전체 proposal HTML](quantized-adaptation/proposal-reader.html)은 같은 연구 계획의 필요성·변경점·검증·자원을 차례로 보여줍니다. 인용된 논문 제목을 누르면 원문 링크와 읽은 범위, 이 연구에 사용하는 이유가 보입니다. 내려받아 브라우저에서 열어 주세요. 화면 크기에 맞춰 읽을 수 있으며, 인쇄에는 접힌 세부 내용도 포함합니다.

[Markdown 원문](quantized-adaptation/proposal.md) · [출처 메모](quantized-adaptation/sources.md) · [HTML 요청 방법](../docs/guide.md#브라우저에서-읽고-근거를-따라가고-싶을-때)

## 다른 형태도 필요하신가요?

[혼합형·미확인 문헌을 다루는 가상 taxonomy](visual-taxonomy/README.md)도 함께 제공합니다. 제안한 방법을 기존 가지 옆에 놓고, 정보가 부족한 문헌을 트리 밖에 남기는 예제입니다.

지금 필요한 작업과 출력 형식을 알려 주세요. 모든 그림을 한 proposal에 넣을 필요는 없습니다. PNG는 미리보기이며, 편집과 확대에는 SVG·HTML을 사용하시면 됩니다. [제작 기록과 재생성 방법](../docs/assets/README.md)에서 원본과 렌더링 경로를 확인하실 수 있습니다.
