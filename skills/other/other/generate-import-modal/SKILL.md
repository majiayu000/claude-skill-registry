---
name: generate-import-modal
description: Excel 가져오기 모달의 보일러플레이트를 자동 생성합니다. useExcelImport 훅 기반. 새 가져오기 기능 추가 시 사용.
argument-hint: "[도메인 이름 (예: 'attendance', 'homework')]"
---

## Purpose

새로운 Excel 가져오기 모달을 프로젝트 표준 패턴에 맞춰 자동 생성합니다:

1. **모달 컴포넌트 생성** — `useExcelImport` 훅을 사용하는 가져오기 모달
2. **파서 함수 생성** — xlsx 필드 매핑 및 정규화 로직
3. **타입 정의** — 파싱된 행의 TypeScript 인터페이스
4. **부모 컴포넌트 연동 안내** — 모달 열기/닫기 및 onImport 콜백 연결

## When to Run

- 새 도메인에 Excel 가져오기 기능을 추가할 때
- 기존 가져오기 모달을 `useExcelImport` 훅 기반으로 리팩토링할 때

## Related Files

| File | Purpose |
|------|---------|
| `hooks/useExcelImport.ts` | Excel 가져오기 공통 훅 (파일 읽기, 상태 관리, 가져오기 실행) |
| `components/Textbooks/TextbookImportModal.tsx` | 참조 구현: 교재 수납 가져오기 |
| `components/Billing/BillingImportModal.tsx` | 참조 구현: 수납 데이터 가져오기 |
| `components/StudentManagement/StudentMigrationModal.tsx` | 참조 구현: 학생 마이그레이션 |
| `utils/studentMatching.ts` | 학생 매칭 유틸 (가져오기 시 학생 DB 매칭이 필요한 경우 사용) |

## Workflow

### Step 1: 사용자 입력 수집

`AskUserQuestion`을 사용하여 다음을 확인합니다:

1. **도메인 이름** (예: `attendance`, `homework`, `shuttle`)
2. **Excel 필드 매핑** — 어떤 열을 읽을지 (예: 이름, 학년, 학교, 점수)
3. **필터 조건** (선택) — 특정 행만 가져올지 (예: 구분 === '교재')
4. **학생 매칭 필요 여부** — `studentMatching.ts` 연동 필요 여부
5. **소속 탭** — 이 모달이 열리는 탭 컴포넌트 이름

### Step 2: 타입 정의 생성

파싱된 행의 인터페이스를 모달 파일 상단에 정의합니다:

```typescript
export interface <PascalCase>ImportRow {
  // 사용자가 지정한 필드들
  studentName: string;
  grade: string;
  // ...
  // 학생 매칭이 필요한 경우:
  matched: boolean;
  studentId?: string;
}
```

### Step 3: 모달 컴포넌트 생성

**파일:** `components/<PascalCase>/<PascalCase>ImportModal.tsx`

**프로젝트 표준 구조:**

```tsx
import React, { useMemo } from 'react';
import { X, Upload, FileSpreadsheet, Loader2, AlertCircle, Check, RotateCcw, Eye } from 'lucide-react';
import { useExcelImport } from '../../hooks/useExcelImport';

// 1. 타입 정의
export interface <PascalCase>ImportRow {
  // ...fields
}

// 2. Props 정의
interface <PascalCase>ImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onImport: (rows: <PascalCase>ImportRow[]) => Promise<{ added: number; skipped: number }>;
  // 학생 매칭이 필요한 경우:
  // studentIds?: Set<string>;
}

// 3. 파서 함수 (또는 컴포넌트 내부 useCallback)
function parse<PascalCase>Rows(rows: Record<string, any>[]): <PascalCase>ImportRow[] {
  return rows
    // .filter(row => ...)  // 필터 조건이 있는 경우
    .map(row => ({
      // 필드 매핑
    }));
}

// 4. 컴포넌트
export const <PascalCase>ImportModal: React.FC<<PascalCase>ImportModalProps> = ({
  isOpen,
  onClose,
  onImport,
}) => {
  const {
    fileInputRef,
    parsedData,
    fileName,
    isImporting,
    importResult,
    handleFileChange,
    handleImport,
    handleReset,
    openFileDialog,
    isParsed,
    isComplete,
  } = useExcelImport({
    parser: parse<PascalCase>Rows,
    onImport,
  });

  // 통계 요약 (useMemo)
  const summary = useMemo(() => {
    if (!isParsed) return null;
    return {
      totalRecords: parsedData.length,
      // ... 도메인별 통계
    };
  }, [parsedData, isParsed]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-start justify-center pt-[8vh] z-[100]" onClick={onClose}>
      <div className="bg-white rounded-sm w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="flex items-center justify-between px-3 py-2 border-b border-gray-200">
          <h2 className="text-sm font-bold text-primary flex items-center gap-2">
            <FileSpreadsheet size={18} className="text-emerald-600" />
            <도메인명> 데이터 가져오기
          </h2>
          <button onClick={onClose} className="p-1 rounded-sm hover:bg-gray-100 text-gray-400 hover:text-gray-600">
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-auto p-6 space-y-2">
          {/* 파일 업로드 섹션 */}
          <div className="bg-white border border-gray-200 overflow-hidden">
            <div className="flex items-center gap-1 px-2 py-1.5 bg-gray-50 border-b border-gray-200">
              <Upload className="w-3 h-3 text-primary" />
              <h3 className="text-primary font-bold text-xs">파일 업로드</h3>
            </div>
            <div className="p-3">
              <input ref={fileInputRef} type="file" accept=".xlsx,.xls" onChange={handleFileChange} className="hidden" />
              <div className="flex items-center gap-3">
                <button
                  onClick={openFileDialog}
                  className="flex items-center gap-2 px-4 py-2 border-2 border-dashed border-gray-300 rounded-sm hover:border-emerald-500 hover:bg-emerald-50 transition-colors text-sm"
                >
                  <FileSpreadsheet className="w-4 h-4" />
                  Excel 파일 선택
                </button>
                {fileName && <span className="text-sm text-gray-600 font-medium">{fileName}</span>}
              </div>
            </div>
          </div>

          {/* 데이터 미리보기 섹션 */}
          {summary && (
            <div className="bg-white border border-gray-200 overflow-hidden">
              <div className="flex items-center gap-1 px-2 py-1.5 bg-gray-50 border-b border-gray-200">
                <Eye className="w-3 h-3 text-primary" />
                <h3 className="text-primary font-bold text-xs">데이터 미리보기</h3>
              </div>
              <div className="p-3 space-y-3">
                {/* 통계 카드 */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm">
                  {/* ... 도메인별 통계 카드 */}
                </div>

                {/* 미리보기 테이블 */}
                <div className="border border-gray-200 rounded-sm overflow-hidden">
                  <div className="bg-gray-50 px-2 py-1 border-b border-gray-200">
                    <h4 className="text-xs font-medium text-gray-600">처음 15건 미리보기</h4>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead className="bg-gray-50 border-b border-gray-200">
                        <tr>{/* 도메인별 컬럼 헤더 */}</tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100 bg-white">
                        {parsedData.slice(0, 15).map((row, i) => (
                          <tr key={i} className="hover:bg-gray-50">
                            {/* 도메인별 컬럼 데이터 */}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  {parsedData.length > 15 && (
                    <div className="bg-gray-50 px-2 py-1 border-t border-gray-200">
                      <p className="text-xxs text-gray-400 text-center">... 외 {parsedData.length - 15}건 더 있음</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* 결과 섹션 */}
          {importResult && (
            <div className="bg-white border border-gray-200 overflow-hidden">
              <div className="flex items-center gap-1 px-2 py-1.5 bg-gray-50 border-b border-gray-200">
                {importResult.success
                  ? <Check className="w-3 h-3 text-emerald-600" />
                  : <AlertCircle className="w-3 h-3 text-red-600" />}
                <h3 className={`font-bold text-xs ${importResult.success ? 'text-emerald-700' : 'text-red-700'}`}>
                  {importResult.success ? '가져오기 완료' : '가져오기 실패'}
                </h3>
              </div>
              <div className={`p-3 ${importResult.success ? 'bg-emerald-50' : 'bg-red-50'}`}>
                {importResult.success ? (
                  <div className="flex items-center gap-2">
                    <Check className="w-5 h-5 text-emerald-600 shrink-0" />
                    <div className="text-sm text-emerald-700 font-medium">
                      {importResult.added.toLocaleString()}건 추가 완료
                      {importResult.skipped > 0 && (
                        <span className="text-gray-500 font-normal ml-1">(중복 {importResult.skipped.toLocaleString()}건 건너뜀)</span>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="flex items-start gap-2">
                    <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
                    <span className="text-sm text-red-700 font-medium">데이터 가져오기에 실패했습니다.</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex gap-3 px-6 py-4 border-t bg-gray-50">
          {isComplete ? (
            <>
              <button onClick={handleReset} className="flex-1 flex items-center justify-center gap-2 px-4 py-2 border border-gray-300 rounded-sm hover:bg-gray-100 text-sm font-medium">
                <RotateCcw className="w-4 h-4" /> 다른 파일 가져오기
              </button>
              <button onClick={onClose} className="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-sm hover:bg-emerald-700 text-sm font-medium">닫기</button>
            </>
          ) : (
            <>
              <button onClick={onClose} className="flex-1 px-4 py-2 border border-gray-300 rounded-sm hover:bg-gray-100 text-sm font-medium">취소</button>
              <button
                onClick={handleImport}
                disabled={!isParsed || isImporting}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-sm hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
              >
                {isImporting ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> 가져오는 중...</>
                ) : (
                  <><Upload className="w-4 h-4" /> {isParsed ? `${parsedData.length.toLocaleString()}건 가져오기` : '가져오기'}</>
                )}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
```

### Step 4: barrel export 업데이트

해당 도메인의 `index.ts`에 export를 추가합니다:

```typescript
export { <PascalCase>ImportModal } from './<PascalCase>ImportModal';
```

### Step 5: 부모 컴포넌트 연동 안내

가져오기 모달을 호출하는 부모 컴포넌트에서:

```tsx
// 1. state 추가
const [isImportOpen, setIsImportOpen] = useState(false);

// 2. onImport 콜백 (훅에서 mutation 함수를 가져와 사용)
const handleImport = async (rows: <PascalCase>ImportRow[]) => {
  // Firebase batch write or mutation
  const batch = writeBatch(db);
  // ... batch.set/update
  await batch.commit();
  return { added: rows.length, skipped: 0 };
};

// 3. 버튼 추가
<button onClick={() => setIsImportOpen(true)}>
  xlsx 가져오기
</button>

// 4. 모달 렌더
<<PascalCase>ImportModal
  isOpen={isImportOpen}
  onClose={() => setIsImportOpen(false)}
  onImport={handleImport}
/>
```

### Step 6: 검증

1. 컴포넌트 파일 존재 확인
2. `useExcelImport` import 확인
3. barrel export 존재 확인
4. TypeScript 타입 오류 없는지 확인

## Output Format

```markdown
## 가져오기 모달 생성 완료

| 항목 | 상태 | 파일 |
|------|------|------|
| 타입 정의 | 생성됨 | `components/<Name>/<Name>ImportModal.tsx` (상단) |
| 모달 컴포넌트 | 생성됨 | `components/<Name>/<Name>ImportModal.tsx` |
| barrel export | 업데이트 | `components/<Name>/index.ts` |
| useExcelImport | 연동됨 | `hooks/useExcelImport.ts` |

필드 매핑:
- `이름` → studentName (string)
- `학년` → grade (string)
- ...

다음 단계:
1. 부모 컴포넌트에서 모달 열기/닫기 state 추가
2. `onImport` 콜백에서 Firebase batch write 구현
3. 통계 카드와 미리보기 테이블의 컬럼을 도메인에 맞게 커스터마이즈
```

## Design Decisions

### useExcelImport 훅 사용 이유

프로젝트에 이미 7개의 가져오기 모달이 존재하며, 모두 동일한 상태 관리 패턴을 반복합니다:
- `fileInputRef`, `parsedData`, `fileName`, `isImporting`, `importResult` state
- `handleFileChange` (xlsx 파싱), `handleImport`, `handleReset` 핸들러

`useExcelImport` 훅은 이 공통 로직을 캡슐화하여:
- 새 모달 작성 시 코드량 60% 감소
- 상태 관리 버그 방지 (검증된 패턴 재사용)
- 일관된 UX (파일 선택 → 미리보기 → 가져오기 → 결과)

### 모달 UI 표준

모든 가져오기 모달은 동일한 4섹션 구조를 따릅니다:
1. **헤더** — FileSpreadsheet 아이콘 + 도메인명 + 닫기 버튼
2. **파일 업로드** — 점선 border 버튼 + hidden input
3. **미리보기** — 통계 카드(grid) + 테이블(처음 15건)
4. **푸터** — 완료 전: 취소/가져오기 | 완료 후: 다른 파일/닫기

색상 체계: emerald(성공), red(실패), gray(기본), blue(통계)

## Exceptions

다음은 **문제가 아닙니다**:

1. **통계 카드/테이블 컬럼이 TODO** — 도메인별 커스터마이즈가 필요한 부분이므로 생성 후 수동 조정
2. **onImport에 Firebase 로직이 없는 것** — 가져오기 모달은 UI만 담당하고, 저장 로직은 부모/훅에서 구현
3. **학생 매칭 미포함** — 학생 매칭이 필요한 경우에만 `studentIds` prop과 `studentMatching.ts` 유틸 연동
