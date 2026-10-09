# RetoVLA proposal의 선행연구와 작성 범위

확인일: **2026-10-09**. [HTML](proposal-reader.html) · [Markdown](proposal.md)

## 문헌을 고른 기준

이 예제는 RetoVLA 연구를 시작하는 관점의 proposal입니다. 알려진 후속 결과를 필요성으로 역산하지 않도록, RetoVLA 최초 공개(2025-09-25) 직전인 **2025-09-24를 편집상 문헌 마감일**로 정하고 그 전에 공개된 버전을 사용했습니다. 실제 연구 착수일이나 당시 작성한 문서라는 뜻은 아닙니다. 현재 분야 전체의 최신 조사·성능 순위·체계적 문헌고찰로 제시하지 않습니다.

질문을 경량 VLA, 명시적 공간 표현, learned-query visual resampler, 행동용 readout tokens, register 개념, 평가 환경으로 나누어 **13편**을 선정했습니다. 선행연구를 지지 사례로만 쓰지 않고, query 집계와 행동용 토큰이 이미 존재한다는 신규성의 제약도 반영했습니다. VLA taxonomy는 이 중 VLM 기반 정책 8편의 행동 출력 설계와 제안 방법을 분류합니다. 시각 정보의 연결 방식은 별도 비교 축입니다. 분류 근거와 경계 사례는 [taxonomy 설명](taxonomy.md)에 적었습니다. 선은 인용이나 역사적 계승이 아닌 범주 소속을 뜻합니다.

## 검색과 접근 기록

- 검색 위치: 웹 검색으로 후보를 찾고 arXiv의 버전별 HTML, 논문 정보, 공식 프로젝트·저장소에서 확인했습니다. 검색 결과 요약만으로 방법 설명을 확정하지 않았습니다.
- 실제 탐색어: `spatial vision language action model efficient spatial tokens SpatialVLA FAST3R SpatialBot 2025 register`, `VLA efficient visual tokens Prismatic OpenVLA Octo Perceiver resampler FastV EfficientVLA 2025`, 그리고 `site:arxiv.org`와 SpatialVLA·TinyVLA·Flamingo·Octo의 논문 제목을 조합했습니다. BLIP-2 원문도 직접 조회했습니다.
- Forward citation: `forward_citations.py 2309.16588 --search robot --from-year 2023 --to-year 2025 --sort oldest --limit 5 --discover-limit 3`을 실행했습니다. 반환 상태는 `partial`입니다. OpenAlex의 제한된 질의에서 관련성이 낮은 X-ray 재구성 후보 1편을 얻었으며, Semantic Scholar 조회 범위도 일부에 한정되었습니다. 해당 후보를 핵심 문헌에 포함하지 않았습니다. arXiv 검색은 HTTP 429로 제한되었습니다. 이 결과를 “로봇 후속 연구가 없다”는 근거로 쓰지 않습니다.
- 원문 가져오기: `fetch_arxiv.py`로 SpatialVLA·TinyVLA·Flamingo를 시도했으나 HTTP 429, Octo·BLIP-2는 timeout으로 원문 저장에 실패했습니다. 웹 도구로 버전이 명시된 arXiv HTML에 접근해 아래 구역을 읽었습니다. 스크립트의 다운로드 성공이나 PDF 시각 검증으로 보고하지 않습니다.
- 포함·제외: 경량 정책의 기반, 가까운 정보 집계 연산, 명시적인 공간 표현 대안, 평가 설계에 직접 영향을 주는 논문을 포함했습니다. 마감일 이후 연구와 읽은 범위를 넘어선 성능·인과 주장은 제안서 근거에서 제외했습니다. 전문 전체, 코드 구현, 모든 관련 연구를 확인한 것은 아닙니다.
- Taxonomy 보강 검색: `site:arxiv.org`와 RT-2·OpenVLA·π₀·OpenVLA-OFT·CogACT의 제목을 조합해 검색한 뒤, 아래 S9–S13의 버전별 HTML 방법 본문을 웹 도구로 확인했습니다. API를 통한 원문 파일 저장이나 구현 재현을 완료했다는 뜻은 아닙니다.
- 이번 보강에서는 방법 본문을 중심으로 확인했습니다. 성능표 숫자 재검산이나 그림의 시각적 분석은 수행하지 않았습니다. 서로 다른 설정의 성공률을 합쳐 순위를 만들지 않았습니다.

## S1 · SmolVLA

- **제목:** SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics.
- **저자·연도:** Mustafa Shukor 외, 2025.
- **버전·원문:** [2506.01844v1](https://arxiv.org/html/2506.01844v1).
- **확인 범위:** 초록, §3.1 Model architecture, §4.3 Implementation details, §5.1 Limitations의 HTML 본문.
- **사용:** 기존 특징과 flow-matching Action Expert의 연결, 고정 VLM과 학습 recipe를 출발점으로 사용합니다.
- **한계:** 모든 경량 모델의 공간 관계 실패나 RetoVLA의 효과·장비 처리량을 입증하지 않습니다.

## S2 · Vision Transformers Need Registers

- **제목:** Vision Transformers Need Registers.
- **저자·연도:** Timothée Darcet, Maxime Oquab, Julien Mairal, Piotr Bojanowski, 2023.
- **버전·원문:** [2309.16588v2](https://arxiv.org/html/2309.16588v2).
- **확인 범위:** 초록, §2.2 Hypothesis and remediation, §3.4 Qualitative evaluation of registers; Fig. 6·9는 캡션만 확인.
- **사용:** ViT 입력의 내부 계산용 토큰이라는 아이디어를 설명하고, feature 뒤의 query 집계와 구분합니다.
- **한계:** 원 방법의 삽입 위치와 학습 목적이 다릅니다. 이 제안의 토큰이 3D 구조를 담거나 조작을 개선한다는 근거가 아닙니다.

## S3 · LIBERO

- **제목:** LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning.
- **저자·연도:** Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, Peter Stone, 2023.
- **버전·원문:** [2306.03310 · NeurIPS 2023](https://arxiv.org/abs/2306.03310) · [공식 저장소](https://github.com/Lifelong-Robot-Learning/LIBERO).
- **확인 범위:** 논문 초록, 공식 저장소 README의 benchmark 설명·Datasets·Getting Started/Task; 본문 전체·원시 데이터 미확인.
- **사용:** 조작 시연, task suite 구분과 초기 상태를 사용하는 평가 경로를 확인합니다.
- **한계:** 제안한 seed 수·평가 정밀도·실행 시간을 보장하지 않습니다. 본 제안의 최소 실험은 lifelong learning 평가가 아닙니다.

## S4 · TinyVLA

- **제목:** TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation.
- **저자·연도:** Junjie Wen 외, 2024.
- **버전·원문:** [2409.12514v3](https://arxiv.org/html/2409.12514v3).
- **확인 범위:** 초록·Introduction, §III-A Building TinyVLA with Efficient Vision-Language Models, §III-B Robot Data Finetuning for Manipulation의 HTML 본문.
- **사용:** 작은 VLM, LoRA 적응, diffusion decoder 연결을 확인해 경량 모델 자체를 결함으로 전제하지 않습니다.
- **한계:** 데이터와 backbone·학습 조건이 달라 보고 성공률을 SmolVLA 기반 A/B/C와 직접 비교하지 않습니다.

## S5 · SpatialVLA

- **제목:** SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Models.
- **저자·연도:** Delin Qu 외, 2025.
- **버전·원문:** [2501.15830v1](https://arxiv.org/html/2501.15830v1).
- **확인 범위:** 초록, §III-A The SpatialVLA Model Architecture, §III-B The Pre-training and Post-training Scheme의 HTML 본문.
- **사용:** ZoeDepth와 카메라 내부 파라미터를 이용한 Ego3D encoding, Adaptive Action Grids를 기존 RGB 특징의 요약 경로와 대비합니다.
- **한계:** 변경하는 구성 요소를 비교한 것입니다. 비용 우위나 같은 조건의 성능 우위는 확인하지 않았습니다.

## S6 · Flamingo

- **제목:** Flamingo: a Visual Language Model for Few-Shot Learning.
- **저자·연도:** Jean-Baptiste Alayrac 외, 2022.
- **버전·원문:** [2204.14198v2](https://arxiv.org/html/2204.14198v2).
- **확인 범위:** §2.1 Visual processing and the Perceiver Resampler, §2.2 Conditioning frozen language models on visual representations, §A.1.1 Perceiver Resampler의 HTML 본문.
- **사용:** 학습 가능한 latent queries로 시각 특징을 모으고 gated cross-attention으로 언어 모델을 조건화하는 선행을 확인합니다.
- **한계:** 로봇 행동 실험은 아닙니다. 원 resampler는 latent의 K/V도 함께 참조하므로 현재의 단순 집계식과 동일한 구현으로 간주하지 않습니다.

## S7 · BLIP-2

- **제목:** BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models.
- **저자·연도:** Junnan Li, Dongxu Li, Silvio Savarese, Steven Hoi, 2023.
- **버전·원문:** [2301.12597v3](https://arxiv.org/html/2301.12597v3).
- **확인 범위:** 초록, §3.1 Model Architecture, §3.3 Bootstrap Vision-to-Language Generative Learning from a Frozen LLM의 HTML 본문.
- **사용:** Q-Former가 고정 이미지 특징에서 query 표현을 추출하고 LLM의 visual prompts로 전달하는 방식을 확인합니다.
- **한계:** 언어 생성용 사전학습과 Action Expert의 행동 학습은 다릅니다. Query 집계 자체의 최초성을 주장할 수 없습니다.

## S8 · Octo

- **제목:** Octo: An Open-Source Generalist Robot Policy.
- **저자·연도:** Octo Model Team 외, 2024.
- **버전·원문:** [2405.12213v2](https://arxiv.org/html/2405.12213v2).
- **확인 범위:** 초록, §III-A Architecture의 Task and observation tokenizers 및 Transformer backbone and readout heads의 HTML 본문.
- **사용:** 관측·과제 토큰을 읽는 readout tokens와 diffusion action head의 연결을 가까운 로봇 정책 선행으로 둡니다.
- **한계:** Backbone·입력 구성·사전학습이 다른 정책입니다. 소수 토큰의 행동 연결이라는 공통점만으로 동일한 방법이나 직접 성능 비교로 취급하지 않습니다.

## S9 · RT-2

- **제목:** RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control.
- **저자·연도:** Anthony Brohan 외, 2023.
- **버전·원문:** [2307.15818v1](https://arxiv.org/html/2307.15818v1).
- **확인 범위:** §3.2 Robot-Action Fine-tuning의 HTML 본문.
- **사용:** 연속 행동 차원을 균등 bin으로 나누고 토큰으로 예측하는 방식을 taxonomy에 배치합니다.
- **한계:** 확인한 RT-2 변형의 행동 표현에 대한 분류입니다. 모든 VLA나 후속 변형의 출력 방식을 뜻하지 않습니다.

## S10 · OpenVLA

- **제목:** OpenVLA: An Open-Source Vision-Language-Action Model.
- **저자·연도:** Moo Jin Kim 외, 2024.
- **버전·원문:** [2406.09246v1](https://arxiv.org/html/2406.09246v1).
- **확인 범위:** §3.2 OpenVLA Training Procedure의 HTML 본문.
- **사용:** 행동 차원별 256-bin 양자화와 next-token prediction을 원본 OpenVLA의 분류 근거로 사용합니다.
- **한계:** 원본 모델의 분류입니다. 연속 회귀로 바뀐 OpenVLA-OFT까지 같은 가지에 넣지 않습니다.

## S11 · π₀

- **제목:** π₀: A Vision-Language-Action Flow Model for General Robot Control.
- **저자·연도:** Kevin Black 외, 2024.
- **버전·원문:** [2410.24164v1](https://arxiv.org/html/2410.24164v1).
- **확인 범위:** §IV The π₀ Model의 HTML 본문과 conditional flow matching 수식 설명.
- **사용:** VLM과 별도 Action Expert를 이용하는 연속 action chunk 생성을 flow matching 가지에 배치합니다.
- **한계:** π₀ 기본 설계의 분류이며 이름이 비슷한 다른 행동 토큰화 변형까지 묶지 않습니다. RetoVLA의 효과를 입증하지 않습니다.

## S12 · OpenVLA-OFT

- **제목:** Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success.
- **저자·연도:** Moo Jin Kim, Chelsea Finn, Percy Liang, 2025.
- **버전·원문:** [2502.19645v2](https://arxiv.org/html/2502.19645v2).
- **확인 범위:** 초록, §IV-A VLA Fine-Tuning Design Decisions, §IV-B Implementing Alternative Design Components의 HTML 본문.
- **사용:** 최종 OFT recipe의 parallel decoding·action chunking·continuous actions·L1 regression을 직접 회귀 가지의 근거로 사용합니다.
- **한계:** 논문에서 비교한 diffusion·이산 출력 대조군은 별도 변형입니다. OFT의 채택 recipe와 혼동하지 않습니다.

## S13 · CogACT

- **제목:** CogACT: A Foundational Vision-Language-Action Model for Synergizing Cognition and Action in Robotic Manipulation.
- **저자·연도:** Qixiu Li 외, 2024.
- **버전·원문:** [2411.19650v1](https://arxiv.org/html/2411.19650v1).
- **확인 범위:** §3.1 Vision and Language Modules, §3.2 Diffusion Action Module의 HTML 본문.
- **사용:** VLM의 cognition token 표현을 DiT action module에 전달하는 구조를 diffusion 가지와 가까운 조건화 선행으로 사용합니다.
- **한계:** 통합된 시각·언어 특징의 단일 cognition token과 이 제안의 이미지 query 요약은 같은 연산이 아닙니다. 효과 비교는 별도입니다.

## 제안서 작성 배경 — 선행연구 근거와 구분합니다

사용자는 RetoVLA 연구를 위한 proposal 예제를 요청했습니다. 방법의 정체성은 사용자의 공개 논문 [RetoVLA: Reusing Register Tokens for Spatial Reasoning in Vision-Language-Action Models](https://arxiv.org/abs/2509.21243v2), 특히 §III-C의 설계를 참고해 유지했습니다. 실제 과거 proposal를 복원한 문서가 아니며, 이 작업이 이미 발표된 연구의 신규성을 다시 주장하지 않습니다.

**RetoVLA 자체의 성능표·결과 해석·채택 사실은 proposal의 필요성·효과 근거와 결과 구역에서 제외했습니다.** 가설·대조군·판정 기준·일정·계산 예산은 연구를 계획하는 형식으로 작성했습니다. 알고 있는 결과를 기준으로 역산한 목표 성공률을 넣지 않았습니다.

장비 기준은 사용자 지정에 따라 **NVIDIA GeForce RTX 5090 GPU 1개**로 정했습니다. 해당 장비의 메모리 사용량·학습 처리량·평가 시간은 아직 실측하지 않았습니다.

K=2와 마지막 cross-attention이라는 방법 후보, δ=5%p·비용 한도, 9회 학습·4,500회 정책 평가·540회 관계 진단, 5–7주와 GPU 시간 산식은 모두 **예제의 제안 설정**입니다. 실제 가용 자원·승인된 실험·관측 결과가 아닙니다. 학습 recipe의 출발점만 S1에서 확인했습니다. 실행 전에 pilot·자원·정밀도를 확인하고 조건을 고정해야 합니다.

가까운 query·resampler·readout 문헌을 포함한 13편의 관련 부분을 확인했습니다. 구현 수준의 중복 여부와 동일 조건 비교는 별도 검증이 필요합니다. 비공개 후속 연구 자료를 포함하지 않았습니다.

## 예제의 출처와 형식

RetoVLA는 원 논문 전체 저자의 공동 연구입니다. 이 예제는 공개된 설계를 제안서 형식으로 재구성한 것이며, Human Researcher가 원 논문을 작성했다는 의미는 아닙니다.

HTML은 [reader 지침](../../skills/write-proposal/references/proposal-reader.md)에 맞춘 편집 가능한 문서입니다. 도식은 제안한 정보 경로와 검증을 설명하며 실제 결과 그래프를 포함하지 않습니다. HTML과 Markdown의 방법·예산·판정 기준을 함께 갱신합니다.
