"""Seed dữ liệu mẫu cho demo/user study.

Chạy:  python -m app.seed
Idempotent — đã có versions thì bỏ qua. Nội dung khớp mock của FE
(app/src/api/mock.ts) để UI hiển thị đúng ngay.
"""
import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine
from app.models.app_settings import AppSettings
from app.models.base import Base
from app.models.lesson import Lesson
from app.models.lesson_item import LessonItem
from app.models.version import Version

VERSIONS = [
    {"code": "v1", "name": "Bảng chữ cái (V1 — tĩnh)", "description": "Chữ cái ASL, giữ tay ổn định", "order_index": 1},
    {"code": "v2", "name": "Từ giao tiếp (V2 — động)", "description": "Từ vựng ASL có chuyển động", "order_index": 2},
]

LESSONS = [
    {"version": "v1", "title": "Nhóm A–E", "description": "5 chữ cái tĩnh đầu tiên của bảng chữ cái ASL", "order_index": 1,
     "items": [
         {"sign_label": "A", "item_type": "static", "difficulty": 1, "confusable": ["S", "T", "M", "N"],
          "steps": [
              {"param": "handshape", "text": "Nắm bàn tay, 4 ngón cuộn tròn, ngón cái áp thẳng bên hông bàn tay"},
              {"param": "orientation", "text": "Lòng bàn tay hướng vào trong (thấy mu bàn tay từ trước)"},
          ]},
         {"sign_label": "B", "item_type": "static", "difficulty": 1, "confusable": ["4", "D"],
          "steps": [
              {"param": "handshape", "text": "Duỗi thẳng 4 ngón, khép sát nhau, ngón cái gập vào lòng bàn tay"},
              {"param": "orientation", "text": "Lòng bàn tay hướng ra trước"},
          ]},
         {"sign_label": "C", "item_type": "static", "difficulty": 1, "confusable": ["O"],
          "steps": [
              {"param": "handshape", "text": "Cong cả bàn tay thành hình chữ C, các ngón giữ độ cong đều"},
              {"param": "orientation", "text": "Lòng bàn tay hướng sang phải (người đối diện thấy hình C)"},
          ]},
         {"sign_label": "D", "item_type": "static", "difficulty": 2, "confusable": ["1", "B"],
          "steps": [
              {"param": "handshape", "text": "Duỗi ngón trỏ hướng lên, 3 ngón còn lại chạm ngón cái thành vòng tròn"},
              {"param": "orientation", "text": "Lòng bàn tay hướng vào trong"},
          ]},
         {"sign_label": "E", "item_type": "static", "difficulty": 2, "confusable": ["S", "M", "N"],
          "steps": [
              {"param": "handshape", "text": "4 ngón gập xuống chạm nhẹ ngón cái, tạo hình vuông nhỏ giữa các ngón"},
              {"param": "orientation", "text": "Lòng bàn tay hướng vào trong"},
          ]},
     ]},
    {"version": "v2", "title": "Chào hỏi", "description": "Các từ chào hỏi giao tiếp hằng ngày", "order_index": 1,
     "items": [
         {"sign_label": "HELLO", "item_type": "dynamic", "difficulty": 2, "confusable": ["GOODBYE"],
          "steps": [
              {"param": "handshape", "text": "Duỗi bàn tay kiểu B (như chữ B)"},
              {"param": "location", "text": "Đặt cạnh trán, ngón tay chạm nhẹ thái dương"},
              {"param": "movement", "text": "Vung tay ra trước và ra ngoài khỏi trán"},
          ]},
         {"sign_label": "THANK YOU", "item_type": "dynamic", "difficulty": 2, "confusable": ["GOOD"],
          "steps": [
              {"param": "handshape", "text": "Duỗi bàn tay phẳng, các ngón khép (kiểu B)"},
              {"param": "location", "text": "Bắt đầu từ gần cằm"},
              {"param": "movement", "text": "Đưa tay ra trước và hơi xuống về phía người đối diện"},
          ]},
         {"sign_label": "YES", "item_type": "dynamic", "difficulty": 1, "confusable": ["NO"],
          "steps": [
              {"param": "handshape", "text": "Nắm bàn tay thành nắm đấm kiểu S"},
              {"param": "location", "text": "Đặt trước ngực, cao hơn vai một chút"},
              {"param": "movement", "text": "Gập cổ tay xuống rồi nâng lên như gật đầu"},
          ]},
         {"sign_label": "NO", "item_type": "dynamic", "difficulty": 1, "confusable": ["YES"],
          "steps": [
              {"param": "handshape", "text": "Duỗi ngón trỏ và ngón giữa, khép lại như chữ U"},
              {"param": "location", "text": "Trước ngực"},
              {"param": "movement", "text": "Gập 2 ngón chạm ngón cái rồi mở ra lại (như mỏ chim)"},
          ]},
     ]},
    {"version": "v2", "title": "Câu lịch sự", "description": "Từ lịch sự trong giao tiếp", "order_index": 2,
     "items": [
         {"sign_label": "PLEASE", "item_type": "dynamic", "difficulty": 3, "confusable": ["SORRY"],
          "steps": [
              {"param": "handshape", "text": "Bàn tay phẳng duỗi (kiểu B)"},
              {"param": "location", "text": "Đặt trước ngực"},
              {"param": "movement", "text": "Xoay tròn bàn tay vài vòng trên ngực theo chiều kim đồng hồ"},
          ]},
         {"sign_label": "SORRY", "item_type": "dynamic", "difficulty": 3, "confusable": ["PLEASE"],
          "steps": [
              {"param": "handshape", "text": "Nắm bàn tay kiểu A"},
              {"param": "location", "text": "Đặt trước ngực"},
              {"param": "movement", "text": "Xoay nắm đấm vài vòng trên ngực"},
          ]},
     ]},
]


def _reference(item_type: str, confusable: list) -> dict:
    return {
        "params": {
            "handshape": "per-sign",
            "orientation": "palm_in" if item_type == "static" else "per-sign",
            "location": "neutral_space" if item_type == "static" else "per-sign",
            "movement": "none" if item_type == "static" else "per-sign",
        },
        "confusable_with": confusable,
        "hold_ms": 1500 if item_type == "static" else 0,
        "trajectory_ref": None,
    }


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        existing = (await db.scalars(select(Version))).all()
        if existing:
            print(f"Đã có dữ liệu ({len(existing)} versions) — bỏ qua seed.")
            return

        versions = {v["code"]: Version(**v) for v in VERSIONS}
        db.add_all(versions.values())
        await db.flush()

        order = 0
        for lesson_def in LESSONS:
            lesson = Lesson(
                version_id=versions[lesson_def["version"]].id,
                title=lesson_def["title"],
                description=lesson_def["description"],
                order_index=lesson_def["order_index"],
                is_active=True,
            )
            db.add(lesson)
            await db.flush()
            for item_def in lesson_def["items"]:
                order += 1
                db.add(LessonItem(
                    lesson_id=lesson.id,
                    sign_label=item_def["sign_label"],
                    item_type=item_def["item_type"],
                    difficulty=item_def["difficulty"],
                    media={},
                    steps=item_def["steps"],
                    reference_data=_reference(item_def["item_type"], item_def["confusable"]),
                    order_index=order,
                    is_active=True,
                ))

        db.add(AppSettings(setting_key="feedback_mode", setting_value={"mode": "adaptive"}))
        await db.commit()
        print(f"Seed xong: {len(VERSIONS)} versions, {len(LESSONS)} lessons, {order} items, settings feedback_mode=adaptive.")


if __name__ == "__main__":
    # Áp dụng migrations (nếu chưa) rồi seed — giữ nhất quán với alembic
    from alembic import command
    from alembic.config import Config

    command.upgrade(Config("alembic.ini"), "head")
    asyncio.run(seed())
