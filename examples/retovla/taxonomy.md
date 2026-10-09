# VLA taxonomy — 행동 표현과 생성 방식

[SVG로 보기](taxonomy.svg) · [제안서 HTML](proposal-reader.html#taxonomy) · [전체 출처](sources.md)

![VLM 기반 VLA의 행동 표현·생성 방식 taxonomy](taxonomy.svg)

## 분류 기준

이 그림은 **사전학습 VLM을 로봇 조작 정책에 활용하는 대표 VLA**를 대상으로, 정책이 저수준 행동을 어떻게 출력하는지 설명합니다. 2025-09-24 이전 공개 버전의 정책 8편과 RetoVLA 제안 방법을 배치했습니다. 원문 확인일은 2026-10-09입니다. 기존 survey의 공식 분류를 옮긴 것이 아니라 이 proposal의 비교 질문을 위해 합성한 분류입니다.

첫 분기는 행동 출력 표현입니다. **이산 행동 토큰**을 예측하는지, **연속 행동값**을 생성하는지 나눕니다. 그다음 이산 계열에서는 양자화 방식을, 연속 계열에서는 실제 생성 연산을 나눕니다. 모델군 전체가 아니라 읽은 논문의 명시된 변형을 분류합니다.

- 실선은 **범주 소속**입니다. 인용·역사적 계승·성능 우위를 뜻하지 않습니다.
- 점선 테두리와 `PROPOSED` 표시는 **검증할 제안 방법**입니다.
- Flow matching과 diffusion은 관련 있는 생성 방법입니다. 여기서는 각 논문의 학습 목표·출력 절차를 구별하려고 나눴으며, 이론적으로 완전히 별개의 집합이라고 주장하지 않습니다.
- 경량화·공간 정보 주입·메모리·요약 토큰은 출력 방식과 교차하는 별도 축입니다. 이를 같은 깊이의 배타적인 가지로 섞지 않았습니다.

## 텍스트 트리

```text
VLM 기반 VLA
├── 이산 행동 토큰
│   ├── 행동 차원별 양자화
│   │   ├── RT-2 (S9)
│   │   └── OpenVLA (S10, 원본)
│   └── 공간 구조 기반 양자화
│       └── SpatialVLA (S5)
└── 연속 행동
    ├── 직접 회귀 · L1
    │   └── OpenVLA-OFT (S12, 채택 recipe)
    ├── Diffusion
    │   ├── TinyVLA (S4)
    │   └── CogACT (S13)
    └── Flow matching
        ├── π₀ (S11, 기본 모델)
        ├── SmolVLA (S1)
        └── RetoVLA (제안 방법)
```

## 배치 근거

| 모델 · 버전 | 분류 경로 | 확인한 위치와 근거 |
|---|---|---|
| [RT-2](https://arxiv.org/html/2307.15818v1) · Brohan 외, 2023 · S9 | 이산 → 행동 차원별 양자화 | §3.2: 연속 행동 차원을 균등한 256 bins로 나누고 행동 토큰으로 표현합니다 |
| [OpenVLA](https://arxiv.org/html/2406.09246v1) · Kim 외, 2024 · S10 | 이산 → 행동 차원별 양자화 | §3.2: 차원별 256 bins 및 next-token prediction을 사용합니다 |
| [SpatialVLA](https://arxiv.org/html/2501.15830v1) · Qu 외, 2025 · S5 | 이산 → 공간 구조 기반 양자화 | §III-A: translation·rotation의 Adaptive Action Grids와 autoregressive spatial action tokens를 사용합니다 |
| [OpenVLA-OFT](https://arxiv.org/html/2502.19645v2) · Kim 외, 2025 · S12 | 연속 → 직접 회귀 | 초록·§IV-A·B: 채택한 OFT recipe는 parallel decoding, action chunking, continuous representation, L1 regression입니다 |
| [TinyVLA](https://arxiv.org/html/2409.12514v3) · Wen 외, 2024 · S4 | 연속 → diffusion | §III-B: VLM 표현을 diffusion policy decoder에 연결합니다 |
| [CogACT](https://arxiv.org/html/2411.19650v1) · Li 외, 2024 · S13 | 연속 → diffusion | §3.1·3.2: cognition feature를 조건으로 DiT가 여러 단계로 action sequence를 생성합니다 |
| [π₀](https://arxiv.org/html/2410.24164v1) · Black 외, 2024 · S11 | 연속 → flow matching | §IV: Action Expert가 conditional flow matching으로 연속 action chunk를 생성합니다 |
| [SmolVLA](https://arxiv.org/html/2506.01844v1) · Shukor 외, 2025 · S1 | 연속 → flow matching | §3.1: VLM 특징과 flow-matching Action Expert를 연결합니다 |
| [RetoVLA 제안](proposal.md) | 연속 → flow matching | 이 예제의 §3: SmolVLA 행동 생성기를 유지하고 이미지 특징의 query 요약 경로를 추가하는 계획입니다. 결과에 근거한 분류가 아닙니다 |

분류에 사용한 방법 본문을 읽었으며 모델을 구현·실행하거나 원 논문의 성능을 재현한 것은 아닙니다. 이 표에 없는 방법이 존재하지 않는다는 뜻도 아닙니다.

## 경계 사례와 연구의 위치

**OpenVLA와 OpenVLA-OFT는 다른 가지에 놓입니다.** 계보와 이름이 이어져도 채택한 행동 출력 연산이 바뀌기 때문입니다. OFT 논문 안의 diffusion 대조군은 여기서 표시한 최종 L1 recipe와 별개입니다. π₀도 이름을 공유하는 다른 tokenization 변형까지 flow matching으로 묶지 않습니다. 여러 출력을 함께 사용하는 hybrid 정책을 추가할 때에는 실제 출력 경로에 따라 복수 소속이나 별도 표시가 필요합니다.

[Octo](https://arxiv.org/html/2405.12213v2)는 시각·언어 조건을 사용하는 중요한 로봇 정책이지만, 여기서 정한 **사전학습 VLM 기반 정책**의 주 트리 대신 readout token 관련 선행으로 다룹니다. [Flamingo](https://arxiv.org/html/2204.14198v2)·[BLIP-2](https://arxiv.org/html/2301.12597v3)·[Vision Transformers Need Registers](https://arxiv.org/html/2309.16588v2)는 표현·연결 모듈의 기반 연구이며 VLA 정책의 잎에 넣지 않았습니다. [LIBERO](https://arxiv.org/abs/2306.03310)는 평가 환경입니다.

RetoVLA의 직접적인 비교 이웃은 **SmolVLA**입니다. 차이는 새 행동 생성 원리가 아니라, 이미지 특징의 query 요약을 기존 Action Expert에 추가 전달하는 경로입니다. CogACT의 cognition feature와 Octo의 readout tokens도 함께 검토해야 하는 가까운 조건화 선행입니다. 따라서 이 트리에서 새 잎을 그렸다는 사실이 신규성이나 유용성을 증명하지 않습니다. 본문 A/B/C 비교로 같은 backbone에서 그 경로가 필요한지 검증합니다.
