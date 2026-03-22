---
name: geocoding
description: Nominatim 기반 주소↔좌표 변환 및 위치 검색 (API 키 불필요)
enabled: true
version: 1.0.0
tags: geo, location
---

## 지오코딩 도구

OpenStreetMap Nominatim API를 사용하여 주소를 좌표로, 좌표를 주소로 변환합니다.

### 사용 가능한 도구

- **geocode_address**: 주소/장소명 → 위도·경도 변환
- **geocode_reverse**: 위도·경도 → 주소 변환

### 사용법

- 한국어 주소, 영어 주소 모두 지원
- 부동산, 날씨, 환경 분석 등의 전처리 단계로 사용
