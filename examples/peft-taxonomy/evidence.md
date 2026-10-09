# PEFT taxonomy의 분류 근거

확인일: 2026-10-08. 아래 버전의 초록과 메타데이터를 직접 확인했습니다. 이 표는 주요 적응 메커니즘을 분류하는 데 사용한 범위를 기록하며, 논문 전체 정독·실험 재현·현재 분야 전체 조사를 뜻하지 않습니다.

| ID | 논문과 확인한 버전 | 확인 위치와 사용한 내용 | 지도에서의 위치 |
|---|---|---|---|
| 01 | Ben-Zaken et al., [BitFit](https://arxiv.org/abs/2106.10199v5) | 초록 첫 문장: 모델의 bias 또는 그 일부만 변경합니다. | 기존 파라미터 선택 → bias |
| 02 | Li & Liang, [Prefix-Tuning](https://arxiv.org/abs/2101.00190v1) | 초록: 언어 모델 파라미터를 고정하고 연속적인 task-specific prefix를 최적화합니다. | 새 모듈·벡터 → prefix |
| 03 | Houlsby et al., [Parameter-Efficient Transfer Learning for NLP](https://arxiv.org/abs/1902.00751v2) | 초록: 과제별로 작은 수의 학습 파라미터를 추가하는 adapter modules를 설명합니다. | 새 모듈·벡터 → adapter modules |
| 04 | Liu et al., [Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning](https://arxiv.org/abs/2205.05638v2) | 초록의 (IA)³ 설명: 학습한 벡터로 activation을 scaling합니다. | 새 모듈·벡터 → activation scales |
| 05 | Hu et al., [LoRA](https://arxiv.org/abs/2106.09685v2) | 초록: 기반 가중치를 고정하고 학습 가능한 rank decomposition matrices를 도입합니다. | 가중치 재매개변수화 → low-rank updates |
| 06 | Liu et al., [DoRA](https://arxiv.org/abs/2402.09353v6) | 초록: 가중치를 magnitude와 direction으로 나누며 방향 갱신에 LoRA를 사용합니다. | 가중치 재매개변수화 → magnitude + direction |
| 07 | Dettmers et al., [QLoRA](https://arxiv.org/abs/2305.14314v1) | 초록: 고정된 4-bit 양자화 기반 모델을 통해 LoRA로 gradient를 전달합니다. | 별도 축: 고정 기반의 저장 정밀도 |

그림의 연도는 최초 arXiv 제출 연도입니다. 논문 버전별 수정 연도나 학회 발표 연도와 다를 수 있습니다.

## 분류 기준과 한계

첫 분기는 기존 파라미터 선택, 새 모듈·벡터 추가, 가중치 업데이트의 재매개변수화라는 **주요 개입 방식**입니다. 두 번째 열은 해당 방식에서 학습하는 대상을 설명합니다. 마지막 열은 범주에 속하는 대표 방법입니다. 이는 Human Researcher가 이 예제를 위해 구성한 분류이며 특정 survey의 공식 taxonomy를 재현한 것은 아닙니다.

방법에 부수적인 학습 요소가 함께 있을 수 있으므로 모든 구현을 배타적으로 나누는 표로 사용하지 않습니다. QLoRA는 LoRA와 고정 기반 양자화를 결합하므로 양자화를 별도 축으로 설명했습니다. 이 배치는 다른 방법과의 임의 조합이 구현·검증됐음을 의미하지 않습니다.

분류선은 확인한 주요 메커니즘의 소속을 뜻합니다. 이 예제에서는 인용 관계를 검증하거나 표시하지 않았습니다. 양자화 설정의 조건부 효과를 연구하려면 [별도의 proposal과 검증 계획](../quantized-adaptation/proposal.md)을 확인해 주세요.
