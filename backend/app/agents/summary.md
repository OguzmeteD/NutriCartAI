# Değişiklik Özeti — Multi-Agent Pipeline + FastAPI Endpoint

## Ne Eklendi

`backend/app/agents/` klasörü oluşturuldu ve `backend/app/routers/chat.py` ile FastAPI entegrasyonu yapıldı.
Daha önce yanlışlıkla oluşturulan `src/backend/agents/` klasörü silindi.

## Dosyalar

### `backend/app/agents/`
| Dosya | Açıklama |
|---|---|
| `deps.py` | `AgentUserProfile` ve `AgentDeps` dataclass'ları — tüm ajanlara enjekte edilir |
| `models.py` | Pydantic çıktı modelleri: `PlannerOutput`, `BudgetOutput`, `SportCoachOutput`, `CalendarOutput`, `ManagerResponse` |
| `planner.py` | Planner Agent — günlük/haftalık plan, yemek programı, görev listesi |
| `budget.py` | Budget Agent — maliyet tahmini, bütçe dökümü, tasarruf önerileri |
| `sport_coach.py` | Sport Coach Agent — antrenman planı, fitness hedefleri, beslenme tavsiyeleri |
| `calendar.py` | Calendar Agent — planları yapılandırılmış takvim etkinliklerine dönüştürür |
| `manager.py` | Manager Agent — koordinatör; ilgili alt ajanlara yönlendirir |
| `pipeline.py` | `run_pipeline()` + `configure_langfuse_tracing()` |
| `__init__.py` | Paket public API'si |

### `backend/app/routers/chat.py`
`POST /chat` endpoint'i. JWT ile kimlik doğrulama, `run_pipeline()` çağrısı, `ChatResponse` dönüşü.

### `backend/app/main.py` (güncellendi)
`lifespan` context manager eklendi — uygulama başlarken `configure_langfuse_tracing()` çalışır.
`chat.router` eklendi.

### `backend/pyproject.toml` (güncellendi)
`pydantic-ai[bedrock]` ve `logfire` bağımlılıkları eklendi.

## Mimari Kararlar

### Neden `src/backend/` silindi?
Gerçek Python paketi `backend/app/` altında. `src/backend/` ayrı bir dizin olduğu için import edilemiyordu — çakışma yaratırdı.

### `AgentUserProfile` ismi
`app.models.user.UserProfile` (auth modeli) ile çakışmayı önlemek için agents katmanında `AgentUserProfile` adı kullanıldı.

### Langfuse Tracing
`configure_langfuse_tracing()` FastAPI `lifespan` içinde bir kez çağrılır. `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` eksikse tracing sessizce devre dışı kalır, uygulama çalışmaya devam eder.

### Session ID
Her `/chat` isteğinde `uuid4()` ile üretilir — ilerideki memory katmanı için trace anahtarı görevi görür.

## Kurulum

```bash
cd backend
uv sync
cp .env.example .env  # MODEL_ID ve Langfuse anahtarlarını doldur
uv run uvicorn app.main:app --reload
```

## Örnek İstek

```bash
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bu hafta için sağlıklı plan yap, bütçeme uygun mu kontrol et",
    "fitness_goals": ["kilo vermek"],
    "monthly_budget": 1500
  }'
```
