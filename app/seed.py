
"""Seed dữ liệu mẫu cho Signora.

Chạy:
    python -m app.seed

Idempotent:
- Tạo versions, lessons, lesson_items nếu chưa có.
- Không tạo dữ liệu trùng khi chạy nhiều lần.
- Không ghi đè media và dữ liệu đã có.
"""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal

from app.models.app_settings import AppSettings
from app.models.lesson import Lesson
from app.models.lesson_item import LessonItem
from app.models.version import Version
from app.core.database import engine
from app.models.base import Base
VERSIONS = [
    {
        "code": "v1",
        "name": "Bảng chữ cái (V1 - tĩnh)",
        "description": "Bảng chữ cái ASL từ A đến Z",
        "order_index": 1,
    },
    {
        "code": "v2",
        "name": "Từ giao tiếp (V2 - động)",
        "description": "Các từ vựng ASL có chuyển động",
        "order_index": 2,
    },
]


# --------------------------------------------------
# V1: BẢNG CHỮ CÁI A-Z
# --------------------------------------------------

ALPHABET = [
    ("A", 1, ["S", "T", "M", "N"],
     "Nắm bàn tay, ngón cái áp sát bên cạnh các ngón đang gập."),

    ("B", 1, ["4", "D"],
     "Duỗi thẳng bốn ngón, khép sát nhau, ngón cái gập vào lòng bàn tay."),

    ("C", 1, ["O"],
     "Cong bàn tay tạo thành hình chữ C."),

    ("D", 2, ["1", "B"],
     "Duỗi ngón trỏ, ba ngón còn lại chạm ngón cái tạo vòng tròn."),

    ("E", 2, ["S", "M", "N"],
     "Gập các ngón tay xuống gần lòng bàn tay, ngón cái đặt phía trước."),

    ("F", 2, ["9"],
     "Chạm ngón trỏ và ngón cái thành vòng tròn, ba ngón còn lại duỗi."),

    ("G", 2, ["H"],
     "Duỗi ngón cái và ngón trỏ theo phương ngang."),

    ("H", 2, ["G", "U"],
     "Duỗi ngón trỏ và ngón giữa song song theo phương ngang."),

    ("I", 1, ["J"],
     "Nắm bàn tay, duỗi ngón út lên."),

    ("J", 2, ["I"],
     "Tạo hình chữ I rồi di chuyển ngón út theo quỹ đạo chữ J."),

    ("K", 2, ["P", "V"],
     "Duỗi ngón trỏ và ngón giữa, ngón cái đặt giữa hai ngón."),

    ("L", 1, ["G"],
     "Duỗi ngón cái và ngón trỏ tạo hình chữ L."),

    ("M", 2, ["N", "E"],
     "Gập ba ngón giữa qua ngón cái."),

    ("N", 2, ["M", "E"],
     "Gập hai ngón giữa qua ngón cái."),

    ("O", 1, ["C"],
     "Cong các ngón tay tạo thành hình vòng tròn."),

    ("P", 2, ["K", "Q"],
     "Tạo hình chữ K và hướng bàn tay xuống dưới."),

    ("Q", 2, ["G", "P"],
     "Duỗi ngón cái và ngón trỏ hướng xuống dưới."),

    ("R", 2, ["U"],
     "Duỗi ngón trỏ và ngón giữa, bắt chéo hai ngón."),

    ("S", 1, ["A", "T"],
     "Nắm bàn tay, ngón cái đặt phía trước các ngón."),

    ("T", 2, ["A", "S"],
     "Nắm bàn tay, đặt ngón cái giữa ngón trỏ và ngón giữa."),

    ("U", 1, ["V", "R"],
     "Duỗi ngón trỏ và ngón giữa khép sát nhau."),

    ("V", 1, ["U", "K"],
     "Duỗi ngón trỏ và ngón giữa tách thành hình chữ V."),

    ("W", 2, ["6"],
     "Duỗi ngón trỏ, giữa và áp út."),

    ("X", 2, ["D"],
     "Duỗi ngón trỏ và gập cong tại khớp giữa."),

    ("Y", 1, ["I"],
     "Duỗi ngón cái và ngón út, các ngón còn lại nắm lại."),

    ("Z", 2, [],
     "Dùng ngón trỏ vẽ quỹ đạo chữ Z trong không gian."),
]

MEDIA_BY_LABEL = {
    "A": {
        "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794413031/A.mp4"
    },
    "B": {
        "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794491513/B.mp4"
    },
    "C": {
        "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794491512/C.mp4"
    },
    "D": {
        "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794491513/D.mp4"
    },
    "E": {
        "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794491513/E.mp4"
    },
    "F": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666497/F.mp4"
        },
    "G": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666497/G.mp4"
        },
    "H": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666500/H.mp4"
        },
    "I": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666501/I.mp4"
        },
    "J": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666502/J.mp4"
        },
    "K": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666502/K.mp4"
        },
    "L": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666499/L.mp4"
        },
    "M": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666503/M.mp4"
        },
    "N": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666520/N.mp4"
        },
    "O": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666518/O.mp4"
        },
    "P": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666518/P.mp4"
        },
    "Q": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666518/P.mp4"
        },
    "R": {
            "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794666518/R.mp4"
        },
    "S": {
                "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759606/S.mp4"
        },
    "T": {
                "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759609/T.mp4"
        },
    "U": {
                    "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759608/U.mp4"
            },
    "V": {
                    "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759609/V.mp4"
            },
    "W": {
                    "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759609/W.mp4"
            },
    "X": {
                    "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759607/X.mp4"
            },
    "Y": {
                    "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759606/Y.mp4"
            },
     "Z": {
                    "demo_video": "https://res.cloudinary.com/zm4ykptz/video/upload/v1794759606/Z.mp4"
            },

    # Bổ sung URL Cloudinary thực tế cho F-Z
    # Ví dụ:
    # "F": {"demo_video": "URL_VIDEO_F"},
}

def make_static_steps(description: str):
    return [
        {
            "param": "handshape",
            "text": description,
        },
        {
            "param": "orientation",
            "text": "Giữ bàn tay ổn định, hướng lòng bàn tay theo mẫu tham chiếu.",
        },
    ]


def make_reference(item_type: str, confusable: list):
    return {
        "params": {
            "handshape": "per-sign",
            "orientation": "per-sign",
            "location": (
                "neutral_space"
                if item_type == "static"
                else "per-sign"
            ),
            "movement": (
                "none"
                if item_type == "static"
                else "per-sign"
            ),
        },
        "confusable_with": confusable,
        "hold_ms": 1500 if item_type == "static" else 0,
        "trajectory_ref": None,
    }


# --------------------------------------------------
# V2: TỪ GIAO TIẾP
# --------------------------------------------------


# --------------------------------------------------
# V2: TỪ GIAO TIẾP THEO 18 CHỦ ĐỀ
# Nguồn danh sách: GestureSign
# Video hướng dẫn tạm thời để trống.
# --------------------------------------------------

V2_TOPICS = [
    {
        "title": "Giao tiếp",
        "description": "Các ký hiệu sử dụng trong giao tiếp hằng ngày",
        "words": """
            bye, call (on phone), hear, hello, listen, look, no, please,
            read, say, see, shh, talk, thank you, where, who, why, yes
        """,
    },
    {
        "title": "Sinh hoạt hằng ngày",
        "description": "Các hoạt động và sinh hoạt thường ngày",
        "words": """
            awake, bath, blow, clean, close, cry, cut, dance, dirty, drop,
            dry, find, finish, give, go, hide, jump, make, nap, open, ride,
            shower, sleep, smile, stay, wake, wet
        """,
    },
    {
        "title": "Cảm xúc và trạng thái",
        "description": "Các từ mô tả cảm xúc và trạng thái",
        "words": """
            bad, better, cute, empty, fast, fine, happy, hate, hot, hungry,
            like, loud, mad, noisy, old, owie, pretty, quiet, sad, sick,
            sleepy, sticky, stuck, thirsty, yucky
        """,
    },
    {
        "title": "Gia đình và con người",
        "description": "Các thành viên gia đình và con người",
        "words": """
            aunt, boy, brother, child, clown, cowboy, dad, fireman, girl,
            grandma, grandpa, man, mom, person, police, uncle
        """,
    },
    {
        "title": "Đồ ăn và thức uống",
        "description": "Các loại đồ ăn và thức uống",
        "words": """
            apple, carrot, cereal, chocolate, drink, food, french fries,
            gum, ice cream, milk, nuts, orange, pizza, snack, taste, water
        """,
    },
    {
        "title": "Cơ thể và giác quan",
        "description": "Các bộ phận cơ thể và giác quan",
        "words": """
            arm, cheek, chin, ear, eye, face, feet, finger, hair, head,
            kiss, lips, mouth, nose, tongue, tooth, touch
        """,
    },
    {
        "title": "Động vật",
        "description": "Tên các loài động vật",
        "words": """
            alligator, animal, bee, bird, bug, cat, cow, dog, donkey, duck,
            elephant, fish, frog, giraffe, goose, hen, horse, kitty, lion,
            mouse, owl, pig, puppy, tiger, wolf, zebra
        """,
    },
    {
        "title": "Màu sắc",
        "description": "Các màu sắc cơ bản",
        "words": """
            black, blue, brown, green, red, white, yellow
        """,
    },
    {
        "title": "Nhà cửa và địa điểm",
        "description": "Các không gian và địa điểm quen thuộc",
        "words": """
            backyard, bedroom, closet, farm, home, outside, pool, room,
            stairs, store
        """,
    },
    {
        "title": "Đồ dùng và giải trí",
        "description": "Đồ vật, vật dụng và hoạt động giải trí",
        "words": """
            balloon, bed, book, chair, doll, drawer, dryer, flag, garbage,
            gift, glass / window, lamp, napkin, pen, pencil, penny, potty,
            puzzle, radio, refrigerator, scissors, story, table, toothbrush,
            toy, TV, vacuum
        """,
    },
    {
        "title": "Quần áo và phụ kiện",
        "description": "Các loại quần áo và phụ kiện",
        "words": """
            hat, jacket, jeans, mitten, pajamas, shirt, shoe, underwear,
            zipper
        """,
    },
    {
        "title": "Thiên nhiên và thời tiết",
        "description": "Các yếu tố thiên nhiên và thời tiết",
        "words": """
            cloud, flower, grass, moon, rain, snow, sun, tree
        """,
    },
    {
        "title": "Phương tiện di chuyển",
        "description": "Các phương tiện giao thông",
        "words": """
            airplane, boat, car, helicopter
        """,
    },
    {
        "title": "Thời gian và thứ tự",
        "description": "Các từ chỉ thời gian và trình tự",
        "words": """
            after, before, first, later, morning, night, now, time,
            tomorrow, yesterday
        """,
    },
    {
        "title": "Vị trí và hướng",
        "description": "Các từ chỉ vị trí và phương hướng",
        "words": """
            beside, down, high, into, on, there, up
        """,
    },
    {
        "title": "Đại từ và từ sở hữu",
        "description": "Các đại từ và từ chỉ sở hữu",
        "words": """
            he / she / it, mine / my, we / us, yourself
        """,
    },
    {
        "title": "Từ chỉ lượng và từ nối",
        "description": "Các từ chỉ số lượng và liên kết ý",
        "words": """
            all, another, any, because, every, for, if, many, not, same,
            that
        """,
    },
    {
        "title": "Khả năng và hành động",
        "description": "Các từ chỉ khả năng và hành động",
        "words": """
            can, fall, have, have to, pretend, think, wait, will
        """,
    },
]


def build_v2_lessons():
    lessons = []

    for index, topic in enumerate(V2_TOPICS, start=1):
        words = [
            word.strip()
            for word in topic["words"].replace("\n", " ").split(",")
            if word.strip()
        ]

        lessons.append({
            "title": topic["title"],
            "description": topic["description"],
            "order_index": index,
            "items": [
                {
                    "sign_label": word.upper(),
                    "difficulty": 1,
                    "confusable": [],
                    "steps": [],
                }
                for word in words
            ],
        })

    return lessons


V2_LESSONS = build_v2_lessons()

# --------------------------------------------------
# SEED HELPERS
# --------------------------------------------------

async def get_or_create_version(db, definition):
    version = await db.scalar(
        select(Version).where(
            Version.code == definition["code"]
        )
    )

    if version:
        return version

    version = Version(**definition)
    db.add(version)
    await db.flush()

    return version


async def get_or_create_lesson(db, version_id, definition):
    lesson = await db.scalar(
        select(Lesson).where(
            Lesson.version_id == version_id,
            Lesson.title == definition["title"],
        )
    )

    if lesson:
        return lesson

    lesson = Lesson(
        version_id=version_id,
        title=definition["title"],
        description=definition["description"],
        order_index=definition["order_index"],
        is_active=True,
    )

    db.add(lesson)
    await db.flush()

    return lesson



async def seed_items(db, lesson, items, item_type):
    existing_items = (
        await db.scalars(
            select(LessonItem).where(
                LessonItem.lesson_id == lesson.id
            )
        )
    ).all()

    existing_by_label = {
        item.sign_label: item
        for item in existing_items
    }

    for index, item in enumerate(items, start=1):
        label = item["sign_label"]

        media = MEDIA_BY_LABEL.get(label, {}) if item_type == "static" else {}
        existing = existing_by_label.get(label)

        # J và Z là ký hiệu động dù thuộc bảng chữ cái V1
        current_item_type = (
            "dynamic"
            if label in {"J", "Z"} and item_type == "static"
            else item_type
        )

        if existing:
            if not existing.media and media:
                existing.media = media
                print(f"[MEDIA] Đã bổ sung video cho {label}")

            # Cập nhật loại ký hiệu cho dữ liệu đã tồn tại
            if existing.item_type != current_item_type:
                existing.item_type = current_item_type
                print(f"[UPDATE] Đã cập nhật loại ký hiệu {label}: {current_item_type}")

            continue

        if current_item_type == "static":
            steps = make_static_steps(item["description"])
        else:
            steps = item.get("steps", [])

        db.add(
            LessonItem(
                lesson_id=lesson.id,
                sign_label=label,
                item_type=current_item_type,
                difficulty=item["difficulty"],
                media=media,
                steps=steps,
                reference_data=make_reference(
                    current_item_type,
                    item["confusable"],
                ),
                order_index=index,
                is_active=True,
            )
        )

        print(f"[SEED] Đã tạo item {label}")
    
    await db.flush()


# --------------------------------------------------
# MAIN SEED
# --------------------------------------------------

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        try:
            versions = {}

            for definition in VERSIONS:
                versions[definition["code"]] = (
                    await get_or_create_version(db, definition)
                )

            # V1: A-Z
            v1_lesson = await get_or_create_lesson(
                db,
                versions["v1"].id,
                {
                    "title": "Bảng chữ cái A-Z",
                    "description": "26 chữ cái ASL từ A đến Z",
                    "order_index": 1,
                },
            )

            v1_items = [
                {
                    "sign_label": label,
                    "difficulty": difficulty,
                    "confusable": confusable,
                    "description": description,
                }
                for label, difficulty, confusable, description in ALPHABET
            ]

            await seed_items(
                db,
                v1_lesson,
                v1_items,
                "static",
            )

            # V2: Các nhóm từ giao tiếp
            for lesson_definition in V2_LESSONS:
                lesson = await get_or_create_lesson(
                    db,
                    versions["v2"].id,
                    lesson_definition,
                )

                await seed_items(
                    db,
                    lesson,
                    lesson_definition["items"],
                    "dynamic",
                )

            # App settings
            setting = await db.scalar(
                select(AppSettings).where(
                    AppSettings.setting_key == "feedback_mode"
                )
            )

            if not setting:
                db.add(
                    AppSettings(
                        setting_key="feedback_mode",
                        setting_value={"mode": "adaptive"},
                    )
                )

            await db.commit()

            total_items = await db.scalar(
                select(LessonItem.id)
            )

            print("Seed Signora hoàn tất!")
            print("V1: 26 chữ cái A-Z")
            print("V2: 6 từ giao tiếp")
            print("Tổng: 32 LessonItems")

        except Exception:
            await db.rollback()
            raise

async def main():
    try:
        await seed()
    finally:
        await engine.dispose()
        
        
if __name__ == "__main__":
    asyncio.run(seed())
